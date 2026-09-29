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
  const headerWrap=document.querySelector('.site-header .nav-wrap');
  if(headerWrap){
    const links=document.createElement('div');links.className='header-social-links';
    links.append(makeLink('polarsteps-header','Polarsteps','Meine Reisen auf Polarsteps'));
    const whatsapp=document.createElement('a');whatsapp.className='whatsapp-header';
    whatsapp.href='https://wa.me/WhatsThomasRehApp';whatsapp.target='_blank';whatsapp.rel='noopener';
    whatsapp.textContent='WhatsApp';whatsapp.setAttribute('aria-label','Thomas über WhatsApp kontaktieren');
    links.append(whatsapp);headerWrap.append(links);
  }
  const footerWrap=document.querySelector('.site-footer .wrap');
  if(footerWrap){
    const links=document.createElement('div');links.className='footer-social-links';
    links.append(makeLink('polarsteps-footer','Polarsteps'));
    const whatsapp=document.createElement('a');whatsapp.className='whatsapp-footer';
    whatsapp.href='https://wa.me/WhatsThomasRehApp';whatsapp.target='_blank';whatsapp.rel='noopener';
    whatsapp.textContent='WhatsApp';whatsapp.setAttribute('aria-label','Thomas über WhatsApp kontaktieren');
    links.append(whatsapp);footerWrap.append(links);
  }
  const aboutActions=document.querySelector('.prose .youtube-links');
  if(aboutActions){
    const whatsapp=document.createElement('a');whatsapp.className='btn btn-secondary whatsapp-about';
    whatsapp.href='https://wa.me/WhatsThomasRehApp';whatsapp.target='_blank';whatsapp.rel='noopener';
    whatsapp.textContent='Schreib mir auf WhatsApp →';
    aboutActions.append(whatsapp);
  }
  const aboutLink=document.querySelector('.prose a[href="'+url+'"]');
  if(aboutLink){const img=document.createElement('img');img.src=icon;img.alt='';img.setAttribute('aria-hidden','true');aboutLink.prepend(img);}
  const ico=document.createElement('link');ico.rel='icon';ico.type='image/x-icon';ico.href='favicon.ico?v=6';document.head.append(ico);
  const apple=document.createElement('link');apple.rel='apple-touch-icon';apple.href='apple-touch-icon.png?v=6';document.head.append(apple);
})();
