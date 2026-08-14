(function(){
  'use strict';

  // 單元與核心概念名稱：與 app/main.mjs 的 units 表同源，改動時兩邊要一起改。
  var UNITS={
    numexpr:{name:'數與式',kp:['實數系與有理／無理','絕對值','數線、距離與根號估算','乘法公式與算幾不等式','比例、百分率與加權平均','高斯（最大整數）函數']},
    poly:{name:'多項式函數',kp:['除法、餘式與因式定理','二次函數：判別式與配方','多項式方程式與不等式','高次方程式','三次函數圖形與對稱中心']},
    linecir:{name:'直線與圓',kp:['直線方程式與斜率','兩點距離與三角形','圓方程式','直線與圓的位置','平面區域與線性規劃']},
    seq:{name:'數列與級數',kp:['等差數列','等比數列','遞迴數列','級數求和與規律週期']},
    prob:{name:'排列組合與機率',kp:['計數原理與排列','組合與分組分配','古典機率','條件機率與貝氏','獨立事件與餘事件','期望值']},
    data:{name:'數據分析',kp:['一維數據與標準差','相關係數','迴歸直線（最適直線）','加權平均與資料判讀']},
    explog:{name:'指數與對數',kp:['指數律與指數方程','對數的定義與運算','常用對數（科學記號、位數）','指數對數函數圖形','應用模型與數列結合']},
    trig:{name:'三角',kp:['三角比、弧度與廣義角','正弦定理、餘弦定理','三角測量與幾何應用','三角函數圖形','和差角、倍角','角平分線、面積比與相似','圓周角與二面角中的三角']},
    pvec:{name:'平面向量',kp:['向量的表示與運算','線性組合、分點與面積比','內積：夾角、垂直、正射影','行列式與平行四邊形面積','向量的旋轉與坐標應用']},
    space:{name:'空間向量',kp:['空間坐標、距離與正立方體','內積、夾角與垂直','外積、面積與體積','平面方程式、投影與點到平面距離','空間直線、軌跡與歪斜線','二面角與立體']},
    matrix:{name:'矩陣',kp:['矩陣的意義、相等與乘法','矩陣的高次方','反方陣與解矩陣方程式','一次聯立與高斯消去','平面線性變換']}
  };
  var STATUS_LABEL={STABLE:'✓ 穩定',EMERGING:'△ 初步',NEEDS_REVIEW:'! 需複習',INSUFFICIENT_EVIDENCE:'… 證據不足',UNTESTED:'○ 未診斷'};
  var STATUS_ORDER=['NEEDS_REVIEW','INSUFFICIENT_EVIDENCE','EMERGING','STABLE','UNTESTED'];
  var STATUS_COLOR={STABLE:'#16794a',EMERGING:'#9a6700',NEEDS_REVIEW:'#b42318',INSUFFICIENT_EVIDENCE:'#1f6f78',UNTESTED:'#667085'};
  var ABILITY={CONCEPT:'概念理解',RECOGNITION:'線索辨識',APPLICATION:'應用遷移'};
  var EXPORT_STORES=['sessions','attempts','mastery','risks','remediation','reports'];

  var students=[];   // {label, units:{unitId:{records, generatedAt}}, hcw:[...], warn}
  var skipped=[];
  var el=function(id){return document.getElementById(id)};
  var esc=function(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})};

  // 與 app/repository.mjs 同一套雜湊：SHA-256 of JSON.stringify(payload[store])
  function sha256(value){
    var bytes=new TextEncoder().encode(JSON.stringify(value));
    return crypto.subtle.digest('SHA-256',bytes).then(function(buf){
      return Array.prototype.map.call(new Uint8Array(buf),function(b){return b.toString(16).padStart(2,'0')}).join('');
    });
  }

  // 檔名 → 學生代號。去掉副檔名，並剝掉 Google Classroom 常見的「姓名 - 檔名」前綴。
  function labelFromName(name){
    var base=String(name).replace(/\.[Jj][Ss][Oo][Nn]$/,'');
    var dash=base.split(' - ');
    if(dash.length>1)base=dash[dash.length-1];
    base=base.replace(/^mathmap-diagnostic-?/i,'').replace(/^\d{4}-\d{2}-\d{2}-?/,'');
    return base.trim()||name;
  }

  function parseBundle(text,fileName){
    var bundle=JSON.parse(text);
    if(!bundle||!bundle.payload)throw new Error('不是診斷系統的匯出檔');
    for(var i=0;i<EXPORT_STORES.length;i++){
      if(!Array.isArray(bundle.payload[EXPORT_STORES[i]]))throw new Error('缺少 '+EXPORT_STORES[i]+' 資料');
    }
    return bundle;
  }

  function verify(bundle){
    var hashes=bundle.hashes||{};
    var checks=EXPORT_STORES.filter(function(s){return hashes[s]});
    if(!checks.length)return Promise.resolve('這個檔沒有完整性雜湊，無法驗證是否被改過');
    return Promise.all(checks.map(function(s){
      return sha256(bundle.payload[s]).then(function(h){return h===hashes[s]?null:s});
    })).then(function(bad){
      var fails=bad.filter(Boolean);
      return fails.length?('完整性檢查未通過（'+fails.join('、')+'），資料可能被修改過'):null;
    });
  }

  // 每個單元取「最後產生」的那份報告
  function latestReports(bundle){
    var byUnit={};
    (bundle.payload.reports||[]).forEach(function(rep){
      var recs=rep.masteryRecords||[];
      if(!recs.length)return;
      var unitId=String(recs[0].kpId||'').split(':')[0];
      if(!UNITS[unitId])return;
      var prev=byUnit[unitId];
      if(!prev||String(rep.generatedAt)>String(prev.generatedAt))byUnit[unitId]={generatedAt:rep.generatedAt,records:recs};
    });
    return byUnit;
  }

  // 高信心答錯：直接從 attempts 算，比旗標精確到「哪一題」
  function highConfidenceWrong(bundle){
    return (bundle.payload.attempts||[]).filter(function(a){
      return a && a.correct===false && a.confidence==='HIGH' && !a.hintUsed;
    }).map(function(a){
      return {kpId:a.primaryConceptId,ability:a.ability,itemId:a.itemId,at:a.submittedAt};
    });
  }

  function addFiles(fileList){
    var files=Array.prototype.slice.call(fileList).filter(function(f){return /\.json$/i.test(f.name)});
    if(!files.length){el('load-msg').innerHTML='<div class="alert">沒有 .json 檔。請確認拖進來的是學生匯出的檔案。</div>';return;}
    el('load-msg').innerHTML='<p class="muted">讀取中…</p>';
    Promise.all(files.map(function(f){
      return f.text().then(function(t){
        var bundle=parseBundle(t,f.name);
        return verify(bundle).then(function(warn){
          return {label:labelFromName(f.name),fileName:f.name,units:latestReports(bundle),hcw:highConfidenceWrong(bundle),warn:warn};
        });
      }).catch(function(e){skipped.push({fileName:f.name,reason:e.message});return null;});
    })).then(function(rows){
      rows.filter(Boolean).forEach(function(r){
        if(!Object.keys(r.units).length){skipped.push({fileName:r.fileName,reason:'檔案有效，但裡面沒有任何已完成的診斷報告'});return;}
        var dup=students.findIndex(function(s){return s.label===r.label});
        if(dup>=0)students[dup]=r; else students.push(r);
      });
      render();
    });
  }

  function unitsPresent(){
    var set={};
    students.forEach(function(s){Object.keys(s.units).forEach(function(u){set[u]=(set[u]||0)+1})});
    return Object.keys(set).sort(function(a,b){return set[b]-set[a]});
  }

  function currentUnit(){return el('unit').value}

  function rowsFor(unitId){
    return students.filter(function(s){return s.units[unitId]}).map(function(s){
      var recs=s.units[unitId].records;
      var byKp={};
      recs.forEach(function(r){byKp[r.kpId]=r});
      var hcwKps={};
      s.hcw.forEach(function(h){if(String(h.kpId).indexOf(unitId+':')===0)hcwKps[h.kpId]=(hcwKps[h.kpId]||[]).concat([h])});
      var need=recs.filter(function(r){return r.status==='NEEDS_REVIEW'}).length;
      return {label:s.label,byKp:byKp,hcwKps:hcwKps,need:need,warn:s.warn,generatedAt:s.units[unitId].generatedAt};
    }).sort(function(a,b){return b.need-a.need || a.label.localeCompare(b.label,'zh-Hant')});
  }

  function kpIdList(unitId){
    return UNITS[unitId].kp.map(function(_,i){return unitId+':kp'+(i+1)});
  }

  function renderStats(unitId,rows){
    var kps=kpIdList(unitId);
    var total=rows.length*kps.length, counts={};
    STATUS_ORDER.forEach(function(s){counts[s]=0});
    rows.forEach(function(r){kps.forEach(function(k){var st=(r.byKp[k]||{}).status||'UNTESTED';counts[st]=(counts[st]||0)+1})});
    var hcwStudents=rows.filter(function(r){return Object.keys(r.hcwKps).length}).length;
    var needStudents=rows.filter(function(r){return r.need>0}).length;
    el('stats').innerHTML=
      stat(rows.length,'份有效資料')+
      stat(needStudents,'人有「需要複習」')+
      stat(hcwStudents,'人有高信心答錯')+
      stat(total?Math.round(counts.NEEDS_REVIEW/total*100)+'%':'—','格子是紅的')+
      stat(kps.length,'個核心概念');
  }
  function stat(v,t){return '<div class="stat"><strong>'+esc(v)+'</strong><span>'+esc(t)+'</span></div>'}

  function renderHcw(unitId,rows){
    var items=[];
    rows.forEach(function(r){
      Object.keys(r.hcwKps).forEach(function(k){
        r.hcwKps[k].forEach(function(h){items.push({label:r.label,kpId:k,ability:h.ability})});
      });
    });
    if(!items.length){el('hcw').innerHTML='<div class="notice">這個單元沒有人「高信心答錯」。要嘛他們對自己的判斷很準，要嘛是沒填信心欄位。</div>';return;}
    var byKp={};
    items.forEach(function(i){(byKp[i.kpId]=byKp[i.kpId]||[]).push(i)});
    var html='<div class="table-wrap"><table><thead><tr><th>核心概念</th><th>人數</th><th>學生（能力面向）</th></tr></thead><tbody>';
    Object.keys(byKp).sort().forEach(function(k){
      var list=byKp[k];
      var names={};
      list.forEach(function(i){(names[i.label]=names[i.label]||[]).push(ABILITY[i.ability]||i.ability)});
      var people=Object.keys(names).sort(function(a,b){return a.localeCompare(b,'zh-Hant')});
      html+='<tr><td><strong>'+esc(kpName(k))+'</strong></td><td>'+people.length+'</td><td>'+
        people.map(function(p){return esc(p)+'<span class="muted">（'+esc(names[p].join('、'))+'）</span>'}).join('、')+'</td></tr>';
    });
    el('hcw').innerHTML=html+'</tbody></table></div>';
  }

  function kpName(kpId){
    var parts=String(kpId).split(':');
    var u=UNITS[parts[0]];
    var n=Number(String(parts[1]||'').replace('kp',''));
    return u&&u.kp[n-1]?('核心概念 '+n+'　'+u.kp[n-1]):kpId;
  }

  function renderKpTable(unitId,rows){
    var kps=kpIdList(unitId);
    var html='<thead><tr><th>核心概念</th><th style="min-width:150px">班級分布</th>'+
      STATUS_ORDER.map(function(s){return '<th>'+esc(STATUS_LABEL[s])+'</th>'}).join('')+'</tr></thead><tbody>';
    kps.forEach(function(k){
      var counts={};STATUS_ORDER.forEach(function(s){counts[s]=0});
      rows.forEach(function(r){var st=(r.byKp[k]||{}).status||'UNTESTED';counts[st]=(counts[st]||0)+1});
      var total=rows.length||1;
      var bar='<div class="bar">'+STATUS_ORDER.map(function(s){
        return counts[s]?'<i style="width:'+(counts[s]/total*100)+'%;background:'+STATUS_COLOR[s]+'" title="'+esc(STATUS_LABEL[s])+' '+counts[s]+' 人"></i>':''
      }).join('')+'</div>';
      html+='<tr><td>'+esc(kpName(k))+'</td><td>'+bar+'</td>'+
        STATUS_ORDER.map(function(s){return '<td>'+(counts[s]||'—')+'</td>'}).join('')+'</tr>';
    });
    el('kptable').innerHTML=html+'</tbody>';
  }

  function renderMatrix(unitId,rows){
    var kps=kpIdList(unitId);
    var html='<thead><tr><th>學生</th>'+kps.map(function(k,i){
      return '<th class="kpcol" title="'+esc(UNITS[unitId].kp[i])+'">'+(i+1)+'　'+esc(UNITS[unitId].kp[i])+'</th>'
    }).join('')+'<th>需複習</th></tr></thead><tbody>';
    rows.forEach(function(r){
      var hot=Object.keys(r.hcwKps).length?' class="hcw"':'';
      html+='<tr'+hot+'><td class="name">'+esc(r.label)+(r.warn?' <span class="flagdot" title="'+esc(r.warn)+'">⚠</span>':'')+'</td>';
      kps.forEach(function(k){
        var st=(r.byKp[k]||{}).status||'UNTESTED';
        var dot=r.hcwKps[k]?' <span class="flagdot" title="高信心答錯">🔴</span>':'';
        html+='<td><span class="cell '+st+'">'+esc(STATUS_LABEL[st])+'</span>'+dot+'</td>';
      });
      html+='<td><strong>'+r.need+'</strong></td></tr>';
    });
    el('matrix').innerHTML=html+'</tbody>';
  }

  function renderFiles(){
    var html=students.map(function(s){
      return '<li><code>'+esc(s.fileName)+'</code> → <strong>'+esc(s.label)+'</strong>'+
        (s.warn?' <span class="flagdot" title="'+esc(s.warn)+'">⚠ '+esc(s.warn)+'</span>':'')+'</li>';
    }).join('');
    html+=skipped.map(function(s){
      return '<li class="muted"><code>'+esc(s.fileName)+'</code> — 略過：'+esc(s.reason)+'</li>';
    }).join('');
    el('flist').innerHTML=html;
    el('fcount').textContent=students.length;
  }

  function render(){
    if(!students.length){
      el('result').hidden=true;
      el('load-msg').innerHTML=skipped.length?'<div class="alert">沒有可用的資料。展開下面的清單看每個檔案被略過的原因。</div>':'';
      renderFiles();
      if(skipped.length)el('result').hidden=false;
      return;
    }
    var avail=unitsPresent();
    var sel=el('unit'), keep=sel.value;
    sel.innerHTML=avail.map(function(u){
      var n=students.filter(function(s){return s.units[u]}).length;
      return '<option value="'+u+'">'+esc(UNITS[u].name)+'（'+n+' 人）</option>';
    }).join('');
    if(avail.indexOf(keep)>=0)sel.value=keep;
    var unitId=sel.value;
    var rows=rowsFor(unitId);
    renderStats(unitId,rows);
    renderHcw(unitId,rows);
    renderKpTable(unitId,rows);
    renderMatrix(unitId,rows);
    renderFiles();
    var warns=students.filter(function(s){return s.warn}).length;
    el('load-msg').innerHTML='<p class="muted">已載入 <strong>'+students.length+'</strong> 份資料'+
      (skipped.length?('，略過 '+skipped.length+' 個檔'):'')+
      (warns?('　⚠ '+warns+' 份未通過完整性檢查'):'')+'</p>';
    el('result').hidden=false;
  }

  function toCsv(){
    var unitId=currentUnit(), rows=rowsFor(unitId), kps=kpIdList(unitId);
    var head=['學生'].concat(UNITS[unitId].kp.map(function(n,i){return (i+1)+' '+n})).concat(['需複習數','高信心答錯','備註']);
    var lines=[head];
    rows.forEach(function(r){
      var line=[r.label];
      kps.forEach(function(k){
        var st=(r.byKp[k]||{}).status||'UNTESTED';
        line.push(STATUS_LABEL[st].replace(/^[^一-龥]+/,''));
      });
      line.push(r.need);
      line.push(Object.keys(r.hcwKps).map(function(k){return '核心概念'+k.split('kp')[1]}).join(' '));
      line.push(r.warn||'');   // 完整性警告要跟著進 Excel，否則匯出後就看不見了
      lines.push(line);
    });
    var csv=lines.map(function(l){return l.map(function(c){
      var s=String(c==null?'':c);
      return /[",\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;
    }).join(',')}).join('\r\n');
    // BOM 讓 Excel 正確辨識 UTF-8
    var blob=new Blob(['﻿'+csv],{type:'text/csv;charset=utf-8'});
    var a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download='班級彙整-'+UNITS[unitId].name+'-'+new Date().toISOString().slice(0,10)+'.csv';
    a.click();
    setTimeout(function(){URL.revokeObjectURL(a.href)},1000);
  }

  var drop=el('drop');
  ['dragenter','dragover'].forEach(function(ev){
    drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.add('hot')});
  });
  ['dragleave','drop'].forEach(function(ev){
    drop.addEventListener(ev,function(e){e.preventDefault();if(ev==='dragleave'&&drop.contains(e.relatedTarget))return;drop.classList.remove('hot')});
  });
  drop.addEventListener('drop',function(e){
    e.preventDefault();
    if(e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files.length)addFiles(e.dataTransfer.files);
  });
  el('pick').addEventListener('click',function(){el('file').click()});
  el('file').addEventListener('change',function(e){if(e.target.files.length)addFiles(e.target.files);e.target.value='';});
  el('unit').addEventListener('change',render);
  el('csv').addEventListener('click',toCsv);
  el('print').addEventListener('click',function(){window.print()});
  el('clear').addEventListener('click',function(){students=[];skipped=[];render();el('load-msg').innerHTML='';});

  // 測試掛勾：讓自動化把檔案內容直接餵進來，不必真的操作檔案總管。
  window.__loadForTest=function(list){
    addFiles(list.map(function(x){return new File([x.text],x.name,{type:'application/json'})}));
  };
})();
