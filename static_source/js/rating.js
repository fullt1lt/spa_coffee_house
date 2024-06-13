document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.querySelector('#id_rating'); // Замените на ваш идентификатор поля рейтинга
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const value = this.dataset.value;
            ratingInput.value = value;
            // Установка активного состояния для звёзд
            stars.forEach(s => {
                if (s.dataset.value <= value) {
                    s.innerHTML = '★'; // Звезда заполнена
                } else {
                    s.innerHTML = '☆'; // Звезда пуста
                }
            });
        });
    });
});
