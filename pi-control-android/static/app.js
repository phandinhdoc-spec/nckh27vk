'use strict';
const $ = id => document.getElementById(id);
let connected=false, busy=false, demo=false, rows=[], lastSample=0;
function page(id){document.querySelectorAll('.page').forEach(e=>e.hidden=e.id!==id);document.querySelectorAll('nav button').forEach(e=>e.classList.toggle('selected',e.dataset.page===id));window.scrollTo(0,0);}
function showError(error){$('error').textContent=error.message||String(error);$('error').hidden=false;}
function node(tag,text,cls){const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;return e;}
let foregroundPending=false;
let transport=Promise.resolve();
const actionSelector='.actions button, #scan, #run, #record, #refresh, #connectForm button, #sensorRefresh, #fileList button';
function actionButtons(disabled){document.querySelectorAll(actionSelector).forEach(e=>e.disabled=disabled);}
async function request(route,data={},options={}){
  const background=options.background===true;
  if(!background&&foregroundPending)throw Error('Đang xử lý lệnh trước, vui lòng đợi hoàn tất.');
  if(!background){
    foregroundPending=true;
    actionButtons(true);
    $('busyOverlay').textContent=busy?'Lệnh đã xếp hàng · vẫn có thể chuyển tab':'Đang xử lý lệnh · vẫn có thể chuyển tab';
    $('busyOverlay').hidden=false;
  }
  const previous=transport;
  const job=(async()=>{
    await previous;
    busy=true;
    if(background)$('updated').textContent='Đang cập nhật…';
    else $('busyOverlay').textContent='Đang xử lý lệnh · vẫn có thể chuyển tab';
    try{
      const controller=new AbortController();
      const timer=setTimeout(()=>controller.abort(),route==='/api/snapshot'?65000:200000);
      try{
      const response=await fetch(route,{method:'POST',headers:{'Content-Type':'application/json','X-Pi-Control':'1'},body:JSON.stringify(data),signal:controller.signal});
      const result=await response.json();
      if(!response.ok)throw Error(result.error||'Lỗi kết nối');
      $('error').hidden=true;
      return result;
      }finally{clearTimeout(timer);}
    }finally{busy=false;}
  })();
  // Serialize SSH requests without disabling navigation or input fields.
  transport=job.catch(()=>{});
  try{return await job;}
  finally{if(!background){foregroundPending=false;$('busyOverlay').hidden=true;actionButtons(false);}}
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
  renderSensors(telemetry);

}
function renderServices(){const filter=$('search').value.toLowerCase();$('serviceList').replaceChildren();$('serviceCount').textContent=rows.length+' service';for(const row of rows){if(!row.join(' ').toLowerCase().includes(filter))continue;const [unit,state,sub,enabled,description]=row;const card=node('article','','service');const head=node('div','','row');head.append(node('h3',unit),node('span',state,'badge '+(state==='active'?'':state==='failed'?'failed':'inactive')));card.append(head,node('p',`${sub} · ${enabled}`),node('p',description));const actions=node('div','','actions');for(const [label,action] of [['Chạy','start'],['Dừng','stop'],['Restart','restart'],['Tự chạy','enable'],['Bỏ tự chạy','disable'],['Log','logs']]){const b=node('button',label,action==='stop'?'danger':'');b.disabled=foregroundPending;b.addEventListener('click',()=>service(action,unit));actions.append(b);}card.append(actions);$('serviceList').append(card);}}
async function refresh(){if(!connected||busy||foregroundPending)return;try{render(await request('/api/snapshot',{}, {background:true}));}catch(e){$('dot').classList.remove('online');$('status').textContent='Không đọc được Pi · dữ liệu cũ';$('sensorStatus').textContent='Chưa xác nhận mẫu mới — xem lỗi phía trên';showError(e);}}
async function service(action,unit){if(action!=='logs'&&!confirm(`${demo?'DEMO — ':''}${action}: ${unit}?`))return;try{const result=await request('/api/service',{action,unit});$('output').textContent=result.message;if(action==='logs')page('commands');else await refresh();}catch(e){showError(e);}}
$('settingsButton').onclick=()=>page('settings');document.querySelectorAll('nav button').forEach(e=>e.onclick=()=>page(e.dataset.page));$('search').oninput=renderServices;$('refresh').onclick=refresh;
$('connectForm').onsubmit=async event=>{event.preventDefault();if(!abandonEdit())return;try{clearWifi();clearEditor();$('fileList').textContent='Chọn thư mục để đọc từ Pi.';render(await request('/api/connect',Object.fromEntries(new FormData(event.target))));connected=true;page('overview');}catch(e){connected=false;$('dot').classList.remove('online');$('status').textContent='Kết nối thất bại';showError(e);}};
$('disconnect').onclick=async()=>{if(!abandonEdit())return;try{clearWifi();clearEditor();$('fileList').textContent='Đã ngắt kết nối';await request('/api/disconnect');connected=false;$('dot').classList.remove('online');$('status').textContent='Đã ngắt · dữ liệu cũ';$('sensorStatus').textContent='Đã ngắt kết nối — mẫu từ lần đọc trước';$('recordResult').hidden=true;$('player').pause();$('player').removeAttribute('src');}catch(e){showError(e);}};
$('scan').onclick=async()=>{try{const data=await request('/api/devices');$('deviceList').replaceChildren();for(const [name,value] of Object.entries(data)){$('deviceList').append(node('h3',name+(value.ok?'':' · không đọc được')),node('pre',value.text||'(không có dữ liệu)'));}}catch(e){showError(e);}};
$('run').onclick=async()=>{const command=$('command').value;if(!confirm('Chạy trên Pi với quyền SSH:\n'+command))return;try{const data=await request('/api/command',{command});$('output').textContent=data.message;}catch(e){$('output').textContent=e.message;showError(e);}};
$('record').onclick=async()=>{const seconds=Number($('seconds').value);if(!Number.isInteger(seconds)||seconds<1||seconds>120){showError(Error('Chọn thời lượng từ 1 đến 120 giây'));return;}if(!confirm(`Thu âm ${seconds} giây từ mic Pi?`))return;$('recordResult').hidden=true;$('player').pause();$('recordStatus').textContent=`Đang thu ${seconds} giây… giữ ứng dụng mở.`;try{const data=await request('/api/record',{device:$('audioDevice').value,seconds,rate:Number($('rate').value)});const url=data.url+'?t='+Date.now();$('player').src=url;$('download').href=url;$('recordResult').hidden=false;$('recordStatus').textContent='Thu xong. Bạn có thể nghe hoặc tải WAV.';}catch(e){$('recordStatus').textContent='Thu âm thất bại';showError(e);}};
setInterval(()=>{if(lastSample&&Date.now()-lastSample>15000){$('dot').classList.remove('online');$('status').textContent='Mẫu hệ thống đã cũ · '+Math.floor((Date.now()-lastSample)/1000)+' giây';}if(!document.hidden)refresh();},5000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh();});
(async()=>{try{const response=await fetch('/api/config');const data=await response.json();if(!response.ok)throw Error(data.error);demo=data.demo;$('demo').hidden=!demo;for(const [key,value] of Object.entries(data.config)){const field=$('connectForm').elements.namedItem(key);if(field)field.value=value;}if(data.hosted){$('settingsButton').hidden=true;$('settings').hidden=true;connected=true;page('overview');await refresh();}else if(demo){connected=true;await refresh();}else page('settings');}catch(e){showError(e);}})();

const measurementLabels={yaw:['Yaw','°'],pitch:['Pitch','°'],roll:['Roll','°'],yaw_deg:['Yaw','°'],pitch_deg:['Pitch','°'],roll_deg:['Roll','°'],pressure_pa:['Áp suất','Pa'],temperature_c:['Nhiệt độ','°C'],altitude_m:['Độ cao ước tính','m'],distance_mm:['Khoảng cách','mm'],distance_m:['Khoảng cách','m']};
function renderSensors(telemetry){
  const devices=telemetry.data?.devices||{};
  const metadata=telemetry.data?.sensor_info||{};
  if(!Object.keys(devices).length){$('sensors').append(node('div','Chưa có kết quả. Kiểm tra đường dẫn telemetry trong Cài đặt và bật xuất dữ liệu ở ứng dụng Pi.','panel'));return;}
  for(const [key,value] of Object.entries(devices)){
    const info=metadata[key]||{};
    const card=node('article','','panel');
    card.append(node('h3',info.name||({'imu':'Cảm biến góc (imu)','pressure':'Cảm biến áp suất (pressure)','distance':'Cảm biến khoảng cách (distance)'}[key]||key)));
    if(!info.name)card.append(node('p','Nguồn chưa cung cấp tên model; không suy đoán từ cổng kết nối.','hint'));
    if(info.connection)card.append(node('p',info.connection,'hint'));
    card.append(node('p',info.enabled===false?'Đang tắt trong cấu hình':value===null?'Chưa đọc được cảm biến':telemetry.state==='fresh'?'Có mẫu mới':'Mẫu cũ — không phải giá trị hiện tại', 'badge'));
    function values(v,path){
      if(v!==null&&typeof v==='object'){for(const [k,item] of Object.entries(v))values(item,path?path+'.'+k:k);}
      else {const [label,unit]=measurementLabels[path]||[path||'Kết quả',''];const line=node('div','','sensor');line.append(node('span',label),node('b',v===null?'Chưa có dữ liệu':String(v)+(unit?' '+unit:'')));card.append(line);}
    }
    values(value,'');$('sensors').append(card);
  }
}
$('sensorRefresh').onclick=refresh;
let openedFile=null, fileDirty=false, folderParent='/';
function abandonEdit(){return !fileDirty||confirm('Bạn có thay đổi chưa lưu. Bỏ phần đang sửa để mở mục khác?');}
function clearEditor(){openedFile=null;fileDirty=false;$('fileEditor').value='';$('fileEditorPanel').hidden=true;}
async function browseFiles(path){
  if(!abandonEdit())return;
  try{const data=await request('/api/files',{action:'list',path});clearEditor();$('filePath').value=data.path;folderParent=data.parent;$('uploadTarget').value=data.path.replace(/\/$/,'')+'/';$('fileList').replaceChildren();
    if(!data.entries.length)$('fileList').append(node('p','Thư mục trống'));
    for(const entry of data.entries){const button=node('button',(entry.kind==='directory'?'▸ ':entry.kind==='link'?'↗ ':'')+entry.name,'fileEntry');button.disabled=['special','unavailable'].includes(entry.kind);button.onclick=()=>{if(entry.kind==='directory')browseFiles(entry.path);else if(entry.kind==='link'){$('filePath').value=entry.path;}else openFile(entry.path);};$('fileList').append(button);}
  }catch(e){showError(e);}
}
async function openFile(path){
  if(!abandonEdit())return;
  try{const data=await request('/api/files',{action:'read',path});openedFile=data;fileDirty=false;$('filePath').value=data.path;$('editingPath').textContent=data.path;$('fileEditor').value=data.content;$('fileInfo').textContent=`${data.bytes} byte · quyền ${data.mode} · UID ${data.uid} / GID ${data.gid}`;$('fileSaveStatus').textContent='Đã mở file';$('fileEditorPanel').hidden=false;$('fileEditorPanel').scrollIntoView({behavior:'smooth'});}catch(e){showError(e);}
}
$('fileEditor').oninput=()=>{fileDirty=true;$('fileSaveStatus').textContent='Có thay đổi chưa lưu';};
$('browseFiles').onclick=()=>browseFiles($('filePath').value);
$('openFile').onclick=()=>openFile($('filePath').value);
$('parentFolder').onclick=()=>browseFiles(folderParent);
$('reloadFile').onclick=()=>{if(openedFile)openFile(openedFile.path);};
$('saveFile').onclick=async()=>{
  if(!openedFile)return;
  const editing=openedFile, editorContent=$('fileEditor').value;
  const crlf=editing.content.includes('\r\n')&&!editing.content.replaceAll('\r\n','').includes('\n');
  const content=crlf?editorContent.replaceAll('\n','\r\n'):editorContent;
  if(!confirm('Lưu thay đổi trên Pi bằng quyền SSH vào:\n'+editing.path+'\nBản sao file cũ sẽ được giữ lại.'))return;
  try{const result=await request('/api/files',{action:'write',path:editing.path,revision:editing.revision,content});
    if(openedFile===editing){openedFile.revision=result.revision;openedFile.content=content;fileDirty=$('fileEditor').value!==editorContent;$('fileSaveStatus').textContent=result.message+(result.backup?' · Bản sao: '+result.backup:'')+(fileDirty?' · Còn thay đổi mới chưa lưu':'');}
  }catch(e){showError(e);}
};
window.addEventListener('beforeunload',e=>{if(fileDirty){e.preventDefault();e.returnValue='';}});

let uploadPending=false;
function readUpload(file){return new Promise((resolve,reject)=>{
  const reader=new FileReader();
  reader.onload=()=>resolve(String(reader.result).split(',')[1]);
  reader.onerror=()=>reject(Error('Không đọc được file đã chọn trên điện thoại'));
  reader.onabort=()=>reject(Error('Đã hủy đọc file'));
  reader.readAsDataURL(file);
});}
$('uploadSource').onchange=()=>{
  const file=$('uploadSource').files[0];
  if(file){const path=$('uploadTarget').value;const slash=path.lastIndexOf('/');$('uploadTarget').value=path.slice(0,slash+1)+file.name;$('uploadStatus').textContent=`${file.name} · ${file.size} byte`;}
};
$('uploadFile').onclick=async()=>{
  if(uploadPending||foregroundPending)return;
  const file=$('uploadSource').files[0];
  if(!file){showError(Error('Chọn file trên điện thoại trước'));return;}
  if(file.size>16*1024*1024){showError(Error('File vượt giới hạn 16 MiB'));return;}
  let target=$('uploadTarget').value;
  if(target.endsWith('/'))target+=file.name;
  if(!target.startsWith('/')&&!target.startsWith('~/')){showError(Error('Nhập đường dẫn đầy đủ trên Pi, ví dụ /root/pi/app.py'));return;}
  if(fileDirty&&!confirm('Có file đang sửa chưa lưu. Tiếp tục tải lên? Phần đang sửa vẫn được giữ trong editor.'))return;
  uploadPending=true;
  // Keep the selected Pi stable while a file is read and its destination checked.
  $('connectForm').inert=true;
  try{
    $('uploadStatus').textContent='Đang đọc file trên điện thoại…';
    const content=await readUpload(file);
    $('uploadStatus').textContent='Đang kiểm tra file đích…';
    const checked=await request('/api/files',{action:'upload_check',path:target});
    const prompt=checked.exists?`File đã tồn tại (${checked.bytes} byte). Ghi đè ${checked.path}? Bản sao file cũ sẽ được giữ.`:`Tạo file mới ${checked.path} (${file.size} byte)?`;
    if(!confirm(prompt)){$('uploadStatus').textContent='Đã hủy, chưa thay đổi file trên Pi';return;}
    $('uploadStatus').textContent='Đang chuyển file qua SSH…';
    const result=await request('/api/files',{action:'upload',path:checked.path,revision:checked.revision,base64:content});
    $('uploadTarget').value=result.path;
    $('uploadStatus').textContent=`${result.message}: ${result.path} · ${result.bytes} byte`+(result.backup?' · Bản sao: '+result.backup:'');
    if(openedFile?.path===result.path)$('fileSaveStatus').textContent='File này vừa được tải lên. Mở lại bản trên Pi trước khi sửa tiếp; nội dung editor hiện tại vẫn được giữ.';
  }catch(e){$('uploadStatus').textContent='Chưa xác nhận tải lên thành công. '+e.message;showError(e);}
  finally{uploadPending=false;$('connectForm').inert=false;}
};

let wifiRevision=null;
function clearWifi(){wifiRevision=null;$('wifiPassword').value='';$('wifiSsid').value='';$('wifiReplace').checked=false;$('wifiNetworks').replaceChildren();$('wifiSummary').textContent='Chưa đọc cấu hình WiFi trên Pi.';$('wifiResult').hidden=true;}
function renderWifi(data){
  wifiRevision=data.revision;
  $('wifiSummary').textContent=`${data.networks.length}/${data.capacity} mạng đã lưu · Quốc gia ${data.country}`+(demo?' · DEMO':'');
  $('wifiNetworks').replaceChildren();
  for(const entry of data.networks){const row=node('div','','row');row.append(node('strong',entry.ssid),node('span',`Vị trí ${entry.slot} · ${entry.security}`));$('wifiNetworks').append(row);}
  if(!data.networks.length)$('wifiNetworks').append(node('p','Chưa có mạng đã lưu.'));
}
$('wifiRead').onclick=async()=>{try{renderWifi(await request('/api/wifi',{action:'status'}));}catch(e){wifiRevision=null;showError(e);}};
$('wifiSecurity').onchange=()=>{$('wifiPasswordLabel').hidden=$('wifiSecurity').value==='NONE';if($('wifiSecurity').value==='NONE')$('wifiPassword').value='';};
$('wifiForm').onsubmit=async event=>{
  event.preventDefault();
  if(!wifiRevision){showError(Error('Bấm Đọc mạng đã lưu trước khi thêm hoặc cập nhật WiFi.'));return;}
  const ssid=$('wifiSsid').value,security=$('wifiSecurity').value;
  if(!confirm(`Lưu mạng “${ssid}” vào Pi? Các mạng khác được giữ; chưa chuyển kết nối ngay.`))return;
  try{
    const data=await request('/api/wifi',{action:'save',ssid,security,password:$('wifiPassword').value,replace:$('wifiReplace').checked,revision:wifiRevision});
    renderWifi(data);$('wifiPassword').value='';$('wifiResult').hidden=false;
    $('wifiResult').textContent=data.message+' · '+data.saved_ssid+'. '+data.note+' Bản sao: '+data.backup;
  }catch(e){showError(e);}
};
$('wifiReload').onclick=async()=>{
  if(!wifiRevision){showError(Error('Đọc mạng đã lưu trước khi áp dụng.'));return;}
  if(!confirm('Nạp lại danh sách WiFi sau 3 giây? Pi có thể đổi mạng và mất SSH/Tailscale tạm thời.'))return;
  $('wifiResult').hidden=false;
  try{const data=await request('/api/wifi',{action:'reload',revision:wifiRevision,confirm:true});$('wifiResult').textContent=data.message;}
  catch(e){$('wifiResult').textContent='Chưa xác nhận được thao tác. Nếu Pi đổi mạng, đợi Tailscale kết nối lại rồi Làm mới.';showError(e);}
};
