document.documentElement.classList.add('js');
const language=document.documentElement.lang.startsWith('en')?'en':'es';
const menu=document.querySelector('#main-nav');
const toggle=document.querySelector('#menu-toggle');
function closeMenu(){if(!menu||!toggle)return;menu.dataset.open='false';toggle.setAttribute('aria-expanded','false');}
toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));menu.dataset.open=String(open);});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&toggle?.getAttribute('aria-expanded')==='true'){closeMenu();toggle.focus();}});
menu?.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
document.addEventListener('click',e=>{if(!e.target.closest('.header-inner'))closeMenu();});

document.querySelectorAll('[data-workflow-demo]').forEach(root=>{
 const choices=[...root.querySelectorAll('[data-flow-choice]')];
 const panels=[...root.querySelectorAll('[data-flow-panel]')];
 choices.forEach(choice=>{choice.disabled=false;choice.addEventListener('click',()=>{
  choices.forEach(button=>button.setAttribute('aria-pressed',String(button===choice)));
  panels.forEach(panel=>{const active=panel.dataset.flowPanel===choice.dataset.flowChoice;panel.hidden=!active;panel.classList.toggle('is-entering',active);});
 });});
});

document.querySelectorAll('[data-stage-explorer]').forEach(root=>{
 const tabs=[...root.querySelectorAll('[data-stage-choice]')];
 const panels=[...root.querySelectorAll('[data-stage-panel]')];
 const select=index=>{
  tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;});
  panels.forEach((panel,i)=>panel.hidden=i!==index);
 };
 tabs.forEach((tab,index)=>{
  tab.disabled=false;tab.tabIndex=index===0?0:-1;
  tab.addEventListener('click',()=>select(index));
  tab.addEventListener('keydown',event=>{
   const next=event.key==='ArrowRight'?(index+1)%tabs.length:event.key==='ArrowLeft'?(index+tabs.length-1)%tabs.length:event.key==='Home'?0:event.key==='End'?tabs.length-1:null;
   if(next===null)return;event.preventDefault();select(next);tabs[next].focus();
  });
 });
});

document.querySelectorAll('[data-report-demo]').forEach(root=>{
 const buttons=[...root.querySelectorAll('[data-basis]')];
 buttons.forEach(button=>{button.disabled=false;button.addEventListener('click',()=>{
  const stay=button.dataset.basis==='stay';
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  root.querySelector('[data-september]').textContent=language==='es'?(stay?'360 $':'1.200 $'):(stay?'$360':'$1,200');
  root.querySelector('[data-october]').textContent=language==='es'?(stay?'840 $':'0 $'):(stay?'$840':'$0');
  root.querySelectorAll('[data-stay-copy]').forEach(e=>e.hidden=!stay);
  root.querySelectorAll('[data-cash-copy]').forEach(e=>e.hidden=stay);
 });});
});

document.querySelectorAll('[data-record-demo]').forEach(root=>{
 const buttons=[...root.querySelectorAll('[data-match]')];
 buttons.forEach(button=>{button.disabled=false;button.addEventListener('click',()=>{
  const exact=button.dataset.match==='email';
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  root.querySelector('[data-record-email]').textContent=exact?'contacto@ejemplo.test':'otro@ejemplo.test';
  root.querySelector('[data-exact-answer]').hidden=!exact;
  root.querySelector('[data-name-answer]').hidden=exact;
 });});
});

const form=document.querySelector('#contact-form');
if(form){
 const context=new URLSearchParams(location.search).get('proceso');
 const contexts={
  informes:language==='es'?'Quiero revisar dos informes que no coinciden.':'I would like to review two reports that do not agree.',
  crm:language==='es'?'Quiero mejorar cómo importamos y mantenemos los datos del CRM.':'I would like to improve how we import and maintain CRM data.',
  documentos:language==='es'?'Quiero revisar cómo recibimos, comprobamos y registramos documentos.':'I would like to review how we receive, check and record documents.',
  asistentes:language==='es'?'Me interesa un asistente de IA conectado a la información y los procesos de mi empresa.':'I am interested in an AI assistant connected to my company’s information and processes.',
  automatizacion:language==='es'?'Quiero aplicar IA para automatizar un proceso de mi empresa.':'I would like to apply AI to automate a process in my business.',
  integraciones:language==='es'?'Quiero conectar nuestras herramientas y mejorar cómo se mueven los datos entre ellas.':'I would like to connect our tools and improve how data moves between them.',
  proyecto:language==='es'?'Tengo un proceso concreto que me gustaría mejorar.':'I have a specific process I would like to improve.',
  continuo:language==='es'?'Me interesa una colaboración continua para mejorar nuestras operaciones.':'I am interested in ongoing support to improve our operations.'
 };
 if(context&&contexts[context]){form.elements.challenge.value=contexts[context];form.elements.source_page.value=context;document.querySelectorAll('.language a').forEach(a=>{const target=new URL(a.href);target.searchParams.set('proceso',context);a.href=target.pathname+target.search;});}
 form.addEventListener('submit',async event=>{
  event.preventDefault();if(!form.reportValidity())return;
  const button=form.querySelector('[type=submit]');const status=document.querySelector('#form-status');const label=button.textContent;
  button.disabled=true;button.textContent=language==='es'?'Enviando…':'Sending…';status.textContent='';status.removeAttribute('data-state');
  try{
   const response=await fetch(form.action,{method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});
   if(!response.ok)throw new Error('submission_failed');
   status.dataset.state='success';status.setAttribute('role','status');
   status.textContent=language==='es'?'Tu solicitud se ha enviado correctamente. Te responderemos al email que has indicado.':'Your request has been sent successfully. We will reply to the email address you provided.';
   form.reset();
  }catch{
   status.dataset.state='error';status.setAttribute('role','alert');
   status.textContent=language==='es'?'No hemos podido confirmar el envío. Conservamos el texto para que puedas reintentarlo. También puedes escribir a hello@almaintel.com.':'We could not confirm delivery. Your text is still here so you can try again. You can also email hello@almaintel.com.';
  }finally{button.disabled=false;button.textContent=label;}
 });
}
