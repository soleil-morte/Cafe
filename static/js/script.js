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

// ===== TABLE ORDER FUNCTIONS =====
function addToOrder(dishId, name, price) {
    const form = document.createElement('form');
    form.method = 'post';
    form.style.display = 'none';
    form.action = '';
    
    // Получаем CSRF токен
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const csrfInput = document.createElement('input');
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    
    const actionInput = document.createElement('input');
    actionInput.name = 'action';
    actionInput.value = 'add_item';
    
    const dishInput = document.createElement('input');
    dishInput.name = 'dish_id';
    dishInput.value = dishId;
    
    const quantityInput = document.createElement('input');
    quantityInput.name = 'quantity';
    quantityInput.value = 1;
    
    form.appendChild(csrfInput);
    form.appendChild(actionInput);
    form.appendChild(dishInput);
    form.appendChild(quantityInput);
    
    document.body.appendChild(form);
    form.submit();
}

function updateQuantity(orderItemId, change, buttonElement) {
    console.log('updateQuantity called:', orderItemId, change);
    
    // Находим элемент с количеством
    const controls = buttonElement.closest('.quantity-controls');
    const quantityElement = controls.querySelector('.quantity');
    let currentQuantity = parseInt(quantityElement.textContent);
    
    console.log('Current quantity:', currentQuantity);
    
    // Вычисляем новое количество
    let newQuantity = currentQuantity + change;
    
    // Не позволяем количеству быть меньше 1
    if (newQuantity < 1) {
        newQuantity = 1;
        return;
    }
    
    console.log('New quantity:', newQuantity);
    
    // Временно обновляем отображение для лучшего UX
    quantityElement.textContent = newQuantity;
    
    // Отправляем запрос на сервер
    sendQuantityUpdate(orderItemId, newQuantity);
}

function sendQuantityUpdate(orderItemId, quantity) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.style.display = 'none';
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    form.innerHTML = `
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
        <input type="hidden" name="action" value="update_quantity">
        <input type="hidden" name="order_item_id" value="${orderItemId}">
        <input type="hidden" name="quantity" value="${quantity}">
    `;
    
    document.body.appendChild(form);
    form.submit();
}

function removeItem(orderItemId) {
    if (confirm('Bu taomni o\'chirmoqchimisiz?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.style.display = 'none';
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        form.innerHTML = `
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
            <input type="hidden" name="action" value="remove_item">
            <input type="hidden" name="order_item_id" value="${orderItemId}">
        `;
        
        document.body.appendChild(form);
        form.submit();
    }
}

function printCheck() {
    alert('Chek chop etildi!');
}

function completeOrder() {
    if (confirm('To\'lovni amalga oshirmoqchimisiz?')) {
        const form = document.createElement('form');
        form.method = 'post';
        form.style.display = 'none';
        form.action = '';
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        
        const actionInput = document.createElement('input');
        actionInput.name = 'action';
        actionInput.value = 'complete_order';
        
        form.appendChild(csrfInput);
        form.appendChild(actionInput);
        
        document.body.appendChild(form);
        form.submit();
    }
}

// Функции для страницы заказов
function initializeTableOrder() {
    // Таймер
    let startTime = new Date();
    
    function updateTimeCounter() {
        const now = new Date();
        const diff = Math.floor((now - startTime) / 60000);
        const timeCounter = document.getElementById('timeCounter');
        if (timeCounter) {
            timeCounter.textContent = diff + ' daqiqa';
        }
    }
    
    // Поиск
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const menuItems = document.querySelectorAll('.menu-item');
            
            menuItems.forEach(item => {
                const name = item.querySelector('.item-name').textContent.toLowerCase();
                if (name.includes(searchTerm)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Категории
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Запускаем таймер
    setInterval(updateTimeCounter, 60000);
    updateTimeCounter();
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Если это страница заказа стола, инициализируем функции
    if (document.querySelector('.table-order-page')) {
        initializeTableOrder();
    }
    
});




// JavaScript для отображения конвертации в реальном времени
document.addEventListener('DOMContentLoaded', function() {
    function updateConversionInfo() {
        document.querySelectorAll('.ingredient-form').forEach(form => {
            const productSelect = form.querySelector('select[name$="-product"]');
            const quantityInput = form.querySelector('input[name$="-quantity"]');
            const unitSelect = form.querySelector('select[name$="-unit"]');
            const conversionInfo = form.querySelector('.conversion-info');
            
            if (productSelect && quantityInput && unitSelect && conversionInfo) {
                const productId = productSelect.value;
                const quantity = parseFloat(quantityInput.value) || 0;
                const ingredientUnit = unitSelect.value;
                
                if (productId && quantity > 0) {
                    // Здесь можно добавить AJAX запрос для получения информации о продукте
                    // Пока просто покажем единицы
                    conversionInfo.textContent = `Указано: ${quantity} ${ingredientUnit}`;
                } else {
                    conversionInfo.textContent = '';
                }
            }
        });
    }
    
    // Обновляем при изменении полей
    document.addEventListener('change', function(e) {
        if (e.target.matches('select[name$="-product"], select[name$="-unit"], input[name$="-quantity"]')) {
            updateConversionInfo();
        }
    });
    
    updateConversionInfo();
});


function addToOrder(dishId, name, price) {
    // Можно добавить проверку доступности порций через AJAX
    // Пока просто добавляем в заказ
    const form = document.createElement('form');
    form.method = 'post';
    form.style.display = 'none';
    form.action = '';
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const csrfInput = document.createElement('input');
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    
    const actionInput = document.createElement('input');
    actionInput.name = 'action';
    actionInput.value = 'add_item';
    
    const dishInput = document.createElement('input');
    dishInput.name = 'dish_id';
    dishInput.value = dishId;
    
    form.appendChild(csrfInput);
    form.appendChild(actionInput);
    form.appendChild(dishInput);
    
    document.body.appendChild(form);
    form.submit();
}