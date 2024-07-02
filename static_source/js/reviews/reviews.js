let page = 2;
let loading = false;
let hasNext = true;

function formatDate(dateString) {
  const options = { year: "numeric", month: "2-digit", day: "2-digit" };
  return new Date(dateString).toLocaleDateString("en-CA", options);
}

function addStarsToRating(ratingElement, rating) {
  const fullStars = Math.floor(rating);
  const emptyStars = 5 - fullStars;

  // Очистка содержимого ratingElement перед добавлением звезд
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

  fetch(`/get_reviews/?page=${page}`)
    .then((response) => response.json())
    .then((data) => {
      const reviewList = document.getElementById("review_list");

      data.reviews.forEach((review) => {
        const reviewItem = document.createElement("li");
        reviewItem.className = "review_item";
        reviewItem.innerHTML = `
                    <ul class="review_user_info_list">
                        <li class="review_user_image">
                            ${
                              review.profile_image
                                ? `<img src="${review.profile_image}" alt="" class="user_image">`
                                : `<img src="/static/icon/profile.png" alt="" class="user_image">`
                            }
                        </li>
                        <li class="review_user_name">
                            ${review.name} ${review.surname}
                        </li>
                    </ul>
                    <span class="review_commit">
                        ${review.comment}
                    </span>
                    <ul class="rating_list">
                        <li class="rating" data-rating="${review.rating}">
                        </li>
                        <li class="created_at_item">
                            <span>${formatDate(review.created_at)}</span>
                        </li>
                    </ul>
                `;
        reviewList.appendChild(reviewItem);

        // Добавляем звездочки рейтинга только для нового комментария
        const ratingElement = reviewItem.querySelector(".rating");
        const rating = parseInt(ratingElement.getAttribute("data-rating"));
        addStarsToRating(ratingElement, rating);
      });

      hasNext = data.has_next;
      if (!hasNext) {
        document.getElementById("load_more_reviews").style.display = "none";
      }
      page += 1;
      loading = false;

      // Прокрутка до последнего элемента
      const lastReviewItem = reviewList.lastElementChild;
      if (lastReviewItem) {
        lastReviewItem.scrollIntoView({ behavior: "smooth" });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      loading = false;
    });
}

// Добавляем обработчик события для кнопки "Посмотреть еще"
document.getElementById("load_more_reviews").addEventListener("click", () => {
  loadReviews();
});

// Вызываем функцию для загрузки комментариев при загрузке страницы, если список пуст
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("review_list").childElementCount === 0) {
    loadReviews();
  }
});
