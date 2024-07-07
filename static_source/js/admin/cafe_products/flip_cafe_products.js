document.addEventListener("DOMContentLoaded", function () {
  const updateButtons = document.querySelectorAll(".Update_CafeProduct_image");

  updateButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const cafeProductId = this.getAttribute("update-cafe_product-id");
      const frontCard = document.getElementById(
        `cafe_product_front_${cafeProductId}`
      );
      const backCard = document.getElementById(
        `cafe_product_back_${cafeProductId}`
      );

      // Переворачиваем карточки
      rotateAllCardsToFront();
      if (frontCard && backCard) {
        frontCard.style.transform = "rotateY(-180deg)";
        backCard.style.transform = "rotateY(0deg)";
      } else {
        return; // Остановить выполнение, если карточки не найдены
      }

      // Заполнение формы
      const nameField = backCard.querySelector(
        '.form-control-cafe-product[name="name"]'
      );
      const descriptionField = backCard.querySelector(
        '.form-control-cafe-description[name="description"]'
      );
      const compositionField = backCard.querySelector(
        '.form-control-cafe-composition[name="composition"]'
      );
      const priceField = backCard.querySelector(
        '.form-control-cafe-price[name="price"]'
      );
      const typeCafeProductField = backCard.querySelector(
        '.form-control-type-cafe-product[name="type_cafe_product"]'
      );
      const imageUploadInput = backCard.querySelector(
        `#image-upload-${cafeProductId}`
      );
      const imageUploadFilename = backCard.querySelector(
        ".image-upload-filename"
      );

      if (
        !nameField ||
        !descriptionField ||
        !compositionField ||
        !priceField ||
        !typeCafeProductField ||
        !imageUploadInput ||
        !imageUploadFilename
      ) {
        return; // Остановить выполнение, если поля не найдены
      }

      // Заполнение полей формы
      const itemHeader = frontCard.querySelector(".item_header h2");
      if (itemHeader && nameField) {
        nameField.value = itemHeader.innerText;
      }

      const itemDescription = frontCard.querySelector(".item_description span");
      if (itemDescription && descriptionField) {
        descriptionField.value = itemDescription.innerText;
      }

      const itemComposition = frontCard.querySelector(".item_composition span");
      if (itemComposition && compositionField) {
        compositionField.value = itemComposition.innerText;
      }

      const itemPrice = frontCard.querySelector(".item_header h2:nth-child(2)");
      if (itemPrice) {
        const priceValue = parseFloat(
          itemPrice.innerText.replace(" грн", "").replace(",", ".")
        );
        priceField.value = priceValue.toFixed(2);
      }

      const itemCategory = frontCard.querySelector(".item_category");
      if (itemCategory && typeCafeProductField) {
        const categoryId = itemCategory.dataset.categoryId;
        const options = typeCafeProductField.options;
        for (let i = 0; i < options.length; i++) {
          if (options[i].value == categoryId) {
            typeCafeProductField.selectedIndex = i;
            break;
          }
        }
      }

      // Событие на изменение файла
      imageUploadInput.addEventListener("change", function (event) {
        const fileName = event.target.files[0]?.name;
        if (fileName) {
          imageUploadFilename.textContent = fileName;
        }
      });
    });
  });

  // Добавляем обработчик для кнопок закрытия
  const closeButtons = document.querySelectorAll(".Cloose_cafe_product_image");
  closeButtons.forEach((closeButton) => {
    closeButton.addEventListener("click", function () {
      const cafeProductId = this.getAttribute("close-cafe-product-id");
      const frontCard = document.getElementById(
        `cafe_product_front_${cafeProductId}`
      );
      const backCard = document.getElementById(
        `cafe_product_back_${cafeProductId}`
      );

      if (frontCard && backCard) {
        frontCard.style.transform = "rotateY(0deg)";
        backCard.style.transform = "rotateY(180deg)";
      }
    });
  });

  // Функция для закрытия всех карточек на переднюю сторону
  function rotateAllCardsToFront() {
    document.querySelectorAll(".CafeProduct_item_list").forEach((frontCard) => {
      frontCard.style.transform = "rotateY(0deg)";
    });

    document
      .querySelectorAll(".CafeProduct_update_item_list")
      .forEach((backCard) => {
        backCard.style.transform = "rotateY(180deg)";
      });
  }
});
