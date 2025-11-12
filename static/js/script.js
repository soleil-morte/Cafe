// Базовые скрипты для интерфейса
document.addEventListener('DOMContentLoaded', function() {
    console.log('Система управления кафе загружена!');
    
    // Анимация карточек при загрузке
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Подсветка активной страницы в навигации
    const currentPage = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.style.background = 'rgba(255,255,255,0.2)';
            link.style.fontWeight = 'bold';
        }
    });
    
    // Простой обработчик для кнопок
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') {
                e.preventDefault();
                alert('Функция в разработке!');
            }
        });
    });
});

// Простое подтверждение удаления
document.addEventListener('DOMContentLoaded', function() {
    // Обработчик для всех ссылок удаления
    const deleteLinks = document.querySelectorAll('a[href*="/delete/"]');
    
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const objectName = this.closest('.product-card, .dish-card, .table-card')
                                .querySelector('h3').textContent;
            
            if (!confirm(`Вы уверены, что хотите удалить "${objectName}"?`)) {
                e.preventDefault();
            }
        });
    });
    
    // Простое подтверждение для занятия/освобождения столов
    const toggleLinks = document.querySelectorAll('a[href*="/toggle/"]');
    toggleLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const tableCard = this.closest('.table-card');
            const tableNumber = tableCard.querySelector('h3').textContent;
            const action = this.textContent.includes('Занять') ? 'занять' : 'освободить';
            
            if (!confirm(`Вы уверены, что хотите ${action} ${tableNumber}?`)) {
                e.preventDefault();
            }
        });
    });
});