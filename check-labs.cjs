// Exercise the actual shipped script against fixed, independent acceptance cases.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
function runtime(lang) {
  const nodes = new Map();
  const el = id => {
    if (!nodes.has(id)) nodes.set(id, {value:'',textContent:'',dataset:{}});
    return nodes.get(id);
  };
  let click;
  const document = {documentElement:{lang},getElementById:el,addEventListener:(_,fn)=>{click=fn;}};
  vm.runInNewContext(fs.readFileSync(__dirname+'/labs.js','utf8'), {document,Math,Number,JSON,Object});
  const run = action => click({target:{closest:()=>({dataset:{action}})}});
  return {el,run};
}
let checked=0;
for (const lang of ['en','zh-CN']) {
  const {el,run}=runtime(lang);
  const set=(id,value)=>{el(id).value=value;};
  set('candidate-choice','A');set('candidate-check','missing');run('candidate');
  assert.equal(el('candidate-state').dataset.pass,'info');checked++;
  set('candidate-check','verified');run('candidate');
  assert.equal(el('candidate-state').dataset.pass,'true');checked++;
  for (const c of ['B','C']) {set('candidate-choice',c);run('candidate');assert.equal(el('candidate-state').dataset.pass,'false');checked++;}
  for (const [kind,claim,n] of [['reposts','geometry',1],['camera','geometry',2],['camera','event',2],['map','geometry',2],['map','event',1],['model','geometry',1]]) {
    set('lineage-choice',kind);set('lineage-claim',claim);run('lineage');assert.ok(el('lineage-state').textContent.includes(String(n)));checked++;
  }
  set('coordinate-first','30');set('coordinate-second','120');set('coordinate-order','latlon');set('coordinate-system','wgs');run('coordinate');
  assert.equal(el('coordinate-state').dataset.pass,'true');assert.ok(el('coordinate-output').textContent.includes('[120,30]'));assert.ok(el('coordinate-output').textContent.includes('0.00'));checked++;
  set('coordinate-order','lonlat');run('coordinate');assert.equal(el('coordinate-state').dataset.pass,'false');checked++;
  set('coordinate-first','45');set('coordinate-second','60');run('coordinate');const first=el('coordinate-output').textContent;assert.equal(el('coordinate-state').dataset.pass,'true');
  set('coordinate-order','latlon');run('coordinate');assert.equal(el('coordinate-state').dataset.pass,'true');assert.notEqual(el('coordinate-output').textContent,first);checked++;
  set('coordinate-system','unknown');run('coordinate');assert.equal(el('coordinate-state').dataset.pass,'info');assert.ok(!el('coordinate-output').textContent.includes('GeoJSON ='));checked++;
  set('coordinate-first','');run('coordinate');assert.equal(el('coordinate-state').dataset.pass,'false');checked++;
  set('coordinate-first','-90');set('coordinate-second','180');set('coordinate-system','wgs');run('coordinate');assert.equal(el('coordinate-state').dataset.pass,'true');assert.ok(!el('coordinate-output').textContent.includes('NaN'));checked++;
}
console.log(`PASS: ${checked} exercise acceptance cases in English and Chinese`);
