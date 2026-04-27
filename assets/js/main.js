/* ============================================================
   MotivaSyon - Ana JavaScript Dosyası
   Genel UI fonksiyonları burada - sidebar, toast, modal vs.
   ============================================================ */

// Sidebar aç/kapat - mobilde hamburger menüsü için
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.toggle('open');
    overlay.classList.toggle('show');
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
}

// Ekran büyüyünce overlay'i otomatik kapatıyorum
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) closeSidebar();
});

// Bildirim paneli toggle - şimdilik profil sayfasına yönlendiriyor
function toggleNotifPanel() {
    window.location.href = '/profile';
}

// Toast mesajı gösteriyorum - category: success, info, danger
function showToast(message, category = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast-msg ${category}`;
    toast.textContent = message;
    container.appendChild(toast);

    // Kısa gecikme ile görünür yapıyorum (CSS transition için)
    requestAnimationFrame(() => {
        requestAnimationFrame(() => toast.classList.add('show'));
    });

    // 3 saniye sonra otomatik kapatıyorum
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Bildirimi okundu olarak işaretliyorum
function markRead(notifId) {
    const item = document.getElementById(`notif-${notifId}`);
    if (!item || !item.classList.contains('unread')) return;

    fetch(`/notifications/read/${notifId}`, { method: 'POST' })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                item.classList.remove('unread');
                const dot = item.querySelector('.unread-dot');
                if (dot) dot.remove();
                // Üst bardaki bildirim sayısını güncelliyorum
                updateNotifBadge(-1);
            }
        });
}

// Tüm bildirimleri okundu yapıyorum
function markAllRead() {
    fetch('/notifications/read-all', { method: 'POST' })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                document.querySelectorAll('.notif-item.unread, .notif-history-item.unread').forEach(el => {
                    el.classList.remove('unread');
                    const dot = el.querySelector('.unread-dot');
                    if (dot) dot.remove();
                });
                // Badge'i sıfırlıyorum
                const badge = document.querySelector('.notif-badge');
                if (badge) badge.remove();
                showToast('Tüm bildirimler okundu.', 'info');
            }
        });
}

// Bildirim badge sayısını güncelliyorum
function updateNotifBadge(delta) {
    const badge = document.querySelector('.notif-badge');
    if (!badge) return;
    const current = parseInt(badge.textContent) + delta;
    if (current <= 0) {
        badge.remove();
    } else {
        badge.textContent = current;
    }
}

// Günlük alıntıyı yeniliyorum - AJAX ile rastgele yeni alıntı çekiyorum
function refreshQuote() {
    const btn = document.querySelector('.btn-refresh');
    if (btn) btn.style.transform = 'rotate(180deg)';

    fetch('/random-quote')
        .then(r => r.json())
        .then(data => {
            if (data.text) {
                const display = document.getElementById('quoteDisplay');
                if (display) {
                    // Kısa fade animasyonu yapıyorum
                    display.style.opacity = '0';
                    setTimeout(() => {
                        display.innerHTML = `
                            <blockquote class="daily-quote-text">${data.text}</blockquote>
                            <cite class="daily-quote-author">— ${data.author}</cite>
                            <span class="quote-category-badge">${data.category}</span>
                        `;
                        display.style.opacity = '1';
                        display.style.transition = 'opacity 0.4s ease';
                    }, 300);
                }
            }
        })
        .finally(() => {
            if (btn) setTimeout(() => btn.style.transform = '', 300);
        });
}

// Yeni rozet kazanıldıysa popup'ı gösteriyorum
function showBadgePopup(badge) {
    const popup = document.getElementById('badgePopup');
    if (!popup) return;

    document.getElementById('badgeIcon').textContent = badge.icon;
    document.getElementById('badgeName').textContent = badge.name;
    document.getElementById('badgeDesc').textContent = badge.description;

    popup.classList.add('show');

    // 4 saniye sonra otomatik kapatıyorum
    setTimeout(() => popup.classList.remove('show'), 4000);
}

// Motivasyon popup'ını kapatıyorum
function closePopup() {
    const popup = document.getElementById('motivationPopup');
    if (popup) popup.classList.remove('show');
}

// ESC tuşuyla popup kapatıyorum
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closePopup();
});

// Stat sayaç animasyonu - sayıları 0'dan hedef değere doğru sayıyor
function animateCounter(el, target, duration = 1200) {
    const start = performance.now();
    const isDecimal = String(target).includes('.');

    function tick(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // ease-out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = eased * target;
        el.textContent = isDecimal ? current.toFixed(1) : Math.floor(current);
        if (progress < 1) requestAnimationFrame(tick);
        else el.textContent = target;
    }
    requestAnimationFrame(tick);
}

// Sayfadaki tüm .stat-number elementlerini sayaç animasyonu ile çalıştır
function initCounters() {
    document.querySelectorAll('.stat-number, .pstat-num, .streak-number').forEach(el => {
        const raw = el.textContent.trim();
        const target = parseFloat(raw);
        if (!isNaN(target) && target > 0) {
            el.textContent = '0';
            // Animasyonun görünür olması için kısa delay
            setTimeout(() => animateCounter(el, target), 400);
        }
    });
}

// Scroll reveal - IntersectionObserver ile elementleri görünce fade-in et
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

// Sayfa yüklendiğinde çalıştır
document.addEventListener('DOMContentLoaded', function() {
    initCounters();
    initScrollReveal();
});
