const DB_NAME='mathmap-diagnostic', DB_VERSION=1;
const STORES=['sessions','attempts','mastery','risks','remediation','reports','meta'];
const EXPORT_STORES=['sessions','attempts','mastery','risks','remediation','reports'];
const FORBIDDEN_KEY=/(^|_)(name|student_?id|school|class|email|e-?mail|phone|telephone)($|_)|姓名|學號|學校|班級|電子郵件|信箱|電話/i;
const EMAIL_VALUE=/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i;

function assertPublicBundle(bundle){
  if(bundle?.schemaVersion!=='1.0.0'||!bundle.payload)throw new Error('不支援的匯入格式');
  const keys=Object.keys(bundle.payload).sort(),expected=[...EXPORT_STORES].sort();
  if(JSON.stringify(keys)!==JSON.stringify(expected))throw new Error('匯入檔欄位不符合公開備份契約');
  for(const store of EXPORT_STORES)if(!Array.isArray(bundle.payload[store]))throw new Error(`匯入檔缺少 ${store} 陣列`);
  const scan=(value,path='payload')=>{
    if(typeof value==='string'&&EMAIL_VALUE.test(value))throw new Error(`匯入檔含疑似 Email：${path}`);
    if(!value||typeof value!=='object')return;
    for(const [key,child] of Object.entries(value)){
      if(FORBIDDEN_KEY.test(key))throw new Error(`匯入檔含禁止的個資欄位：${key}`);
      scan(child,`${path}.${key}`);
    }
  };
  scan(bundle.payload);
}
async function sha256(value){
  const bytes=new TextEncoder().encode(JSON.stringify(value)),digest=await crypto.subtle.digest('SHA-256',bytes);
  return [...new Uint8Array(digest)].map(byte=>byte.toString(16).padStart(2,'0')).join('');
}
async function verifyHashes(bundle){
  const hashes=bundle.hashes??{},required=bundle.algorithmVersion==='1.1.0';
  for(const store of EXPORT_STORES){
    if(!hashes[store]){if(required)throw new Error(`備份檔缺少 ${store} 完整性雜湊`);continue;}
    if(hashes[store]!==await sha256(bundle.payload[store]))throw new Error(`備份檔 ${store} 完整性檢查失敗`);
  }
}

function openDb(){
  return new Promise((resolve,reject)=>{
    const request=indexedDB.open(DB_NAME,DB_VERSION);
    request.onupgradeneeded=()=>{ for(const name of STORES) if(!request.result.objectStoreNames.contains(name)) request.result.createObjectStore(name,{keyPath:name==='meta'?'key':name==='attempts'?'attemptId':name==='sessions'?'sessionId':name==='mastery'?'kpId':name==='risks'?'riskId':name==='remediation'?'taskId':'reportId'}); };
    request.onsuccess=()=>resolve(request.result); request.onerror=()=>reject(request.error);
  });
}
async function tx(store,mode,action){
  const db=await openDb();
  return new Promise((resolve,reject)=>{const transaction=db.transaction(store,mode), objectStore=transaction.objectStore(store), request=action(objectStore); request.onsuccess=()=>resolve(request.result); request.onerror=()=>reject(request.error); transaction.oncomplete=()=>db.close();});
}
export const repository={
  get:(store,key)=>tx(store,'readonly',s=>s.get(key)),
  getAll:(store)=>tx(store,'readonly',s=>s.getAll()),
  put:(store,value)=>tx(store,'readwrite',s=>s.put(value)),
  delete:(store,key)=>tx(store,'readwrite',s=>s.delete(key)),
  async clearAll(){const db=await openDb(); await Promise.all(STORES.map(store=>new Promise((resolve,reject)=>{const t=db.transaction(store,'readwrite'),r=t.objectStore(store).clear();r.onsuccess=()=>resolve();r.onerror=()=>reject(r.error)}))); db.close(); for(const key of Object.keys(localStorage)) if(key.startsWith('mmdx:')) localStorage.removeItem(key);},
  async exportBundle(){const payload={};for(const store of EXPORT_STORES)payload[store]=await this.getAll(store);const hashes={};for(const store of EXPORT_STORES)hashes[store]=await sha256(payload[store]);return {schemaVersion:'1.0.0',algorithmVersion:'1.1.0',exportedAt:new Date().toISOString(),payload,hashes};},
  async importBundle(bundle,mode='merge'){assertPublicBundle(bundle);await verifyHashes(bundle);if(mode==='replace')await this.clearAll();let inserted=0;for(const store of EXPORT_STORES){for(const row of bundle.payload[store]){await this.put(store,row);inserted++;}}return{inserted,skipped:0,warnings:[]};}
};
