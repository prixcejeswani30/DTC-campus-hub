const reveal=()=>{document.querySelectorAll('.section,.orgcard,.newscard,.eventcard,.panel').forEach((el,i)=>{el.style.setProperty('--delay',(i%8)*50+'ms'); el.classList.add('reveal')})};
const closeMenu=()=>document.body.classList.remove('menuopen');
window.addEventListener('load',()=>{reveal();setTimeout(()=>document.querySelectorAll('.toast').forEach(t=>t.remove()),4500);document.querySelectorAll('.navlinks a,.navactions a').forEach(a=>a.addEventListener('click',closeMenu))});
