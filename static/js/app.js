const reveal=()=>{document.querySelectorAll('.section,.orgcard,.newscard,.eventcard,.panel').forEach((el,i)=>{el.style.setProperty('--delay',(i%8)*50+'ms'); el.classList.add('reveal')})};
window.addEventListener('load',()=>{reveal();setTimeout(()=>document.querySelectorAll('.toast').forEach(t=>t.remove()),4500)});
