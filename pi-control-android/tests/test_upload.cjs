const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(require('node:path').join(__dirname,'../static/app.js'),'utf8').split('let uploadPending=false;')[1];
const elements={uploadFile:{},uploadSource:{files:[{name:'a.bin',size:3}]},uploadTarget:{value:'/root/pi/'},uploadStatus:{},connectForm:{inert:false}};
let calls=[],exists=false,confirmed=true;
const context={$:id=>elements[id],foregroundPending:false,fileDirty:false,openedFile:null,
  confirm:()=>confirmed,showError:e=>{throw e;},FileReader:class{readAsDataURL(){this.result='data:application/octet-stream;base64,AP8B';this.onload();}},
  request:async(route,data)=>{calls.push(data);return data.action==='upload_check'?{path:'/root/pi/a.bin',exists,bytes:9,revision:exists?'old':null}:{path:'/root/pi/a.bin',bytes:3,message:'OK',backup:exists?'backup':null};}};
vm.createContext(context);vm.runInContext('let uploadPending=false;'+source,context);
(async()=>{
 await elements.uploadFile.onclick();
 assert.equal(calls.length,2);assert.equal(calls[1].base64,'AP8B');assert.equal(calls[1].revision,null);assert.equal(elements.connectForm.inert,false);
 calls=[];exists=true;confirmed=false;await elements.uploadFile.onclick();assert.equal(calls.length,1,'Cancel must never upload');
 calls=[];confirmed=true;await elements.uploadFile.onclick();assert.equal(calls[1].revision,'old');assert.match(elements.uploadStatus.textContent,/backup/);
 console.log('PASS: upload create, cancelled overwrite, confirmed overwrite, binary payload, connection form restored');
})().catch(e=>{console.error(e);process.exitCode=1;});
