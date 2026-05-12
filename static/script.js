function parseOpeningHours(openingHours) {
    if (!openingHours) {
        return null;
    }

    const parts = openingHours.split('-').map(part => part.trim());
    if (parts.length !== 2) {
        return null;
    }

    const parseTime = (value) => {
        const match = value.match(/^(\d{1,2}):(\d{2})$/);
        if (!match) {
            return null;
        }
        const hour = Number(match[1]);
        const minute = Number(match[2]);
        if (hour < 0 || hour > 23 || minute < 0 || minute > 59) {
            return null;
        }
        return hour * 60 + minute;
    };

    const open = parseTime(parts[0]);
    const close = parseTime(parts[1]);
    if (open === null || close === null) {
        return null;
    }

    return { open, close };
}

function getOpenStatus(openingHours) {
    const times = parseOpeningHours(openingHours);
    if (!times) {
        return {
            state: 'unknown',
            text: '⏱️ Jam tidak tersedia'
        };
    }

    const now = new Date();
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    const { open, close } = times;
    let isOpen;

    if (open < close) {
        isOpen = currentMinutes >= open && currentMinutes < close;
    } else {
        isOpen = currentMinutes >= open || currentMinutes < close;
    }

    return isOpen
        ? { state: 'open', text: '🟢 Buka' }
        : { state: 'closed', text: '🔴 Tutup' };
}

function updateOpeningBadges() {
    document.querySelectorAll('[data-opening-hours]').forEach(function(wrapper) {
        const openingHours = wrapper.dataset.openingHours || '';
        const badge = wrapper.classList.contains('opening-badge')
            ? wrapper
            : wrapper.querySelector('.opening-badge');

        if (!badge) {
            return;
        }

        const status = getOpenStatus(openingHours);
        badge.textContent = status.text;
        badge.classList.remove('open', 'closed', 'unknown');
        badge.classList.add(status.state);

        if (status.state === 'open') {
            badge.style.background = '#16a34a';
            badge.style.color = '#ffffff';
        } else if (status.state === 'closed') {
            badge.style.background = '#dc2626';
            badge.style.color = '#ffffff';
        } else {
            badge.style.background = '#6b7280';
            badge.style.color = '#ffffff';
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.popup').forEach(function(popup) {
        setTimeout(function() {
            popup.classList.remove('show');
            setTimeout(function() {
                if (popup.parentElement) {
                    popup.parentElement.removeChild(popup);
                }
            }, 300);
        }, 3000);
    });

    updateOpeningBadges();
    setInterval(updateOpeningBadges, 60000);
});
