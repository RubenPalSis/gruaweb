// Mensaje de WhatsApp con contexto de la página y medición de clics (si hay GA4/gtag)
document.querySelectorAll('a[data-track]').forEach(function(a){
  a.addEventListener('click',function(){
    if(typeof gtag==='function'){gtag('event',a.dataset.track,{link_url:a.href,page_location:location.href});}
  });
});
var y=document.getElementById('year');if(y)y.textContent=new Date().getFullYear();
// Selector de idioma: se cierra al pulsar fuera o con Escape
var lang=document.querySelector('details.lang');
if(lang){
  document.addEventListener('click',function(e){if(lang.open&&!lang.contains(e.target))lang.open=false;});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')lang.open=false;});
}
// Aviso de cookies (Consent Mode de Google): se guarda la elección y se actualiza el consentimiento
var ck=document.getElementById('ck');
if(ck){
  var get=function(){try{return localStorage.getItem('ck')}catch(e){return null}};
  if(get()===null)ck.hidden=false;
  ck.querySelectorAll('[data-ck]').forEach(function(b){
    b.addEventListener('click',function(){
      var ok=b.dataset.ck==='1',v=ok?'granted':'denied';
      try{localStorage.setItem('ck',b.dataset.ck)}catch(e){}
      if(typeof gtag==='function')gtag('consent','update',{ad_storage:v,ad_user_data:v,ad_personalization:v,analytics_storage:v});
      ck.hidden=true;
    });
  });
  document.querySelectorAll('.ck-open').forEach(function(b){b.addEventListener('click',function(){ck.hidden=false;});});
}
