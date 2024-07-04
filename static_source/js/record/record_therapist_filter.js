document.addEventListener("DOMContentLoaded", function () {
  const therapistList = document.getElementById("therapist-list");

  therapistList.addEventListener("click", function (event) {
    const target = event.target.closest(".therapist-item");
    if (target) {
      const checkbox = target.querySelector('input[type="checkbox"]');
      if (checkbox) {
        // Снимаем отметку со всех чекбоксов
        therapistList
          .querySelectorAll('input[type="checkbox"]')
          .forEach((cb) => (cb.checked = false));

        // Устанавливаем отметку на текущий чекбокс
        checkbox.checked = true;

        // Устанавливаем значение выбранного терапевта в скрытое поле
        document.getElementById("selected-therapist").value = checkbox.value;

        // Удаляем класс "selected" у всех элементов
        const items = therapistList.querySelectorAll(".therapist-item");
        items.forEach((item) => item.classList.remove("selected"));

        // Добавляем класс "selected" к текущему элементу
        target.classList.add("selected");
      }
    }
  });
});
