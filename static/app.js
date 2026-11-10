const $ = (s) => document.querySelector(s);
let currentIntent = null;
let lastPrompt = "";
const history = [];
let liveMode = false;
const msg = $('#messages'), intro = $('#intro'), text = $('#message');
function node(tag, className, content) {const e=document.createElement(tag); if(className)e.className=className; if(content!==undefined)e.textContent=content;return e;}
function scroll(){const box=$('.conversation');box.scrollTop=box.scrollHeight;}
function addUser(content){const wrapper=node('div','message user'); wrapper.append(node('div','bubble',content));msg.append(wrapper);scroll();}
function addBot(payload, revised=false, originalPrompt=lastPrompt){
 const wrapper=node('div','message');wrapper.append(node('div','avatar','IR'));
 const bubble=node('div','bubble');
 if(revised)bubble.append(node('div','feedback','✓ Preferences updated — response regenerated'));
 bubble.append(node('div','label',revised?'REFINED SUGGESTION':(payload.engine === 'live-ai' ? 'ASSISTANT · LIVE AI' : 'ASSISTANT · SIMULATED RESPONSE')));
 bubble.append(node('h3','',payload.recommendation.title));
 bubble.append(node('p','',payload.recommendation.description));
 const list=node('ul');payload.recommendation.details.forEach(t=>list.append(node('li','',t)));bubble.append(list);
 if(payload.needs_clarification)bubble.append(node('div','notice','ⓘ This request needs clarification. You can correct the interpretation below.'));
 const btn=node('button','refine','✎  Refine your request');btn.type='button';btn.addEventListener('click',()=>togglePanel(bubble,btn,originalPrompt,payload.recommendation.description));bubble.append(btn);
 bubble.append(node('div','fine',payload.recommendation.disclaimer));wrapper.append(bubble);msg.append(wrapper);scroll();
}
async function togglePanel(bubble, btn, originalPrompt, answer) {
 const oldPanel=bubble.querySelector('.panel');
 if(oldPanel){oldPanel.remove();btn.textContent='✎  Refine your request';return;}
 btn.disabled=true;btn.textContent='Generating suggestions…';
 const panel=node('div','panel');
 panel.append(node('h4','','Clarify your intention'));
 const loading=node('p','','AI is analysing this request…');panel.append(loading);
 bubble.insertBefore(panel,btn.nextSibling);
 try{
   const result=await request('/api/clarify',{message:originalPrompt,answer,history:history.slice(-8)});
   loading.remove();panel.append(node('p','',result.question));
   const choices=node('div','choices');let selected=null;
   const apply=node('button','apply','Update response');apply.type='button';apply.disabled=true;
   result.options.forEach(option=>{
     const choice=node('button','',option);choice.type='button';
     choice.addEventListener('click',()=>{
       selected=option;
       choices.querySelectorAll('button').forEach(c=>c.classList.remove('active'));
       choice.classList.add('active');apply.disabled=false;
     });
     choices.append(choice);
   });
   panel.append(choices);
   apply.addEventListener('click',async()=>{
     if(!selected)return;
     apply.disabled=true;
     const clarified=`My earlier request was: ${originalPrompt}\nYour earlier response was: ${answer}\nI clarify my intended meaning as follows: ${selected}\nPlease revise the original answer accordingly, following this clarification.`;
     panel.remove();btn.textContent='✎  Refine your request';
     await submit(clarified);
   });
   panel.append(apply);btn.textContent='✕  Close refinement';
 }catch(error){loading.textContent='Could not generate suggestions: '+error.message;btn.textContent='✕  Close refinement';}
 finally{btn.disabled=false;scroll();}
}
async function request(path,body){const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const data=await r.json();if(!r.ok)throw Error(data.error||'Request failed');return data;}
async function submit(value){const prompt=value.trim();if(!prompt)return;intro.hidden=true;lastPrompt=prompt;addUser(prompt);text.value='';text.style.height='auto';try{const data=await request('/api/chat',{message:prompt,history:history.slice(-8)});currentIntent=data.intent;addBot(data,false,prompt);history.push({role:'user',content:prompt},{role:'assistant',content:data.recommendation.description});if(history.length>16)history.splice(0,history.length-16)}catch(e){msg.append(node('div','error',e.message));scroll()}}
$('#chatForm').addEventListener('submit',e=>{e.preventDefault();submit(text.value)});
text.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();$('#chatForm').requestSubmit()}});
text.addEventListener('input',()=>{text.style.height='auto';text.style.height=Math.min(text.scrollHeight,110)+'px'});
$('#reset').addEventListener('click',()=>{msg.replaceChildren();intro.hidden=false;currentIntent=null;lastPrompt='';history.length=0;text.value='';text.focus()});
document.querySelectorAll('[data-example]').forEach(btn=>btn.addEventListener('click',()=>submit(btn.dataset.example)));

fetch('/api/health').then(r=>r.json()).then(data=>{
 liveMode=data.mode==='live';
 const status=document.querySelector('.status');
 const foot=document.querySelector('.footerhint');
 const side=document.querySelector('.sidebottom');
 if(status) status.textContent=liveMode?'●  LIVE AI CONNECTED':'●  DEMO MODE';
 if(foot) foot.textContent=liveMode?'Live AI replies · Research prototype · Travel details are not verified.':'Demo replies · Configure a server-side API key for live AI.';
 if(side) side.textContent=liveMode?'● Live AI connected · v2.0':'● Rule-based demo · v2.0';
}).catch(()=>{});
