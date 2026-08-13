// Scroll reveals
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

// RSVP demo submit
const form=document.getElementById('rsvpForm');
form.addEventListener('submit',e=>{
  e.preventDefault();
  const name=document.getElementById('f-name'),email=document.getElementById('f-email');
  if(!name.value.trim()||!email.value.trim()||!email.checkValidity()){
    (!name.value.trim()?name:email).focus();
    return;
  }
  form.classList.add('sent');
});
