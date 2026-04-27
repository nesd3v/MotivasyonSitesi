/* ============================================================
   MotivaSyon - Bildirim JavaScript Dosyası
   Motivasyon gönderme, tarayıcı bildirimleri, rozet kontrolü
   ============================================================ */

// Motivasyon gönder butonuna basıldığında çağrılıyor
function sendMotivation() {
    const btn = document.getElementById('motivateBtn');
    const bigBtn = document.querySelector('.btn-big-motivate');

    // Butonları loading haline getiriyorum
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Yükleniyor...'; }
    if (bigBtn) { bigBtn.disabled = true; bigBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Yükleniyor...'; }

    fetch('/send-motivation', { method: 'POST' })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                // Motivasyon popup'ını gösteriyorum
                showMotivationPopup(data.title, data.quote.text, data.quote.author);
                // Tarayıcı bildirimini deniyorum
                sendBrowserNotification(data.title, data.quote.text);
                showToast('Motivasyon bildirimi gönderildi!', 'success');
                // Bildirim listesini güncelliyorum
                updateNotifBadge(1);
            }
        })
        .catch(() => showToast('Bir hata oluştu, tekrar dene.', 'danger'))
        .finally(() => {
            // Butonları normal haline döndürüyorum
            if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-bolt"></i> <span>Motivasyon Al</span>'; }
            if (bigBtn) { bigBtn.disabled = false; bigBtn.innerHTML = '<i class="fas fa-bolt me-2"></i>Motivasyonumu Güçlendir'; }
        });
}

// Motivasyon popup'ını açıyorum ve alıntıyı gösteriyorum
function showMotivationPopup(title, quote, author) {
    const popup = document.getElementById('motivationPopup');
    const popupTitle = document.getElementById('popupTitle');
    const popupQuote = document.getElementById('popupQuote');
    const popupAuthor = document.getElementById('popupAuthor');

    if (!popup) return;

    popupTitle.textContent = title;
    popupQuote.textContent = `"${quote}"`;
    popupAuthor.textContent = `— ${author}`;

    popup.classList.add('show');

    // 8 saniye sonra otomatik kapatıyorum
    setTimeout(() => popup.classList.remove('show'), 8000);
}

// Tarayıcı web bildirimi gönderiyorum - izin alındıysa çalışıyor
function sendBrowserNotification(title, body) {
    if (!('Notification' in window)) return;

    if (Notification.permission === 'granted') {
        new Notification('MotivaSyon - ' + title, {
            body: body.substring(0, 100),
            icon: '/static/images/icon.png',
            badge: '/static/images/icon.png'
        });
    } else if (Notification.permission !== 'denied') {
        // İzin isteği gönderiyorum
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                new Notification('MotivaSyon - ' + title, { body: body.substring(0, 100) });
            }
        });
    }
}

// Rozet kazanıldığını sunucuya kontrol ettiriyorum
function checkBadges() {
    fetch('/check-badges', { method: 'POST' })
        .then(r => r.json())
        .then(data => {
            if (data.new_badges && data.new_badges.length > 0) {
                // Yeni rozetleri sırayla gösteriyorum
                data.new_badges.forEach((badge, index) => {
                    setTimeout(() => {
                        showBadgePopup(badge);
                        showToast(`Yeni rozet kazandın: ${badge.name}!`, 'success');
                        updateNotifBadge(1);
                    }, index * 1500);
                });
            }
        });
}

// Sayfa yüklendiğinde tarayıcı bildirimi izni istiyorum
document.addEventListener('DOMContentLoaded', function() {
    if ('Notification' in window && Notification.permission === 'default') {
        // Kullanıcı etkileşimi olmadan izin istemek engelleniyor, buton ile istiyorum
        console.log('Bildirim izni bekleniyor - buton ile istenecek.');
    }
});
