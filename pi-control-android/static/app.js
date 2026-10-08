'use strict';
const $ = id => document.getElementById(id);
let connected=false, busy=false, demo=false, rows=[], lastSample=0;
function page(id){document.querySelectorAll('.page').forEach(e=>e.hidden=e.id!==id);document.querySelectorAll('nav button').forEach(e=>e.classList.toggle('selected',e.dataset.page===id));window.scrollTo(0,0);}
function showError(error){$('error').textContent=error.message||String(error);$('error').hidden=false;}
function node(tag,text,cls){const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;return e;}
async function request(route,data={}){
  if(busy)throw Error('Đang thực hiện thao tác khác');
  busy=true;$('busyOverlay').hidden=false;
  document.querySelectorAll('button').forEach(e=>e.disabled=true);
  try{const response=await fetch(route,{method:'POST',headers:{'Content-Type':'application/json','X-Pi-Control':'1'},body:JSON.stringify(data)});const result=await response.json();if(!response.ok)throw Error(result.error||'Lỗi kết nối');$('error').hidden=true;return result;}
  finally{busy=false;$('busyOverlay').hidden=true;document.querySelectorAll('button').forEach(e=>e.disabled=false);}
}
function render(data){
  lastSample=Date.now();$('host').textContent=data.hostname;$('dot').classList.add('online');$('status').textContent=demo?'DEMO · không có kết nối thật':'SSH đã phản hồi';
  const time=new Date().toLocaleTimeString('vi-VN');$('updated').textContent=time;
  for(const [id,key,suffix] of [['cpu','cpu_percent','%'],['ram','ram_percent','%'],['disk','disk_percent','%'],['temp','temperature_c',' °C']]){$(id).textContent=data[key]==null?'—':data[key]+suffix;}
  $('cpuBar').style.width=Math.max(0,Math.min(100,data.cpu_percent||0))+'%';$('ramBar').style.width=Math.max(0,Math.min(100,data.ram_percent||0))+'%';
  $('uptime').textContent=(data.uptime_seconds/3600).toFixed(1)+' giờ';rows=data.services.rows;$('activeCount').textContent=rows.filter(r=>r[1]==='active').length+' / '+rows.length;renderServices();
  if(data.services.errors.length)showError(new Error(data.services.errors.join('\n')));
  const telemetry=data.telemetry;
  $('sensorStatus').textContent=demo?'Mẫu minh họa — không phải cảm biến thật':({'fresh':'Mẫu mới','stale':'DỮ LIỆU CŨ','unavailable':'Chưa có telemetry'}[telemetry.state]+` · Tuổi mẫu: ${telemetry.age_seconds??'—'} giây`+(telemetry.error?' · '+telemetry.error:''));
  $('sensors').replaceChildren();
  function flatten(value,path){if(value!==null&&typeof value==='object'&&!Array.isArray(value)){for(const [key,item] of Object.entries(value))flatten(item,path?path+'.'+key:key);}else{const e=node('div','','sensor');e.append(node('span',path),node('b',value===null?'Chưa đọc được':String(value)));$('sensors').append(e);}}
  flatten(telemetry.data?.devices||{},'');
}
function renderServices(){const filter=$('search').value.toLowerCase();$('serviceList').replaceChildren();$('serviceCount').textContent=rows.length+' service';for(const row of rows){if(!row.join(' ').toLowerCase().includes(filter))continue;const [unit,state,sub,enabled,description]=row;const card=node('article','','service');const head=node('div','','row');head.append(node('h3',unit),node('span',state,'badge '+(state==='active'?'':state==='failed'?'failed':'inactive')));card.append(head,node('p',`${sub} · ${enabled}`),node('p',description));const actions=node('div','','actions');for(const [label,action] of [['Chạy','start'],['Dừng','stop'],['Restart','restart'],['Tự chạy','enable'],['Bỏ tự chạy','disable'],['Log','logs']]){const b=node('button',label,action==='stop'?'danger':'');b.addEventListener('click',()=>service(action,unit));actions.append(b);}card.append(actions);$('serviceList').append(card);}}
async function refresh(){if(!connected||busy)return;try{render(await request('/api/snapshot'));}catch(e){$('dot').classList.remove('online');$('status').textContent='Không đọc được Pi · dữ liệu cũ';$('sensorStatus').textContent='Chưa xác nhận mẫu mới — xem lỗi phía trên';showError(e);}}
async function service(action,unit){if(action!=='logs'&&!confirm(`${demo?'DEMO — ':''}${action}: ${unit}?`))return;try{const result=await request('/api/service',{action,unit});$('output').textContent=result.message;if(action==='logs')page('commands');else await refresh();}catch(e){showError(e);}}
$('settingsButton').onclick=()=>page('settings');document.querySelectorAll('nav button').forEach(e=>e.onclick=()=>page(e.dataset.page));$('search').oninput=renderServices;$('refresh').onclick=refresh;
$('connectForm').onsubmit=async event=>{event.preventDefault();try{render(await request('/api/connect',Object.fromEntries(new FormData(event.target))));connected=true;page('overview');}catch(e){connected=false;$('dot').classList.remove('online');$('status').textContent='Kết nối thất bại';showError(e);}};
$('disconnect').onclick=async()=>{try{await request('/api/disconnect');connected=false;$('dot').classList.remove('online');$('status').textContent='Đã ngắt · dữ liệu cũ';$('sensorStatus').textContent='Đã ngắt kết nối — mẫu từ lần đọc trước';$('recordResult').hidden=true;$('player').pause();$('player').removeAttribute('src');}catch(e){showError(e);}};
$('scan').onclick=async()=>{try{const data=await request('/api/devices');$('deviceList').replaceChildren();for(const [name,value] of Object.entries(data)){$('deviceList').append(node('h3',name+(value.ok?'':' · không đọc được')),node('pre',value.text||'(không có dữ liệu)'));}}catch(e){showError(e);}};
$('run').onclick=async()=>{const command=$('command').value;if(!confirm('Chạy trên Pi với quyền SSH:\n'+command))return;try{const data=await request('/api/command',{command});$('output').textContent=data.message;}catch(e){$('output').textContent=e.message;showError(e);}};
$('record').onclick=async()=>{const seconds=Number($('seconds').value);if(!Number.isInteger(seconds)||seconds<1||seconds>120){showError(Error('Chọn thời lượng từ 1 đến 120 giây'));return;}if(!confirm(`Thu âm ${seconds} giây từ mic Pi?`))return;$('recordResult').hidden=true;$('player').pause();$('recordStatus').textContent=`Đang thu ${seconds} giây… giữ Termux hoạt động.`;try{const data=await request('/api/record',{device:$('audioDevice').value,seconds,rate:Number($('rate').value)});const url=data.url+'?t='+Date.now();$('player').src=url;$('download').href=url;$('recordResult').hidden=false;$('recordStatus').textContent='Thu xong. Bạn có thể nghe hoặc tải WAV.';}catch(e){$('recordStatus').textContent='Thu âm thất bại';showError(e);}};
setInterval(()=>{if(lastSample&&Date.now()-lastSample>15000){$('dot').classList.remove('online');$('status').textContent='Mẫu hệ thống đã cũ · '+Math.floor((Date.now()-lastSample)/1000)+' giây';}if(!document.hidden)refresh();},5000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh();});
(async()=>{try{const response=await fetch('/api/config');const data=await response.json();if(!response.ok)throw Error(data.error);demo=data.demo;$('demo').hidden=!demo;for(const [key,value] of Object.entries(data.config)){const field=$('connectForm').elements.namedItem(key);if(field)field.value=value;}if(demo){connected=true;await refresh();}else page('settings');}catch(e){showError(e);}})();
