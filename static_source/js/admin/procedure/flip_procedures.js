document.addEventListener("DOMContentLoaded", function () {
  const updateButtons = document.querySelectorAll(".Update_Procedure_image");

  updateButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const procedureId = this.getAttribute("update-procedure-id");
      const frontCard = document.getElementById(
        `procedure_front_${procedureId}`
      );
      const backCard = document.getElementById(`procedure_back_${procedureId}`);

      // Переворачиваем карточки
      rotateAllCardsToFront();
      if (frontCard && backCard) {
        frontCard.style.transform = "rotateY(-180deg)";
        backCard.style.transform = "rotateY(0deg)";
      }

      // Заполнение формы
      const durationField = backCard.querySelector('[name="duration"]');
      const priceField = backCard.querySelector('[name="price"]');

      // Добавить проверку наличия полей
      if (durationField && priceField) {
        const durationText = frontCard.querySelector(
          ".item_duration span"
        ).innerText;
        const durationMinutes = parseInt(
          durationText.replace("Тривалість: ", "").replace(" хв", ""),
          10
        );

        // Вывод всех значений опций в durationField для проверки
        const durationOptions = durationField.options;
        for (let i = 0; i < durationOptions.length; i++) {
          if (parseInt(durationOptions[i].text, 10) === durationMinutes) {
            durationField.selectedIndex = i;
            break;
          }
        }

        const priceText = frontCard.querySelector(".item_price span").innerText;
        const priceValue = parseFloat(
          priceText.replace("Цiна: ", "").replace(" грн", "")
        );
        priceField.value = priceValue;
      }
    });
  });

  // Добавляем обработчик для кнопок закрытия
  const closeButtons = document.querySelectorAll(".Cloose_procedure_image");
  closeButtons.forEach((closeButton) => {
    closeButton.addEventListener("click", function () {
      const procedureId = this.getAttribute("close-procedure-id");
      const frontCard = document.getElementById(
        `procedure_front_${procedureId}`
      );
      const backCard = document.getElementById(`procedure_back_${procedureId}`);

      // Возвращаем карточки в исходное положение
      if (frontCard && backCard) {
        frontCard.style.transform = "rotateY(0deg)";
        backCard.style.transform = "rotateY(180deg)";
      }
    });
  });

  // Функция для закрытия всех карточек на переднюю сторону
  function rotateAllCardsToFront() {
    document.querySelectorAll(".Procedure_item_list").forEach((frontCard) => {
      frontCard.style.transform = "rotateY(0deg)";
    });

    document
      .querySelectorAll(".Procedure_update_item_list")
      .forEach((backCard) => {
        backCard.style.transform = "rotateY(180deg)";
      });
  }
});
