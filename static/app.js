document.addEventListener('click', (event) => {
  const heart = event.target.closest('.heart');
  if (heart) { heart.classList.toggle('liked'); heart.textContent = heart.classList.contains('liked') ? '♥' : '♡'; }
});
window.setTimeout(() => {
  document.querySelectorAll('.flash').forEach((el) => {
    el.style.transition = 'opacity .35s ease'; el.style.opacity = '0';
    window.setTimeout(() => el.remove(), 400);
  });
}, 3200);
