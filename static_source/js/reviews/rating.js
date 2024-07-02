document.addEventListener("DOMContentLoaded", function () {
  const stars = document.querySelectorAll(".star_rating");
  const ratingInput = document.querySelector("#id_rating");
  stars.forEach((star) => {
    star.addEventListener("click", function () {
      const value = this.dataset.value;
      ratingInput.value = value;
      stars.forEach((s) => {
        if (s.dataset.value <= value) {
          s.innerHTML = "★"; // Звезда заполнена
        } else {
          s.innerHTML = "☆"; // Звезда пуста
        }
      });
    });
  });
});
