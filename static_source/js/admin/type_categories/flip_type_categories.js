document.addEventListener("DOMContentLoaded", function () {
  const updateButtons = document.querySelectorAll(".Update_TypeCategory_image");

  updateButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const typecategoryId = this.getAttribute("update-type_category-id");
      const frontCard = document.getElementById(
        `type_category_front_${typecategoryId}`
      );
      const backCard = document.getElementById(
        `type_category_back_${typecategoryId}`
      );

      // Переворачиваем карточки
      rotateAllCardsToFront();
      frontCard.style.transform = "rotateY(-180deg)";
      backCard.style.transform = "rotateY(0deg)";

      // Заполнение формы
      const nameField = backCard.querySelector('[name="name"]');
      const descriptionField = backCard.querySelector('[name="description"]');
      const categoryField = backCard.querySelector('[name="categories"]');
      const imageUploadInput = backCard.querySelector(
        `#image-upload-${typecategoryId}`
      );
      const imageUploadFilename = backCard.querySelector(
        ".image-upload-filename"
      );

      nameField.value = frontCard.querySelector(".item_header h2").innerText;
      descriptionField.value = frontCard.querySelector(
        ".item_description span"
      ).innerText;
      categoryField.value =
        frontCard.querySelector(".item_category").dataset.categoryId;

      // Событие на изменение файла
      imageUploadInput.addEventListener("change", function (event) {
        const fileName = event.target.files[0].name;
        imageUploadFilename.textContent = fileName;
      });
    });
  });

  // Добавляем обработчик для кнопок закрытия
  const closeButtons = document.querySelectorAll(".Cloose_type_category_image");
  closeButtons.forEach((closeButton) => {
    closeButton.addEventListener("click", function () {
      const typecategoryId = this.getAttribute("close-type-category-id");
      const frontCard = document.getElementById(
        `type_category_front_${typecategoryId}`
      );
      const backCard = document.getElementById(
        `type_category_back_${typecategoryId}`
      );

      // Возвращаем карточки в исходное положение
      frontCard.style.transform = "rotateY(0deg)";
      backCard.style.transform = "rotateY(180deg)";
    });
  });

  // Функция для закрытия всех карточек на переднюю сторону
  function rotateAllCardsToFront() {
    document
      .querySelectorAll(".TypeCategory_item_list")
      .forEach((frontCard) => {
        frontCard.style.transform = "rotateY(0deg)";
      });

    document
      .querySelectorAll(".TypeCategory_update_item_list")
      .forEach((backCard) => {
        backCard.style.transform = "rotateY(180deg)";
      });
  }
});
