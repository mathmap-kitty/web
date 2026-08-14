import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

function repairMathMarkup(value) {
  const slash = String.fromCharCode(92);
  return String(value).replace(/\[\[([\s\S]*?)\]\]/g, (_, original) => {
    let tex = original.replaceAll("\f", `${slash}f`).replaceAll("\r", `${slash}r`);
    for (const command of ["frac", "cdot", "sqrt", "left", "right", "ge", "le", "ldots", "log"]) {
      const token = `${slash}${command}`;
      const marker = `@@${command.toUpperCase()}@@`;
      tex = tex.replaceAll(token, marker).replaceAll(command, token).replaceAll(marker, token);
    }
    return `[[${tex}]]`;
  });
}

function q(unit, kp, slot, ability, purpose, seconds, stem, options, correct, explanation, codes) {
  const ids = ["A", "B", "C", "D"];
  const distractorMap = {};
  ids.forEach((id, index) => {
    if (id !== correct && codes[index]) distractorMap[id] = codes[index];
  });
  return {
    schemaVersion: "1.0.0",
    itemId: `${unit}-kp${kp}-${slot}`,
    itemVersion: "1",
    primaryConceptId: `${unit}:kp${kp}`,
    ability,
    publicationStatus: "IN_REVIEW",
    purpose,
    expectedSeconds: seconds,
    stem: repairMathMarkup(stem),
    options: options.map((text, index) => ({ id: ids[index], text: repairMathMarkup(text) })),
    answerSpec: { kind: "singleChoice", correctOptionIds: [correct] },
    explanation: repairMathMarkup(explanation),
    distractorMap,
    source: { type: "PROJECT_ORIGINAL", reference: "Gate 4 教師核准題庫藍圖（2026-08-09）" }
  };
}

const L = {
  direction: "linecir.REPRESENTATION.001",
  vertical: "linecir.CONDITION.001",
  coordinate: "linecir.PROCEDURE.001",
  distance: "linecir.CALCULATION.001",
  circle: "linecir.CONCEPT.001",
  strategy: "linecir.STRATEGY.001",
  chord: "linecir.PROCEDURE.002",
  region: "linecir.REPRESENTATION.002",
  containment: "linecir.CONDITION.002"
};

const linecir = [
  q("linecir",1,"c1","CONCEPT","INITIAL",50,
    "直線 [[2x-3y+1=0]] 的一組方向向量為何？",
    ["[[(2,-3)]]","[[(3,2)]]","[[(2,3)]]","[[(-3,2)]]"],"B",
    "一般式 [[ax+by+c=0]] 的法向量可取 [[(a,b)]]，方向向量可取 [[(b,-a)]]。因此本題可取 [[(-3,-2)]] 或其倍數，選項中的 [[(3,2)]] 與它方向相反但平行，仍是方向向量。",
    [L.direction,null,L.direction,L.direction]),
  q("linecir",1,"r1","RECOGNITION","INITIAL",50,
    "已知直線通過 [[(2,-1)]]，斜率為 [[3]]。下列何式最適合作為第一步？",
    ["[[y+1=3(x-2)]]","[[y-1=3(x+2)]]","[[y+1=2(x-3)]]","[[3y=x-7]]"],"A",
    "已知一點與斜率時，直接使用點斜式 [[y-y_0=m(x-x_0)]]，代入 [[(x_0,y_0)=(2,-1)]] 得 [[y+1=3(x-2)]]。",
    [null,L.coordinate,L.coordinate,L.direction]),
  q("linecir",1,"a1","APPLICATION","INITIAL",75,
    "通過點 [[(1,2)]] 且垂直於直線 [[x=4]] 的直線方程式為何？",
    ["[[x=1]]","[[y=2]]","[[y=4]]","[[x+y=3]]"],"B",
    "[[x=4]] 是鉛直線，與它垂直的直線為水平線。通過 [[(1,2)]] 的水平線是 [[y=2]]。這個特例不適合硬套兩斜率乘積。",
    [L.vertical,null,L.vertical,L.vertical]),
  q("linecir",1,"r2","RECOGNITION","DELAYED_RETEST",65,
    "直線 [[3x+4y-7=0]] 的一組方向向量為何？",
    ["[[(3,4)]]","[[(4,-3)]]","[[(4,3)]]","[[(-3,4)]]"],"B",
    "法向量可取 [[(3,4)]]，與它垂直的方向向量可取 [[(4,-3)]]，因為內積 [[3\cdot4+4\cdot(-3)=0]]。",
    [L.direction,null,L.direction,L.direction]),
  q("linecir",1,"a2","APPLICATION","DELAYED_RETEST",85,
    "坐標平面上，到 [[x]] 軸與 [[y]] 軸距離相等的所有點所形成的圖形為何？",
    ["只有 [[y=x]]","只有 [[y=-x]]","[[y=x]] 或 [[y=-x]]","[[x^2+y^2=1]]"],"C",
    "點 [[(x,y)]] 到兩坐標軸的距離分別為 [[|y|]] 與 [[|x|]]。由 [[|x|=|y|]] 得 [[y=x]] 或 [[y=-x]]。",
    [L.direction,L.direction,null,L.direction]),

  q("linecir",2,"c1","CONCEPT","INITIAL",50,
    "兩點 [[A(1,2)]]、[[B(4,6)]] 的距離為何？",
    ["[[3]]","[[4]]","[[5]]","[[7]]"],"C",
    "水平差為 [[3]]、鉛直差為 [[4]]，因此 [[AB=\sqrt{3^2+4^2}=5]]。",
    [L.distance,L.distance,null,L.distance]),
  q("linecir",2,"r1","RECOGNITION","INITIAL",50,
    "線段端點為 [[A(-2,3)]]、[[B(4,-1)]]，其中點坐標為何？",
    ["[[(1,1)]]","[[(2,1)]]","[[(1,2)]]","[[(-1,1)]]"],"A",
    "中點的兩個坐標分別取平均：[[\left(\frac{-2+4}{2},\frac{3+(-1)}{2}\right)=(1,1)]]。",
    [null,L.coordinate,L.coordinate,L.coordinate]),
  q("linecir",2,"a1","APPLICATION","INITIAL",90,
    "三角形三頂點為 [[A(0,0)]]、[[B(6,0)]]、[[C(2,4)]]，其面積為何？",
    ["[[8]]","[[10]]","[[12]]","[[24]]"],"C",
    "以 [[AB]] 為底，底長為 [[6]]，點 [[C]] 到 [[x]] 軸的高為 [[4]]，所以面積為 [[\frac12\cdot6\cdot4=12]]。",
    [L.distance,L.distance,null,L.distance]),
  q("linecir",2,"r2","RECOGNITION","DELAYED_RETEST",70,
    "點 [[P(x,y)]] 到 [[A(-2,0)]] 與 [[B(4,0)]] 的距離相等，則 [[P]] 所在的軌跡為何？",
    ["[[x=-1]]","[[x=1]]","[[y=1]]","[[y=0]]"],"B",
    "等距軌跡是線段 [[AB]] 的中垂線。[[AB]] 中點的 [[x]] 坐標為 [[\frac{-2+4}{2}=1]]，故軌跡為 [[x=1]]。",
    [L.coordinate,null,L.coordinate,L.coordinate]),
  q("linecir",2,"a2","APPLICATION","DELAYED_RETEST",90,
    "點 [[P(t,2)]] 到點 [[A(1,0)]] 的距離為 [[\sqrt5]]，則 [[t]] 的所有可能值為何？",
    ["只有 [[0]]","只有 [[2]]","[[0]] 或 [[2]]","[[-1]] 或 [[3]]"],"C",
    "由距離公式，[[(t-1)^2+2^2=5]]，所以 [[(t-1)^2=1]]，得到 [[t=0]] 或 [[t=2]]。平方後要保留正負兩種可能。",
    [L.distance,L.distance,null,L.distance]),

  q("linecir",3,"c1","CONCEPT","INITIAL",45,
    "圓 [[(x+2)^2+(y-3)^2=25]] 的圓心與半徑為何？",
    ["圓心 [[(2,-3)]]，半徑 [[25]]","圓心 [[(-2,3)]]，半徑 [[5]]","圓心 [[(2,-3)]]，半徑 [[5]]","圓心 [[(-2,3)]]，半徑 [[25]]"],"B",
    "標準式是 [[(x-h)^2+(y-k)^2=r^2]]。因此圓心為 [[(-2,3)]]，半徑為 [[\sqrt{25}=5]]。",
    [L.circle,null,L.circle,L.circle]),
  q("linecir",3,"r1","RECOGNITION","INITIAL",75,
    "圓 [[x^2+y^2-6x+4y-12=0]] 的圓心與半徑為何？",
    ["圓心 [[(3,-2)]]，半徑 [[5]]","圓心 [[(-3,2)]]，半徑 [[5]]","圓心 [[(3,-2)]]，半徑 [[25]]","圓心 [[(-3,2)]]，半徑 [[25]]"],"A",
    "配方得 [[(x-3)^2+(y+2)^2=25]]，所以圓心為 [[(3,-2)]]，半徑為 [[5]]。",
    [null,L.circle,L.circle,L.circle]),
  q("linecir",3,"a1","APPLICATION","INITIAL",75,
    "對圓 [[(x-1)^2+(y-1)^2=9]]，點 [[P(4,1)]] 位於何處？",
    ["圓內","圓上","圓外","無法判定"],"B",
    "圓心為 [[(1,1)]]、半徑為 [[3]]。[[P]] 到圓心的距離為 [[3]]，等於半徑，所以 [[P]] 在圓上。",
    [L.circle,null,L.circle,L.circle]),
  q("linecir",3,"r2","RECOGNITION","DELAYED_RETEST",80,
    "方程 [[x^2+y^2+4x-8y+4=0]] 所表示的圓，其半徑為何？",
    ["[[2]]","[[4]]","[[8]]","[[16]]"],"B",
    "配方得 [[(x+2)^2+(y-4)^2=16]]，因此半徑為 [[4]]，不是 [[16]]。",
    [L.circle,null,L.circle,L.circle]),
  q("linecir",3,"a2","APPLICATION","DELAYED_RETEST",95,
    "圓的一條直徑端點為 [[A(-1,2)]]、[[B(5,2)]]，此圓的方程式為何？",
    ["[[(x-2)^2+(y-2)^2=9]]","[[(x+2)^2+(y-2)^2=9]]","[[(x-2)^2+(y+2)^2=36]]","[[(x-2)^2+(y-2)^2=36]]"],"A",
    "直徑中點為圓心 [[(2,2)]]，直徑長為 [[6]]，半徑為 [[3]]，故方程式是 [[(x-2)^2+(y-2)^2=9]]。",
    [null,L.circle,L.circle,L.circle]),

  q("linecir",4,"c1","CONCEPT","INITIAL",50,
    "圓 [[x^2+y^2=9]] 與直線 [[y=4]] 的位置關係為何？",
    ["相離","相切","相交於兩點","直線通過圓心"],"A",
    "圓心到直線 [[y=4]] 的距離為 [[4]]，半徑為 [[3]]。因 [[4>3]]，所以相離。",
    [null,L.strategy,L.strategy,L.strategy]),
  q("linecir",4,"r1","RECOGNITION","INITIAL",55,
    "圓 [[(x-1)^2+(y+2)^2=9]] 與直線 [[x=4]] 的位置關係為何？",
    ["相離","相切","相交於兩點","直線通過圓心"],"B",
    "圓心為 [[(1,-2)]]，到直線 [[x=4]] 的距離為 [[3]]，等於半徑 [[3]]，所以相切。",
    [L.strategy,null,L.strategy,L.strategy]),
  q("linecir",4,"a1","APPLICATION","INITIAL",90,
    "圓 [[x^2+y^2=25]] 被直線 [[y=3]] 截得的弦長為何？",
    ["[[4]]","[[5]]","[[8]]","[[10]]"],"C",
    "圓心到直線的距離為 [[3]]。半弦長為 [[\sqrt{5^2-3^2}=4]]，整條弦長為 [[2\cdot4=8]]。",
    [L.chord,L.chord,null,L.chord]),
  q("linecir",4,"r2","RECOGNITION","DELAYED_RETEST",85,
    "圓 [[x^2+y^2=10]] 在點 [[P(1,3)]] 的切線方程式為何？",
    ["[[x+3y=10]]","[[3x+y=10]]","[[x+3y=0]]","[[3x-y=0]]"],"A",
    "半徑 [[OP]] 的方向為 [[(1,3)]]，可作為切線的法向量。通過 [[P(1,3)]] 得 [[x+3y=10]]。",
    [null,L.direction,L.direction,L.direction]),
  q("linecir",4,"a2","APPLICATION","DELAYED_RETEST",100,
    "直線 [[y=k]] 與圓 [[x^2+y^2=4]] 恰有一個交點，則 [[k]] 的所有可能值為何？",
    ["只有 [[2]]","只有 [[-2]]","[[2]] 或 [[-2]]","[[-4]] 或 [[4]]"],"C",
    "圓心到直線 [[y=k]] 的距離為 [[|k|]]。恰有一個交點表示相切，所以 [[|k|=2]]，即 [[k=2]] 或 [[k=-2]]。",
    [L.strategy,L.strategy,null,L.strategy]),

  q("linecir",5,"c1","CONCEPT","INITIAL",50,
    "關於不等式 [[x+2y\le4]] 所表示的區域，下列何者正確？",
    ["包含原點，且包含邊界直線","包含原點，但不包含邊界直線","不包含原點，但包含邊界直線","不包含原點，也不包含邊界直線"],"A",
    "代入原點得 [[0\le4]]，所以包含原點；符號含等號，因此邊界直線也包含在區域內。",
    [null,L.region,L.region,L.region]),
  q("linecir",5,"r1","RECOGNITION","INITIAL",55,
    "不等式 [[y>2x+1]] 所表示的區域具有哪一項特徵？",
    ["包含原點，邊界為實線","包含原點，邊界為虛線","不包含原點，邊界為實線","不包含原點，邊界為虛線"],"D",
    "代入原點得到 [[0>1]]，不成立，所以不包含原點；嚴格不等式不含邊界，因此畫虛線。",
    [L.region,L.region,L.region,null]),
  q("linecir",5,"a1","APPLICATION","INITIAL",95,
    "區域 [[x\ge0]]、[[y\ge0]]、[[x+y\le6]] 的三個頂點為何？",
    ["[[(0,0),(6,0),(0,6)]]","[[(0,0),(3,0),(0,3)]]","[[(6,0),(0,6),(6,6)]]","[[(0,0),(6,6),(3,3)]]"],"A",
    "前兩式限制在第一象限，第三式的邊界與兩軸交於 [[(6,0)]]、[[(0,6)]]，再加上原點，共三個頂點。",
    [null,L.region,L.region,L.region]),
  q("linecir",5,"r2","RECOGNITION","DELAYED_RETEST",75,
    "某物品甲、乙的數量分別為 [[x]]、[[y]]，每件分別耗用 [[2]] 與 [[3]] 單位材料，總材料至多 [[12]] 單位。正確限制式為何？",
    ["[[2x+3y\ge12]]","[[2x+3y\le12]]","[[3x+2y\le12]]","[[2x+3y=12]]"],"B",
    "「至多」表示不超過，因此是 [[2x+3y\le12]]；數量題通常還需搭配 [[x\ge0]]、[[y\ge0]]。",
    [L.region,null,L.region,L.region]),
  q("linecir",5,"a2","APPLICATION","DELAYED_RETEST",120,
    "半徑為 [[1]] 的圓要完全落在正方形 [[0\le x\le6]]、[[0\le y\le4]] 內。若圓心為 [[(h,k)]]，其可行範圍為何？",
    ["[[0\le h\le6,\ 0\le k\le4]]","[[1\le h\le5,\ 1\le k\le3]]","[[-1\le h\le7,\ -1\le k\le5]]","[[1\le h\le6,\ 1\le k\le4]]"],"B",
    "整個圓都在正方形內，圓心到四邊的距離都至少為半徑 [[1]]，故 [[1\le h\le5]] 且 [[1\le k\le3]]。",
    [L.containment,null,L.containment,L.containment])
];

const S = {
  index: "seq.CONCEPT.001",
  middle: "seq.CONDITION.001",
  transform: "seq.REPRESENTATION.001",
  geometric: "seq.CONCEPT.002",
  model: "seq.MODELING.001",
  initial: "seq.CONDITION.002",
  recurrence: "seq.PROCEDURE.001",
  proof: "seq.STRATEGY.001",
  summation: "seq.PROCEDURE.002",
  period: "seq.RECOGNITION.001"
};

const seq = [
  q("seq",1,"c1","CONCEPT","INITIAL",45,
    "若 [[a,b,c]] 為等差數列中依序相鄰的三項，必定滿足哪一個關係？",
    ["[[a+b=c]]","[[2b=a+c]]","[[b^2=ac]]","[[b=a+c]]"],"B",
    "等差數列相鄰差相等：[[b-a=c-b]]，整理得 [[2b=a+c]]。",
    [S.middle,null,S.geometric,S.middle]),
  q("seq",1,"r1","RECOGNITION","INITIAL",55,
    "等差數列首項為 [[5]]，公差為 [[-2]]，其一般項為何？",
    ["[[a_n=5-2n]]","[[a_n=7-2n]]","[[a_n=5+2n]]","[[a_n=3-2n]]"],"B",
    "[[a_n=a_1+(n-1)d=5-2(n-1)=7-2n]]。常見錯誤是把公差算了 [[n]] 次。",
    [S.index,null,S.index,S.index]),
  q("seq",1,"a1","APPLICATION","INITIAL",70,
    "[[x,10,16]] 依序為等差數列的三項，則 [[x]] 為何？",
    ["[[2]]","[[4]]","[[6]]","[[8]]"],"B",
    "中項關係給出 [[2\cdot10=x+16]]，因此 [[x=4]]。",
    [S.middle,null,S.middle,S.middle]),
  q("seq",1,"r2","RECOGNITION","DELAYED_RETEST",65,
    "下列哪一個以正整數 [[n]] 為索引的數列一定是等差數列？",
    ["[[a_n=n^2]]","[[a_n=2^n]]","[[a_n=3n-1]]","[[a_n=\frac1n]]"],"C",
    "[[a_n=3n-1]] 的相鄰差恆為 [[3]]。其餘三個數列的相鄰差不固定。",
    [S.transform,S.transform,null,S.transform]),
  q("seq",1,"a2","APPLICATION","DELAYED_RETEST",100,
    "正數 [[a,b,c]] 依序成等差數列，且 [[\log a,\log b,\log c]] 也依序成等差數列。必有何結論？",
    ["[[a<b<c]]","[[a>b>c]]","[[a=b=c]]","[[ac=1]]"],"C",
    "兩組中項關係分別為 [[2b=a+c]] 與 [[b^2=ac]]。由算幾不等式，[[\frac{a+c}{2}\ge\sqrt{ac}]]；本題兩邊都等於 [[b]]，故等號成立，得到 [[a=b=c]]。",
    [S.middle,S.middle,null,S.middle]),

  q("seq",2,"c1","CONCEPT","INITIAL",50,
    "若非零數 [[a,b,c]] 依序為等比數列的三項，必定滿足哪一個關係？",
    ["[[2b=a+c]]","[[b^2=ac]]","[[a+b=c]]","[[b=a+c]]"],"B",
    "相鄰公比相等：[[\frac ba=\frac cb]]，交叉相乘得 [[b^2=ac]]。",
    [S.middle,null,S.geometric,S.geometric]),
  q("seq",2,"r1","RECOGNITION","INITIAL",65,
    "等比數列首項為 [[3]]，公比為 [[2]]，前 [[4]] 項和為何？",
    ["[[24]]","[[30]]","[[45]]","[[48]]"],"C",
    "前四項是 [[3,6,12,24]]，相加得 [[45]]；亦可用有限等比級數公式。",
    [S.geometric,S.geometric,null,S.geometric]),
  q("seq",2,"a1","APPLICATION","INITIAL",90,
    "等差數列 [[x_n=1+2(n-1)]]，令 [[y_n=3^{x_n}]]。則 [[y_n]] 的公比為何？",
    ["[[2]]","[[3]]","[[6]]","[[9]]"],"D",
    "相鄰輸入增加 [[2]]，所以 [[\frac{y_{n+1}}{y_n}=3^{x_{n+1}-x_n}=3^2=9]]。",
    [S.transform,S.transform,S.transform,null]),
  q("seq",2,"r2","RECOGNITION","DELAYED_RETEST",55,
    "等比數列 [[2,6,18]] 倒序寫成 [[18,6,2]] 後，新公比為何？",
    ["[[3]]","[[\frac13]]","[[-3]]","[[\frac12]]"],"B",
    "原公比為 [[3]]；順序反轉後，相鄰項的比變為原公比的倒數，即 [[\frac13]]。",
    [S.geometric,null,S.geometric,S.geometric]),
  q("seq",2,"a2","APPLICATION","DELAYED_RETEST",95,
    "數列 [[T_n=200+80\left(\frac12\right)^{n-1}]]，則 [[T_4]] 為何？",
    ["[[10]]","[[200]]","[[210]]","[[280]]"],"C",
    "[[T_4=200+80\left(\frac12\right)^3=200+10=210]]。每次減半的是超過 [[200]] 的變動量，不是整個 [[T_n]]。",
    [S.model,S.model,null,S.model]),

  q("seq",3,"c1","CONCEPT","INITIAL",45,
    "只知道遞迴式 [[a_{n+1}=2a_n]]，要唯一決定數列還缺少什麼？",
    ["公差","公比","至少一個初始值","前 [[n]] 項和"],"C",
    "遞迴式說明下一項如何由前一項產生，但仍需至少一個初始值，才能唯一決定整個數列。",
    [S.initial,S.initial,null,S.initial]),
  q("seq",3,"r1","RECOGNITION","INITIAL",60,
    "第一週存款為 [[200]] 元，以後每週比前一週多存 [[50]] 元。若第 [[n]] 週存款為 [[a_n]]，正確遞迴表示為何？",
    ["[[a_{n+1}=a_n+50,\ a_1=200]]","[[a_{n+1}=50a_n,\ a_1=200]]","[[a_{n+1}=a_n+200,\ a_1=50]]","[[a_n=200n+50]]"],"A",
    "「每週比前一週多 [[50]]」表示 [[a_{n+1}=a_n+50]]，並需保留初始條件 [[a_1=200]]。",
    [null,S.recurrence,S.recurrence,S.recurrence]),
  q("seq",3,"a1","APPLICATION","INITIAL",70,
    "數列滿足 [[a_1=1]]、[[a_{n+1}=2a_n+1]]，則 [[a_4]] 為何？",
    ["[[7]]","[[8]]","[[15]]","[[16]]"],"C",
    "逐項生成：[[a_2=3]]、[[a_3=7]]、[[a_4=15]]。",
    [S.recurrence,S.recurrence,null,S.recurrence]),
  q("seq",3,"r2","RECOGNITION","DELAYED_RETEST",95,
    "若 [[a_{n+1}=3a_n-4]]，定義下列哪一個新數列，可得到 [[b_{n+1}=3b_n]]？",
    ["[[b_n=a_n-2]]","[[b_n=a_n+2]]","[[b_n=2a_n]]","[[b_n=a_n-4]]"],"A",
    "令 [[b_n=a_n-2]]，則 [[b_{n+1}=a_{n+1}-2=3a_n-6=3(a_n-2)=3b_n]]。",
    [null,S.recurrence,S.recurrence,S.recurrence]),
  q("seq",3,"a2","APPLICATION","DELAYED_RETEST",110,
    "數列滿足 [[a_1=2]]、[[a_{n+1}=2a_n+1]]。下列哪一個一般項正確？",
    ["[[a_n=2^n]]","[[a_n=3\cdot2^{n-1}-1]]","[[a_n=2n]]","[[a_n=3^n-1]]"],"B",
    "令 [[b_n=a_n+1]]，則 [[b_{n+1}=2b_n]] 且 [[b_1=3]]，所以 [[b_n=3\cdot2^{n-1}]]，因此 [[a_n=3\cdot2^{n-1}-1]]。",
    [S.proof,null,S.proof,S.proof]),

  q("seq",4,"c1","CONCEPT","INITIAL",50,
    "[[\sum_{k=2}^{5}k]] 的值為何？",
    ["[[9]]","[[12]]","[[14]]","[[15]]"],"C",
    "展開為 [[2+3+4+5=14]]。上下限決定從第幾個索引加到第幾個索引。",
    [S.summation,S.summation,null,S.summation]),
  q("seq",4,"r1","RECOGNITION","INITIAL",70,
    "交錯和 [[1-2+3-4+\cdots+99-100]] 的值為何？",
    ["[[-100]]","[[-50]]","[[0]]","[[50]]"],"B",
    "每兩項配對：[[(1-2)+(3-4)+\cdots+(99-100)]]，共有 [[50]] 組，每組為 [[-1]]，所以和為 [[-50]]。",
    [S.summation,null,S.summation,S.summation]),
  q("seq",4,"a1","APPLICATION","INITIAL",80,
    "[[\sum_{k=1}^{10}(2k-1)]] 的值為何？",
    ["[[55]]","[[90]]","[[100]]","[[110]]"],"C",
    "這是前 [[10]] 個正奇數的和，等於 [[10^2=100]]；也可展開後用等差級數公式。",
    [S.summation,S.summation,null,S.summation]),
  q("seq",4,"r2","RECOGNITION","DELAYED_RETEST",75,
    "數列 [[2,-1,3,2,-1,3,\ldots]] 以三項為一週期，前 [[8]] 項和為何？",
    ["[[8]]","[[9]]","[[10]]","[[12]]"],"B",
    "一個完整週期的和為 [[2-1+3=4]]。前 [[8]] 項含兩個完整週期，再加 [[2,-1]]，所以總和為 [[2\cdot4+1=9]]。",
    [S.period,null,S.period,S.period]),
  q("seq",4,"a2","APPLICATION","DELAYED_RETEST",95,
    "[[\sum_{k=1}^{4}k(k+1)]] 的值為何？",
    ["[[20]]","[[30]]","[[40]]","[[50]]"],"C",
    "展開為 [[1\cdot2+2\cdot3+3\cdot4+4\cdot5=2+6+12+20=40]]。也可拆成 [[\sum k^2+\sum k]]。",
    [S.summation,S.summation,null,S.summation])
];

const rewrites = {
  "linecir-kp1-r2": {
    stem: "直線通過 [[A(1,2)]] 與 [[B(4,6)]]，下列何者是這條直線的一組方向向量？",
    options: ["[[(3,4)]]", "[[(4,3)]]", "[[(1,2)]]", "[[(5,8)]]"],
    correct: "A",
    explanation: "由 [[A]] 指向 [[B]] 的向量為 [[(4-1,6-2)=(3,4)]]，可作為直線的方向向量。",
    distractorMap: {}
  },
  "linecir-kp3-r1": {
    stem: "要由圓 [[x^2+y^2-6x+4y-12=0]] 找出圓心與半徑，最適合先做哪一步？",
    options: ["分別將 [[x^2-6x]] 與 [[y^2+4y]] 配方", "直接把 [[-6]] 與 [[4]] 當成圓心坐標", "先令 [[x=0]] 求 [[y]]", "先計算 [[x+y]] 的最大值"],
    correct: "A",
    explanation: "一般式要轉成圓心半徑式，應先把 [[x]] 與 [[y]] 的二次式分組配方；本題應處理 [[x^2-6x]] 與 [[y^2+4y]]。",
    distractorMap: {}
  },
  "linecir-kp3-r2": {
    stem: "已知圓的一條直徑端點為 [[A]]、[[B]]。要寫出圓方程式，最適合先使用哪一組工具？",
    options: ["用 [[AB]] 中點找圓心，再用 [[AB]] 長度的一半找半徑", "把 [[A]] 的坐標直接當圓心，把 [[AB]] 長度當半徑", "只求 [[AB]] 的斜率，不需要圓心", "只求 [[AB]] 中點，不需要半徑"],
    correct: "A",
    explanation: "直徑的中點就是圓心，而直徑長度的一半就是半徑；這兩個量齊備後才能寫標準式。",
    distractorMap: {}
  },
  "linecir-kp4-r2": {
    stem: "圓心為 [[O]]，[[P]] 為圓上一點。要作圓在 [[P]] 點的切線，首先應使用哪一個關係？",
    options: ["切線平行 [[OP]]", "切線垂直 [[OP]]", "切線必通過 [[O]]", "[[O]] 到切線的距離為 [[0]]"],
    correct: "B",
    explanation: "圓在 [[P]] 點的切線與半徑 [[OP]] 垂直。先確定這個方向關係，再利用通過 [[P]] 寫直線方程式。",
    distractorMap: { A: L.direction }
  },
  "seq-kp2-r1": {
    stem: "等比數列首項為 [[3]]、公比為 [[2]]。要計算前 [[4]] 項和 [[S_4]]，下列哪一個列式最直接？",
    options: ["[[3+2\cdot4]]", "[[3\cdot\frac{1-2^4}{1-2}]]", "[[3\cdot2^4]]", "[[\frac{3+24}{2}\cdot4]]"],
    correct: "B",
    explanation: "有限等比級數使用 [[S_n=a_1\frac{1-r^n}{1-r}]]，代入 [[a_1=3]]、[[r=2]]、[[n=4]]，即 [[3\cdot\frac{1-2^4}{1-2}]]。",
    distractorMap: {}
  },
  "seq-kp3-r2": {
    stem: "遞迴式 [[a_{n+1}=3a_n-4]] 的固定點 [[c]] 滿足 [[c=3c-4]]，故 [[c=2]]。要把遞迴轉成等比形式，應定義哪一個新數列？",
    options: ["[[b_n=a_n-2]]", "[[b_n=a_n+2]]", "[[b_n=2a_n]]", "[[b_n=a_n-4]]"],
    correct: "A",
    explanation: "以固定點平移，令 [[b_n=a_n-2]]，即可得到 [[b_{n+1}=a_{n+1}-2=3(a_n-2)=3b_n]]。",
    distractorMap: {}
  }
};

const mapOverrides = {
  "linecir-kp1-r1": {},
  "linecir-kp1-a1": { A: L.vertical },
  "linecir-kp1-a2": {},
  "linecir-kp2-r2": { A: L.coordinate },
  "linecir-kp3-a1": {},
  "linecir-kp4-a1": { A: L.chord },
  "linecir-kp3-a2": {},
  "linecir-kp4-a2": { D: L.circle },
  "seq-kp1-c1": { C: "seq.CONCEPT.003" },
  "seq-kp1-r1": { A: S.index },
  "seq-kp1-a1": {},
  "seq-kp1-r2": {},
  "seq-kp1-a2": {},
  "seq-kp2-c1": { A: "seq.CONCEPT.003" },
  "seq-kp2-a1": { A: S.transform },
  "seq-kp2-r2": { A: S.geometric },
  "seq-kp3-c1": {},
  "seq-kp3-a2": {},
  "seq-kp4-r2": { A: S.period }
};

for (const item of [...linecir, ...seq]) {
  const rewrite = rewrites[item.itemId];
  if (rewrite) {
    item.stem = repairMathMarkup(rewrite.stem);
    item.options = rewrite.options.map((text, index) => ({ id: ["A", "B", "C", "D"][index], text: repairMathMarkup(text) }));
    item.answerSpec.correctOptionIds = [rewrite.correct];
    item.explanation = repairMathMarkup(rewrite.explanation);
    item.distractorMap = rewrite.distractorMap;
  }
  if (Object.prototype.hasOwnProperty.call(mapOverrides, item.itemId)) item.distractorMap = mapOverrides[item.itemId];
  if (rewrite || Object.prototype.hasOwnProperty.call(mapOverrides, item.itemId)) item.itemVersion = "2";
  if (["linecir-kp3-r1", "linecir-kp3-r2", "linecir-kp3-a2"].includes(item.itemId)) item.itemVersion = "3";
}

for (const [unitId, items] of [["linecir", linecir], ["seq", seq]]) {
  const dir = path.join(here, unitId);
  fs.mkdirSync(dir, { recursive: true });
  const payload = { schemaVersion: "1.0.0", unitId, status: "IN_REVIEW", items };
  fs.writeFileSync(path.join(dir, "questions.json"), JSON.stringify(payload, null, 2) + "\n", "utf8");
  console.log(`${unitId}: ${items.length}`);
}
