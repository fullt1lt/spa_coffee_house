let page = 1; // Начальная страница для загрузки
let loading = false; // Флаг загрузки
let hasNext = true; // Флаг наличия следующих страниц
let loadedCommentIds = new Set(); // Множество для хранения ID загруженных комментариев

function addStarsToRating(ratingElement, rating) {
  const fullStars = Math.floor(rating);
  const emptyStars = 5 - fullStars;

  // Очищаем содержимое ratingElement перед добавлением звезд
  ratingElement.innerHTML = "";

  // Добавляем полные звезды
  for (let i = 0; i < fullStars; i++) {
    const star = document.createElement("span");
    star.classList.add("star");
    star.innerHTML = "★";
    ratingElement.appendChild(star);
  }

  // Добавляем пустые звезды
  for (let i = 0; i < emptyStars; i++) {
    const emptyStar = document.createElement("span");
    emptyStar.classList.add("star");
    emptyStar.innerHTML = "☆";
    ratingElement.appendChild(emptyStar);
  }
}

function loadReviews() {
  if (loading || !hasNext) return;
  loading = true;
  document.getElementById("loading").style.display = "block";

  fetch(`/get_reviews/?page=${page}`)
    .then((response) => response.json())
    .then((data) => {
      const reviewList = document.getElementById("review_list");
      data.reviews.forEach((review) => {
        // Проверяем, что комментарий еще не был загружен
        if (!loadedCommentIds.has(review.id)) {
          loadedCommentIds.add(review.id); // Добавляем ID комментария в множество загруженных

          const reviewItem = document.createElement("li");
          reviewItem.className = "review_item";
          reviewItem.dataset.reviewId = review.id;
          reviewItem.innerHTML = `
            <ul class="review_user_info_list">
              <li class="review_user_image">
                ${
                  review.profile_image
                    ? `<img src="${review.profile_image}" alt="" class="user_image">`
                    : `<img src="/static/icon/profile.png" alt="" class="user_image">`
                }
              </li>
              <li class="review_user_name">${review.user}</li>
            </ul>
            <span class="review_commit">${review.comment}</span>
            <ul class="rating_list">
              <li class="rating" data-rating="${review.rating}"></li>
            </ul>
          `;
          reviewList.appendChild(reviewItem);

          // Добавляем звездочки рейтинга только для нового комментария
          const ratingElement = reviewItem.querySelector(".rating");
          const rating = parseInt(ratingElement.getAttribute("data-rating"));
          addStarsToRating(ratingElement, rating);
        }
      });
      hasNext = data.has_next;
      page += 1;
      loading = false;
      document.getElementById("loading").style.display = "none";
    })
    .catch((error) => {
      console.error("Error:", error);
      loading = false;
      document.getElementById("loading").style.display = "none";
    });
}

// Функция для проверки необходимости загрузки новых комментариев при скролле
function handleScroll() {
  const reviewList = document.getElementById("review_list");
  if (
    reviewList.scrollTop + reviewList.clientHeight >=
    reviewList.scrollHeight - 50
  ) {
    loadReviews();
  }
}

// Добавляем обработчик события скролла
document.addEventListener("DOMContentLoaded", function () {
  // Вызываем первоначальную загрузку комментариев
  loadReviews();

  // Добавляем обработчик события скролла только если есть что прокручивать
  if (document.getElementById("review_list")) {
    document
      .getElementById("review_list")
      .addEventListener("scroll", handleScroll);
  }
});
