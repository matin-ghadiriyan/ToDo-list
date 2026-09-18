// TaskFlow client-side interactions

document.addEventListener('DOMContentLoaded', () => {
  /* ---------- Mobile sidebar ---------- */
  const sidebar = document.getElementById('sidebar');
  const menuToggle = document.getElementById('menuToggle');
  const overlay = document.getElementById('overlay');

  const closeSidebar = () => {
    if (!sidebar) return;
    sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('show');
  };

  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('show');
    });
  }

  if (overlay) overlay.addEventListener('click', closeSidebar);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSidebar();
  });

  /* ---------- Auto-dismiss flash messages ---------- */
  document.querySelectorAll('.flash').forEach((flash) => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateY(-8px)';
      setTimeout(() => flash.remove(), 400);
    }, 4000);
  });

  /* ---------- Animate task cards on load ---------- */
  const animatedItems = document.querySelectorAll(
    '.task-card, .timeline-item, .stat-card, .mini-item'
  );
  animatedItems.forEach((el, index) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(12px)';
    setTimeout(() => {
      el.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, index * 45);
  });

  /* ---------- Visual feedback for toggle buttons ---------- */
  document.querySelectorAll('.check').forEach((btn) => {
    btn.addEventListener('click', () => {
      btn.style.transform = 'scale(0.85)';
      setTimeout(() => (btn.style.transform = ''), 150);
    });
  });

  /* ---------- Keyboard shortcut: "n" for new task ---------- */
  document.addEventListener('keydown', (e) => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
    if (e.key === 'n' || e.key === 'N') {
      const newBtn = document.querySelector('a[href$="/tasks/new"]');
      if (newBtn) window.location.href = newBtn.getAttribute('href');
    }
  });
});
