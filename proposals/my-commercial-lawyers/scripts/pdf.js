const {chromium}=require(process.env.PW);
(async()=>{const [inp,out]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:1810}});
await p.goto('file://'+inp,{waitUntil:'networkidle'});await p.waitForTimeout(2500);
await p.screenshot({path:out+'.png',fullPage:true});
await p.emulateMedia({media:'screen'});
await p.pdf({path:out+'.pdf',printBackground:true,width:'1280px',height:'1810px',margin:{top:'0',right:'0',bottom:'0',left:'0'},scale:1});
console.log('h',await p.evaluate(()=>document.body.scrollHeight));await b.close()})();
