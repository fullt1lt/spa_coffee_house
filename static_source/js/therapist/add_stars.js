document.addEventListener("DOMContentLoaded", function () {
  const ratingElements = document.querySelectorAll(".rating");

  ratingElements.forEach((el) => {
    const rating = parseInt(el.getAttribute("data-rating"));
    const fullStars = Math.floor(rating);
    const emptyStars = 5 - fullStars;

    // Добавляем полные звезды
    for (let i = 0; i < fullStars; i++) {
      const star = document.createElement("span");
      star.classList.add("star");
      star.innerHTML = "★";
      el.appendChild(star);
    }

    // Добавляем пустые звезды
    for (let i = 0; i < emptyStars; i++) {
      const emptyStar = document.createElement("span");
      emptyStar.classList.add("star");
      emptyStar.innerHTML = "☆";
      el.appendChild(emptyStar);
    }
  });
});
