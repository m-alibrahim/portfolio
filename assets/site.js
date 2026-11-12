(function(){
  var root=document.documentElement,btn=document.querySelector('.theme');
  if(btn)btn.addEventListener('click',function(){var t=root.dataset.theme==='dark'?'light':'dark';root.dataset.theme=t;try{localStorage.setItem('theme',t)}catch(e){}});
  var glow=document.querySelector('.glow');
  if(glow&&matchMedia('(pointer:fine)').matches&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
    addEventListener('pointermove',function(ev){glow.classList.add('on');glow.style.setProperty('--mx',ev.clientX+'px');glow.style.setProperty('--my',ev.clientY+'px')},{passive:true});
  }
  var links=[].slice.call(document.querySelectorAll('.intro nav a'));
  if(links.length&&'IntersectionObserver' in window){
    var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){links.forEach(function(a){a.classList.remove('on')});var a=map[en.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-30% 0px -60% 0px'});
    document.querySelectorAll('main section[id]').forEach(function(s){io.observe(s)});
  }
})();
