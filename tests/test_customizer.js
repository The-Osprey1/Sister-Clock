const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('firmware/index_html.h', 'utf8');
const begin = html.indexOf('      async function applyCustomizerSetting(');
const end = html.indexOf('      // Initialize the checkbox from cfg', begin);
assert(begin >= 0 && end > begin);
const elements = {};
for (const id of ['btn-12h','btn-24h','twelveHourToggle','showDayOfWeek','colonBlinkEnabled','btn-showdate-yes','btn-showdate-no','showDate','brightnessSlider','brightnessValue','mobile-bright-slider','mobile-bright-val', ...[0,1,2].map(i=>'clock-style-'+i), ...[0,1,2].map(i=>'alarm-style-'+i)]) {
  elements[id] = {checked:true,value:'7',textContent:'',active:false, classList: {toggle(_,state) { elements[id].active=state; }}};
}
let ok = true;
const toasts = [];
const ctx = {document:{getElementById:id=>elements[id]},fetch:async()=>({ok,status:ok?200:500}), showToast:s=>toasts.push(s), console:{error(){}},setTimeout,clearTimeout,encodeURIComponent};
vm.createContext(ctx);
vm.runInContext(html.slice(begin,end),ctx);
(async()=>{
 await ctx.chooseClockStyle(0);
 assert.equal(elements.showDayOfWeek.checked,false);
 assert.equal(elements.colonBlinkEnabled.checked,false);
 assert.equal(elements['clock-style-0'].active,true);
 ok=false;
 await ctx.chooseClockStyle(1);
 assert.equal(elements.showDayOfWeek.checked,false);
 assert.match(toasts.at(-1), /Could not change/);
 assert.equal(elements['clock-style-0'].active,true);
 await ctx.testAlarmNow();
 assert.match(toasts.at(-1), /Could not trigger/);
 console.log('Customizer behavior checks passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
