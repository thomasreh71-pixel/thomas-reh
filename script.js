if('scrollRestoration' in history){history.scrollRestoration='manual';}
window.addEventListener('pageshow',()=>{if(!location.hash){requestAnimationFrame(()=>window.scrollTo(0,0));setTimeout(()=>window.scrollTo(0,0),80);}});
const toggle=document.querySelector('.menu-toggle');const nav=document.querySelector('.mainnav');if(toggle&&nav){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');}));}const year=document.getElementById('year');if(year)year.textContent=new Date().getFullYear();
const autoVideo=document.querySelector('.video-frame iframe[data-src]');if(autoVideo){const loadVideo=()=>{if(autoVideo.src==='about:blank'||autoVideo.src===''){autoVideo.src=autoVideo.dataset.src;}};if('IntersectionObserver'in window){const io=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){loadVideo();io.disconnect();}});},{rootMargin:'200px 0px'});io.observe(autoVideo);}else{loadVideo();}}

/* Gemeinsame Polarsteps-Links und Icons auf allen Seiten. */
(() => {
  const url='https://www.polarsteps.com/CamperRuby';
  const icon='polarsteps-icon.svg';
  const makeLink=(className,text,accessibleName)=>{
    const a=document.createElement('a');
    a.className=className;a.href=url;a.target='_blank';a.rel='noopener';
    if(accessibleName)a.setAttribute('aria-label',accessibleName);
    const img=document.createElement('img');img.src=icon;img.alt='';img.setAttribute('aria-hidden','true');
    a.append(img,document.createTextNode(text));
    return a;
  };
  document.querySelector('.site-header .nav-wrap')?.append(makeLink('polarsteps-header','Polarsteps','Meine Reisen auf Polarsteps'));
  document.querySelector('.site-footer .wrap')?.append(makeLink('polarsteps-footer','Polarsteps'));
  const aboutLink=document.querySelector('.prose a[href="'+url+'"]');
  if(aboutLink){const img=document.createElement('img');img.src=icon;img.alt='';img.setAttribute('aria-hidden','true');aboutLink.prepend(img);}
  const ico=document.createElement('link');ico.rel='icon';ico.type='image/x-icon';ico.href='favicon.ico?v=6';document.head.append(ico);
  const apple=document.createElement('link');apple.rel='apple-touch-icon';apple.href='apple-touch-icon.png?v=6';document.head.append(apple);
})();
