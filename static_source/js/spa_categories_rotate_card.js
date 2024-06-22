document.addEventListener("DOMContentLoaded", () => {
  // Находим все элементы с классом Update_image
  const updateButtons = document.querySelectorAll(".Update_image");

  updateButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Получаем ID категории из кнопки
      const categoryId = this.getAttribute("update-category-id");

      // Находим элементы front и back по ID категории
      const categoryFront = document.getElementById(
        `categories_front_${categoryId}`
      );
      const categoryBack = document.getElementById(
        `categories_back_${categoryId}`
      );

      if (categoryFront) {
        // Применяем стиль rotateY(-180deg) к front
        categoryFront.style.transform = "rotateY(-180deg)";
        console.log("Изменен стиль front карточки с ID:", categoryId);
      }

      if (categoryBack) {
        // Применяем стиль rotateY(0deg) к back
        categoryBack.style.transform = "rotateY(0deg)";
        console.log("Изменен стиль back карточки с ID:", categoryId);
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // Находим все элементы с классом Update_image
  const updateButtons = document.querySelectorAll(".Cloose_image");

  updateButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Получаем ID категории из кнопки
      const categoryId = this.getAttribute("close-category-id");

      // Находим элементы front и back по ID категории
      const categoryFront = document.getElementById(
        `categories_front_${categoryId}`
      );
      const categoryBack = document.getElementById(
        `categories_back_${categoryId}`
      );

      if (categoryFront) {
        // Применяем стиль rotateY(-180deg) к front
        categoryFront.style.transform = "rotateY(0deg)";
        console.log("Изменен стиль front карточки с ID:", categoryId);
      }

      if (categoryBack) {
        // Применяем стиль rotateY(0deg) к back
        categoryBack.style.transform = "rotateY(180deg)";
        console.log("Изменен стиль back карточки с ID:", categoryId);
      }
    });
  });
});
