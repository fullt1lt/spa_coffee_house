document.addEventListener("DOMContentLoaded", function () {
  const updateButtons = document.querySelectorAll(".Update_therapist_image");

  updateButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const therapistId = this.getAttribute("update-therapist-id");
      const frontCard = document.getElementById(
        `therapist_front_${therapistId}`
      );
      const backCard = document.getElementById(`therapist_back_${therapistId}`);

      // Переворачиваем карточки
      rotateAllCardsToFront();
      frontCard.style.transform = "rotateY(-180deg)";
      backCard.style.transform = "rotateY(0deg)";


      // Находим элемент .Cloose_therapist_form_list
      const formList = backCard.querySelector(".Cloose_therapist_form_list");

      // Проверяем, есть ли уже форма в .Cloose_therapist_form_list
      const existingForm = formList.querySelector("form");

      // Если формы нет, то создаем и добавляем форму
      if (!existingForm) {
        const form = document.createElement("form");
        form.method = "post";
        form.enctype = "multipart/form-data";
        form.classList.add("therapist_form_update");

        // Перемещаем все дочерние элементы .Cloose_therapist_form_list внутрь form
        while (formList.firstChild) {
          form.appendChild(formList.firstChild);
        }

        // Добавляем CSRF токен в форму
        const csrfInput = document.createElement("input");
        csrfInput.type = "hidden";
        csrfInput.name = "csrfmiddlewaretoken";
        csrfInput.value = getCookie("csrftoken");
        form.appendChild(csrfInput);

        // Вставляем созданный тег <form> в .Cloose_therapist_form_list
        formList.appendChild(form);
      }
    });
  });

  // Добавляем обработчик для кнопок закрытия
  const closeButtons = document.querySelectorAll(".Cloose_therapist_image");
  closeButtons.forEach((closeButton) => {
    closeButton.addEventListener("click", function () {
      const therapistId = this.getAttribute("close-therapist-id");
      const frontCard = document.getElementById(
        `therapist_front_${therapistId}`
      );
      const backCard = document.getElementById(`therapist_back_${therapistId}`);

      // Возвращаем карточки в исходное положение
      frontCard.style.transform = "rotateY(0deg)";
      backCard.style.transform = "rotateY(180deg)";
    });
  });

  // Функция для закрытия всех карточек на переднюю сторону
  function rotateAllCardsToFront() {
    document
      .querySelectorAll(".Massage_Therapist_info")
      .forEach((frontCard) => {
        frontCard.style.transform = "rotateY(0deg)";
      });

    document
      .querySelectorAll(".Massage_Therapist_update_item")
      .forEach((backCard) => {
        backCard.style.transform = "rotateY(180deg)";
      });
  }

  // Функция для получения CSRF токена из cookie
  function getCookie(name) {
    const cookieValue = document.cookie.match(
      `(^|;)\\s*${name}\\s*=\\s*([^;]+)`
    );
    return cookieValue ? cookieValue.pop() : "";
  }
});
