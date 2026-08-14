import { repository } from './repository.mjs';
import { diagnose } from '../engine/diagnose.mjs';

const main=document.querySelector('#main'),saveState=document.querySelector('#save-state');
const previewMode=new URLSearchParams(location.search).get('preview')==='1';
const currentPath=decodeURIComponent(location.pathname);
const localPreviewPath=currentPath.includes('/診斷系統/app/');
const mathMapRoot=localPreviewPath?'../../tmp/mathmap-source-audit/':currentPath.includes('/diagnostic/app/')?'../../':'../';
const units={
  poly:{name:'多項式函數',shortName:'多項式',minutes:'15–20',map:'concept-map/115學測數學_多項式函數.html',kp:['除法、餘式與因式定理','二次函數：判別式與配方','多項式方程式與不等式','高次方程式','三次函數圖形與對稱中心']},
  linecir:{name:'直線與圓',shortName:'直線與圓',minutes:'15–20',map:'concept-map/115學測數學_直線與圓.html',kp:['直線方程式與斜率','兩點距離與三角形','圓方程式','直線與圓的位置','平面區域與線性規劃']},
  seq:{name:'數列與級數',shortName:'數列與級數',minutes:'12–16',map:'concept-map/115學測數學_數列與級數.html',kp:['等差數列','等比數列','遞迴數列','級數求和與規律週期']},
  comb:{name:'排列組合',shortName:'排列組合',minutes:'12–16',map:'concept-map/115學測數學_排列組合與機率.html',kp:['計數原理與系統列舉','排列與位置限制','組合、重複組合與分組','分類計數與結果等價']},
  probability:{name:'機率',shortName:'機率',minutes:'12–16',map:'concept-map/115學測數學_排列組合與機率.html',kp:['樣本空間與古典機率','事件運算、餘事件與獨立','條件機率、全機率與貝氏','隨機變數與期望值']},
  data:{name:'數據分析',shortName:'數據分析',minutes:'12–16',map:'concept-map/115學測數學_數據分析.html',kp:['一維數據與標準差','相關係數','迴歸直線（最適直線）','加權平均與資料判讀']},
  explog:{name:'指數與對數',shortName:'指數與對數',minutes:'15–20',map:'concept-map/115學測數學_指數與對數.html',kp:['指數律與指數方程','對數的定義與運算','常用對數（科學記號、位數）','指數對數函數圖形','應用模型與數列結合']},
  trig:{name:'三角比與三角函數',shortName:'三角比與三角函數',minutes:'20–25',map:'concept-map/115學測數學_三角.html',kp:['三角比、弧度與廣義角','正弦定理、餘弦定理','三角測量與幾何應用','三角函數圖形','和差角、倍角','角平分線、面積比與相似','圓周角與二面角中的三角']},
  pvec:{name:'平面向量',shortName:'平面向量',minutes:'15–20',map:'concept-map/115學測數學_平面向量.html',kp:['向量的表示與運算','線性組合、分點與面積比','內積：夾角、垂直、正射影','行列式與平行四邊形面積','向量的旋轉與坐標應用']},
  space:{name:'空間向量',shortName:'空間向量',minutes:'18–24',map:'concept-map/115學測數學_空間向量.html',kp:['空間坐標、距離與正立方體','內積、夾角與垂直','外積、面積與體積','平面方程式、投影與點到平面距離','空間直線、軌跡與歪斜線','二面角與立體']},
  matrix:{name:'矩陣',shortName:'矩陣',minutes:'15–20',map:'concept-map/115學測數學_矩陣.html',kp:['矩陣的意義、相等與乘法','矩陣的高次方','反方陣與解矩陣方程式','一次聯立與高斯消去','平面線性變換']}
};
const labels={UNTESTED:'○ 尚未診斷',INSUFFICIENT_EVIDENCE:'… 證據不足',NEEDS_REVIEW:'! 需要複習',EMERGING:'△ 初步掌握',STABLE:'✓ 穩定掌握'};
const abilityNames={CONCEPT:'概念理解',RECOGNITION:'線索辨識',APPLICATION:'應用遷移'};
const priorityOrder={NEEDS_REVIEW:0,INSUFFICIENT_EVIDENCE:1,EMERGING:2,STABLE:3,UNTESTED:4};
const state={banks:{},selectedUnitId:'poly',session:null,learningCycleId:null,attempts:[],report:null};
const route=()=>location.hash.replace(/^#\//,'').split('/')[0]||'home';
const id=prefix=>`${prefix}-${crypto.randomUUID()}`;
const esc=value=>String(value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const itemUnit=itemId=>String(itemId||'').split('-')[0];
const sessionUnit=session=>itemUnit(session?.itemIds?.[0]);
const config=()=>units[state.selectedUnitId];
const bank=()=>state.banks[state.selectedUnitId];
const kpIds=unitId=>units[unitId].kp.map((_,index)=>`${unitId}:kp${index+1}`);
const kpName=kpId=>units[kpId.split(':')[0]]?.kp[Number(kpId.match(/kp(\d+)/)?.[1])-1]||kpId;
// 概念圖錨點對照。多數單元與概念圖核心概念同序（第 n 個核心概念 → #kpn），
// 但「排列組合」與「機率」是兩個診斷單元共用同一張概念圖頁（該頁共 6 個核心概念），
// 同序推導會指到錯的段落，故明列對照。
const kpAnchors={comb:['kp1','kp1','kp2','kp1'],probability:['kp3','kp5','kp4','kp6']};
// 次要參照：該核心概念另有一段落值得一併回讀（comb:kp4 的排容原理寫在核心概念 2）。
const kpAnchorExtra={'comb:kp4':'kp2'};
const kpAnchor=kpId=>{const[unitId,anchor]=kpId.split(':');return kpAnchors[unitId]?.[Number(anchor.slice(2))-1]??anchor;};
const kpLinks=kpId=>[kpAnchor(kpId),...(kpAnchorExtra[kpId]?[kpAnchorExtra[kpId]]:[])];
const priorityRecords=records=>records.filter(record=>['NEEDS_REVIEW','INSUFFICIENT_EVIDENCE'].includes(record.status)).sort((a,b)=>(priorityOrder[a.status]-priorityOrder[b.status])||(a.score??1)-(b.score??1)||(a.accuracy??1)-(b.accuracy??1)).slice(0,3);

function renderTex(tex,legacy=false){let source=String(tex);if(legacy)source=source.replaceAll('⋯','\\cdots ').replaceAll('∣','\\mid ').replace(/([A-Za-z0-9]+)\/\(([A-Za-z0-9]+)\)/g,'\\frac{$1}{$2}').replace(/([A-Za-z0-9]+)\/([A-Za-z0-9]+)/g,'\\frac{$1}{$2}');try{return window.katex.renderToString(source,{throwOnError:true,strict:'ignore',output:'htmlAndMathml'});}catch{return`<span class="math-fallback">${esc(source)}</span>`;}}
function formatMath(value){const text=String(value??'');if(!text.includes('[[')){let output='',position=0;for(const match of text.matchAll(/[A-Za-z0-9][A-Za-z0-9_()=+\-*/^⋯≠≤≥<>∣·,]*/g)){output+=esc(text.slice(position,match.index));output+=renderTex(match[0],true);position=match.index+match[0].length;}return output+esc(text.slice(position));}let output='',position=0;for(const match of text.matchAll(/\[\[([\s\S]*?)\]\]/g)){output+=esc(text.slice(position,match.index));output+=renderTex(match[1]);position=match.index+match[0].length;}return output+esc(text.slice(position));}
function setSave(text,error=false){saveState.textContent=text;saveState.style.background=error?'#7a1b1b':'';}
async function persist(store,value){setSave('儲存中…');try{await repository.put(store,value);setSave('已儲存在本機');}catch(error){setSave('無法儲存',true);throw error;}}
function usable(question){return question.publicationStatus==='APPROVED_PUBLISHED'||previewMode;}
function initialItems(unitId=state.selectedUnitId){return state.banks[unitId].items.filter(question=>question.purpose==='INITIAL'&&usable(question));}
function immediateItems(unitId=state.selectedUnitId){return state.banks[unitId].items.filter(question=>question.purpose==='IMMEDIATE_VARIANT'&&usable(question));}
function delayedItems(unitId=state.selectedUnitId){return state.banks[unitId].items.filter(question=>question.purpose==='DELAYED_RETEST'&&usable(question));}
function requiredImmediateItems(unitId=state.selectedUnitId){
  const records=state.report?.masteryRecords??[];
  return immediateItems(unitId).filter(question=>records.some(record=>record.kpId===question.primaryConceptId&&(record.weakAbilities??[]).includes(question.ability)));
}

async function activateUnit(unitId){state.selectedUnitId=unitId;state.report=null;state.learningCycleId=(await repository.get('meta',`current-learning-cycle-${unitId}`).catch(()=>null))?.value??null;state.attempts=state.learningCycleId?(await repository.getAll('attempts')).filter(attempt=>attempt.learningCycleId===state.learningCycleId):[];await repository.put('meta',{key:'selected-unit',value:unitId});}
async function load(){const entries=await Promise.all(Object.keys(units).map(async unitId=>{const response=await fetch(`../content/questions/${unitId}/questions.json`);if(!response.ok)throw new Error(`${units[unitId].name}題庫載入失敗`);return[unitId,await response.json()];}));state.banks=Object.fromEntries(entries);state.session=(await repository.get('meta','active-session').catch(()=>null))?.value??null;const stored=(await repository.get('meta','selected-unit').catch(()=>null))?.value,active=sessionUnit(state.session),preferred=units[active]?active:units[stored]?stored:'poly';await activateUnit(preferred);if(state.session?.learningCycleId){state.learningCycleId=state.session.learningCycleId;state.attempts=(await repository.getAll('attempts')).filter(attempt=>attempt.learningCycleId===state.learningCycleId);}addEventListener('hashchange',render);render();}
function nav(){document.querySelectorAll('[data-nav]').forEach(link=>link.toggleAttribute('aria-current',link.dataset.nav===route()));}
function shell(title,body,eyebrow=config()?.shortName||'十一單元整合'){main.innerHTML=`<p class="eyebrow">${esc(eyebrow)}｜十一單元整合</p><h1>${title}</h1>${body}`;main.focus();nav();}

async function startSession(unitId,kind='INITIAL'){
  await activateUnit(unitId);
  if(kind!=='INITIAL')await ensureReport();
  const now=new Date().toISOString(),learningCycleId=kind==='INITIAL'?id(`learning-${unitId}`):state.learningCycleId;
  if(!learningCycleId)throw new Error('尚未完成這個單元的初診');
  const existingCycle=(await repository.get('meta',`remediation-cycle-${learningCycleId}`).catch(()=>null))?.value??null;
  const scheduled=kind==='DELAYED_RETEST'?(await repository.getAll('remediation')).find(task=>task.learningCycleId===learningCycleId&&task.kpId.startsWith(`${unitId}:`)):null;
  const remediationCycleId=scheduled?.remediationCycleId??existingCycle??(kind==='INITIAL'?null:id('remediation'));
  state.learningCycleId=learningCycleId;
  if(kind==='INITIAL'){state.attempts=[];state.report=null;}
  const questions=kind==='INITIAL'?initialItems(unitId):kind==='IMMEDIATE_VARIANT'?requiredImmediateItems(unitId):delayedItems(unitId);
  if(!questions.length)throw new Error(kind==='IMMEDIATE_VARIANT'?'目前沒有需要立即變式驗證的弱能力':'目前沒有可用題目');
  state.session={schemaVersion:'1.1.0',sessionId:id('session'),learningCycleId,blueprintId:kind,status:'IN_PROGRESS',itemIds:questions.map(question=>question.itemId),startedAt:now,submittedAt:null};
  await Promise.all([persist('sessions',state.session),persist('meta',{key:'active-session',value:state.session}),persist('meta',{key:`current-learning-cycle-${unitId}`,value:learningCycleId}),persist('meta',{key:`item-started-at-${state.session.sessionId}`,value:now}),persist('meta',{key:`remediation-cycle-${learningCycleId}`,value:remediationCycleId})]);
  location.hash='#/session';render();
}

function home(){const active=state.session?.status==='IN_PROGRESS'?state.session:null,activeUnit=sessionUnit(active);const cards=Object.entries(units).map(([unitId,unit])=>{const initial=initialItems(unitId).length,immediate=immediateItems(unitId).length,delayed=delayedItems(unitId).length,disabled=active&&activeUnit!==unitId;const button=activeUnit===unitId?'<button class="primary-button continue-session">繼續作答</button>':initial?`<button class="primary-button start-unit" data-unit="${unitId}" ${disabled?'disabled':''}>開始${unit.shortName}診斷</button>`:'<p class="alert">題庫尚未出版。</p>';return`<section class="card unit-card"><h2>${unit.name}</h2><p>${initial} 題初診，約 ${unit.minutes} 分鐘；另備 ${immediate} 題立即變式與 ${delayed} 題延後確認。</p>${button}</section>`;}).join('');shell('選擇今天要診斷的單元',`<p class="lead">十一個單元共用五階段透明判讀；初診後依弱能力派送立即變式，第 3 天再做延後確認。</p>${active?`<div class="notice">你有一份「${units[activeUnit].name}」診斷尚未完成，請先繼續作答。</div>`:''}<div class="grid four">${cards}</div><div class="grid three info-grid"><section class="card warn"><h2>透明判讀</h2><p>概念、辨識與應用分開取證，不以總分掩蓋弱點。</p></section><section class="card good"><h2>兩次確認</h2><p>補強後先做立即變式，最快第 3 日再確認是否穩定。</p></section><section class="card"><h2>本機資料</h2><p>診斷紀錄只存在這個瀏覽器，可自行匯出、匯入或清除。</p></section></div>`,'複習後診斷');document.querySelectorAll('.start-unit').forEach(button=>button.onclick=()=>startSession(button.dataset.unit));document.querySelector('.continue-session')?.addEventListener('click',()=>{location.hash='#/session';});}

function session(){
  if(!state.session||state.session.status!=='IN_PROGRESS'){shell('目前沒有進行中的診斷','<div class="notice">請先選擇一個單元。</div><a class="button" href="#/home">回單元選擇</a>');return;}
  const unitId=sessionUnit(state.session);state.selectedUnitId=unitId;
  const sessionAttempts=state.attempts.filter(attempt=>attempt.sessionId===state.session.sessionId),index=sessionAttempts.length,itemId=state.session.itemIds[index],question=state.banks[unitId].items.find(item=>item.itemId===itemId);
  if(!question){shell('題目無法載入','<div class="alert">目前題庫與作答進度不一致，請返回單元選擇。</div>');return;}
  const number=index+1,total=state.session.itemIds.length,stage=state.session.blueprintId==='IMMEDIATE_VARIANT'?'立即變式':state.session.blueprintId==='DELAYED_RETEST'?'延後確認':'初次診斷';
  shell(`${stage}｜第 ${number} 題，共 ${total} 題`,`<section class="card question"><div class="progress" aria-label="作答進度 ${number}/${total}"><span style="width:${number/total*100}%"></span></div><p class="muted">${esc(kpName(question.primaryConceptId))} · ${esc(abilityNames[question.ability])}</p><h2>${formatMath(question.stem)}</h2><form id="answer-form"><div class="options">${question.options.map(option=>`<label class="option"><input required type="radio" name="answer" value="${option.id}"><span><strong>${option.id}．</strong>${formatMath(option.text)}</span></label>`).join('')}</div><fieldset class="confidence"><legend>你對答案的信心（選填）</legend>${[['LOW','低'],['MEDIUM','中'],['HIGH','高']].map(([value,text])=>`<label><input type="radio" name="confidence" value="${value}"> ${text}</label>`).join('')}</fieldset><div class="actions"><a class="button" href="#/home">暫停</a><button class="primary-button">${number===total?'完成並看報告':'送出並繼續'}</button></div></form></section>`);
  document.querySelector('#answer-form').onsubmit=async event=>{
    event.preventDefault();
    const form=new FormData(event.currentTarget),answer=form.get('answer'),now=new Date(),started=(await repository.get('meta',`item-started-at-${state.session.sessionId}`).catch(()=>null))?.value??state.session.startedAt,remediationCycleId=(await repository.get('meta',`remediation-cycle-${state.session.learningCycleId}`).catch(()=>null))?.value??null;
    const delayed=state.session.blueprintId==='DELAYED_RETEST',immediate=state.session.blueprintId==='IMMEDIATE_VARIANT';
    const attempt={schemaVersion:'1.1.0',attemptId:id('attempt'),sessionId:state.session.sessionId,learningCycleId:state.session.learningCycleId,remediationCycleId:delayed||immediate?remediationCycleId:null,itemId:question.itemId,itemVersion:question.itemVersion,attemptOrdinal:1,primaryConceptId:question.primaryConceptId,ability:question.ability,correct:question.answerSpec.correctOptionIds.includes(answer),hintUsed:false,submittedAt:now.toISOString(),elapsedSeconds:Math.max(0,Math.round((now-new Date(started))/1000)),timeRatio:question.expectedSeconds?Math.max(0,(now-new Date(started))/1000/question.expectedSeconds):null,confidence:form.get('confidence'),delayedDay:delayed?3:null,graded:true,source:delayed?'REMEDIATION_RETEST':immediate?'IMMEDIATE_VARIANT':'DIAGNOSTIC'};
    await persist('attempts',attempt);state.attempts.push(attempt);await persist('meta',{key:`item-started-at-${state.session.sessionId}`,value:now.toISOString()});
    if(index+1>=total){state.session.status='SUBMITTED';state.session.submittedAt=now.toISOString();await persist('sessions',state.session);await repository.put('meta',{key:'active-session',value:null});await buildReport(remediationCycleId);location.hash='#/report';}else render();
  };
}

async function buildReport(remediationCycleId=null){const unitId=state.selectedUnitId,now=new Date().toISOString(),questions=bank().items.map(question=>({itemId:question.itemId,publicationStatus:previewMode?'APPROVED_PUBLISHED':question.publicationStatus})),evaluation=diagnose({asOf:now,currentLearningCycleId:state.learningCycleId,currentRemediationCycleId:remediationCycleId,questions,attempts:state.attempts,conceptIds:kpIds(unitId)}),masteryRecords=evaluation.masteryRecords.map(record=>({schemaVersion:'1.1.0',kpId:record.kpId,learningCycleId:state.learningCycleId,status:record.status,algorithmVersion:'1.1.0',score:record.score,dimensions:record.dimensions,accuracy:record.accuracy,immediateAccuracy:record.immediateAccuracy,delayedAccuracy:record.delayedAccuracy,weakAbilities:record.weakAbilities,immediateComplete:record.immediateComplete,immediatePassedAbilities:record.immediatePassedAbilities,independentItemCount:record.independentItemCount,evidenceItemIds:[...new Set(state.attempts.filter(attempt=>attempt.primaryConceptId===record.kpId).map(attempt=>attempt.itemId))],excludedEvidence:record.excludedEvidence,reasonCodes:record.flags,updatedAt:now}));state.report={schemaVersion:'1.1.0',reportId:id('report'),learningCycleId:state.learningCycleId,algorithmVersion:'1.1.0',masteryRecords,excludedEvidence:masteryRecords.flatMap(record=>record.excludedEvidence),generatedAt:now};await persist('reports',state.report);for(const record of masteryRecords)await persist('mastery',record);}
async function ensureReport(){if(state.report?.learningCycleId===state.learningCycleId)return;const reports=await repository.getAll('reports').catch(()=>[]);state.report=reports.filter(report=>report.learningCycleId===state.learningCycleId&&report.masteryRecords?.every(record=>record.kpId.startsWith(`${state.selectedUnitId}:`))).at(-1)??null;}
async function report(){await ensureReport();if(!state.report){shell('尚無診斷報告','<div class="notice">完成這個單元的初診後，這裡會顯示各核心概念的證據與下一步。</div><a class="button" href="#/home">選擇單元</a>');return;}const records=state.report.masteryRecords,priorities=priorityRecords(records),priorityIndex=new Map(priorities.map((record,index)=>[record.kpId,index+1])),weak=records.filter(record=>['NEEDS_REVIEW','INSUFFICIENT_EVIDENCE'].includes(record.status)),stable=records.filter(record=>record.status==='STABLE').length,title=stable===records.length?'這個單元已達穩定掌握':weak.length?'先補需要複習的核心概念':'目前皆達初步掌握',prioritySummary=priorities.length?`<section class="card primary"><h2>前三項優先補強</h2><ol>${priorities.map(record=>`<li><strong>${esc(kpName(record.kpId))}</strong>｜${labels[record.status]}</li>`).join('')}</ol><p class="muted">依狀態、掌握分數與正確率排序；未檢測核心概念不列入弱點。</p></section>`:'<section class="card good"><h2>目前沒有優先補強項目</h2><p>已達穩定掌握的核心概念不再列入補強排序。</p></section>';shell(title,`<p class="lead">${stable===records.length?`已通過 ${records.length} 個核心概念的延後變式。`:weak.length?`有 ${weak.length} 個核心概念需要優先補強。`:'初步掌握不等於穩定掌握，請完成延後重測。'}</p>${prioritySummary}<div class="grid report-grid">${records.map(record=>`<section class="card">${priorityIndex.has(record.kpId)?`<span class="badge priority">優先 ${priorityIndex.get(record.kpId)}</span>`:''}<h2>${esc(kpName(record.kpId))}</h2><span class="badge ${record.status}">${labels[record.status]}</span><p>初測正確率：${record.accuracy===null?'尚無資料':Math.round(record.accuracy*100)+'%'}</p><details class="evidence"><summary>查看判讀依據</summary><p>獨立題目 ${record.independentItemCount} 題；排除 ${record.excludedEvidence.length} 筆；規則旗標：${record.reasonCodes.join('、')||'無'}。</p></details></section>`).join('')}</div><p><a class="button primary-button" href="#/remediation">前往補強與重測</a></p>`);}

async function remediation(){
  if(!state.learningCycleId){shell('尚未開始這個單元','<div class="notice">請先完成初診。</div><a class="button" href="#/home">選擇單元</a>');return;}
  await ensureReport();
  const tasks=(await repository.getAll('remediation').catch(()=>[])).filter(task=>task.learningCycleId===state.learningCycleId&&task.kpId.startsWith(`${state.selectedUnitId}:`));
  const due=tasks[0]?.dueAt?new Date(tasks[0].dueAt):null,ready=previewMode||(due&&Date.now()>=due.getTime());
  const required=requiredImmediateItems(),currentCycle=(await repository.get('meta',`remediation-cycle-${state.learningCycleId}`).catch(()=>null))?.value??null;
  const immediateAttempts=state.attempts.filter(attempt=>attempt.source==='IMMEDIATE_VARIANT'&&(!currentCycle||attempt.remediationCycleId===currentCycle));
  const missing=required.filter(question=>!immediateAttempts.some(attempt=>attempt.itemId===question.itemId));
  const immediatePassed=required.every(question=>immediateAttempts.some(attempt=>attempt.itemId===question.itemId&&attempt.correct&&!attempt.hintUsed));
  let button;
  if(tasks.length)button=previewMode?'<button class="primary-button" id="retest">開始預覽延後確認</button>':ready?'<button class="primary-button" id="retest">開始第 3 天延後確認</button>':`<button disabled>可確認日期：${due.toLocaleDateString('zh-TW')}</button>`;
  else if(missing.length)button=`<button class="primary-button" id="immediate">開始立即變式（${required.length} 題）</button>`;
  else if(required.length&&!immediatePassed)button='<button disabled>立即變式尚未通過，請重新補強</button>';
  else button='<button class="primary-button" id="schedule">排程第 3 天延後確認</button>';
  const stageText=tasks.length?'立即變式已完成；下一步以延後題確認是否能穩定提取。':required.length?`本輪有 ${required.length} 個弱能力，須先以同能力的新題立即驗證。`:'本輪沒有初診弱能力，可直接排程延後確認。';
  // 弱核心概念各自帶錨點連到概念圖對應段落，學生不必自己在整頁裡找。
  const weak=(state.report?.masteryRecords??[]).filter(record=>record.status==='NEEDS_REVIEW'||record.status==='EMERGING');
  const weakList=weak.length?`<section class="card"><h2>先回去讀這些核心概念</h2><ul>${weak.map(record=>{const links=kpLinks(record.kpId).map((anchor,index)=>`<a href="${mathMapRoot}${config().map}#${anchor}">${index?'延伸段落':'重點整理'}</a>`).join('、');return `<li><strong>${esc(kpName(record.kpId))}</strong>｜${labels[record.status]} → ${links}</li>`;}).join('')}</ul></section>`:'';
  shell('補強、立即變式與延後確認',`<p class="lead">先回到教材釐清觀念，再用不同題目確認能否獨立完成；立即答對不會直接標示穩定。</p><section class="card primary"><h2>${esc(config().name)}補強</h2><p>${stageText}</p><p>延後題池共 ${delayedItems().length} 題，涵蓋每個核心概念的概念、辨識與應用。</p><div class="data-actions"><a class="button" href="${mathMapRoot}${config().map}">開啟概念圖</a><a class="button" href="${mathMapRoot}exam/">開啟歷屆試題</a>${button}</div><p class="muted">正式模式須等到第 3 日；預覽模式只用來驗證完整閉環。</p></section>${weakList}`);
  document.querySelector('#immediate')?.addEventListener('click',()=>startSession(state.selectedUnitId,'IMMEDIATE_VARIANT'));
  document.querySelector('#retest')?.addEventListener('click',()=>startSession(state.selectedUnitId,'DELAYED_RETEST'));
  document.querySelector('#schedule')?.addEventListener('click',async()=>{const now=new Date(),dueAt=new Date(now.getTime()+3*86400000),remediationCycleId=currentCycle??id('remediation');await Promise.all(kpIds(state.selectedUnitId).map(kpId=>persist('remediation',{schemaVersion:'1.1.0',taskId:`task-${state.learningCycleId}-${kpId.replace(':','-')}`,learningCycleId:state.learningCycleId,kpId,remediationCycleId,status:'READY_FOR_RETEST',actions:kpLinks(kpId).map(anchor=>({kind:'CONCEPT_MAP',target:`${mathMapRoot}${config().map}#${anchor}`})),scheduledRetestDays:[3],createdAt:now.toISOString(),dueAt:dueAt.toISOString()})));await persist('meta',{key:`remediation-cycle-${state.learningCycleId}`,value:remediationCycleId});render();});
}

function dataPage(){shell('你的學習紀錄由你控制',`<p class="lead">資料只儲存在本機。匯出檔不包含姓名、學號或 Email。</p><section class="card"><div class="notice"><strong>備份保護：</strong>匯出檔包含六類公開資料的 SHA-256 完整性雜湊；匯入時會拒絕遭修改的檔案、內部畫面狀態及疑似個資欄位。</div><div class="data-actions"><button id="export">匯出資料</button><label class="button file-label">匯入資料<input id="import" type="file" accept="application/json"></label><button id="clear">清除診斷資料</button></div><div id="data-message" role="status" aria-live="polite"></div></section>`,'複習後診斷');const message=document.querySelector('#data-message');document.querySelector('#export').onclick=async()=>{const bundle=await repository.exportBundle(),blob=new Blob([JSON.stringify(bundle,null,2)],{type:'application/json'}),link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download=`mathmap-diagnostic-${new Date().toISOString().slice(0,10)}.json`;link.click();URL.revokeObjectURL(link.href);message.textContent='資料已匯出並附完整性雜湊。';};document.querySelector('#import').onchange=async event=>{try{const bundle=JSON.parse(await event.target.files[0].text()),result=await repository.importBundle(bundle,'merge');message.textContent=`完整性與隱私檢查通過；匯入 ${result.inserted} 筆。`;state.report=null;}catch(error){message.innerHTML=`<div class="alert">匯入失敗：${esc(error.message)}</div>`;}};document.querySelector('#clear').onclick=async()=>{if(!confirm('只會清除複習後診斷資料，不會刪除原有 MathMap 紀錄。確定清除？'))return;await repository.clearAll();state.session=null;state.learningCycleId=null;state.attempts=[];state.report=null;message.textContent='診斷資料已清除；原有 MathMap 紀錄未變動。';};}
async function render(){try{const current=route();if(current==='home')home();else if(current==='session')session();else if(current==='report')await report();else if(current==='remediation'||current==='retest')await remediation();else if(current==='data')dataPage();else location.hash='#/home';}catch(error){shell('目前無法顯示這一頁',`<div class="alert" role="alert">${esc(error.message)}</div><a class="button" href="#/home">回單元選擇</a>`);}}
document.querySelector('#mathmap-home').href=`${mathMapRoot}index.html`;
load().catch(error=>{main.innerHTML=`<div class="alert" role="alert">${esc(error.message)}。請由本機伺服器開啟試點。</div>`;});

