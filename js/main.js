// Mensaje de WhatsApp con contexto de la página y medición de clics (si hay GA4/gtag)
document.querySelectorAll('a[data-track]').forEach(function(a){
  a.addEventListener('click',function(){
    if(typeof gtag==='function'){gtag('event',a.dataset.track,{link_url:a.href,page_location:location.href});}
  });
});
var y=document.getElementById('year');if(y)y.textContent=new Date().getFullYear();
