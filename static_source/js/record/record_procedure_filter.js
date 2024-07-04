document.addEventListener("DOMContentLoaded", function () {
  const categoryButtons = document.querySelectorAll(
    "#category-buttons .category-button"
  );
  const procedureList = document.getElementById("procedure-list");
  categoryButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Удаляем класс "selected" у всех кнопок
      categoryButtons.forEach((btn) =>
        btn.classList.remove("selected")
      );
      // Добавляем класс "selected" к текущей кнопке
      this.classList.add("selected");
      const categoryId = this.getAttribute("data-category-id");
      // Фильтруем процедуры по категории
      procedureList
        .querySelectorAll(".procedure-item")
        .forEach((item) => {
          if (item.getAttribute("data-category-id") === categoryId) {
            item.style.display = "flex";
          } else {
            item.style.display = "none";
          }
        });
    });
  });
  
  procedureList.addEventListener("click", function (event) {
    const target = event.target.closest(".procedure-item-label");
    if (target) {
      const checkbox = target.querySelector('input[type="checkbox"]');
      if (checkbox) {
        // Снимаем отметку со всех чекбоксов
        procedureList
          .querySelectorAll('input[type="checkbox"]')
          .forEach((cb) => (cb.checked = false));

        // Устанавливаем отметку на текущий чекбокс
        checkbox.checked = true;

        // Устанавливаем значение выбранной процедуры в скрытое поле
        document.getElementById("selected-procedure").value = checkbox.value;

        // Удаляем класс "selected" у всех элементов
        const items = procedureList.querySelectorAll(".procedure-item");
        items.forEach((item) => item.classList.remove("selected"));

        // Добавляем класс "selected" к текущему элементу
        target.parentElement.classList.add("selected");
      }
    }
  });
});