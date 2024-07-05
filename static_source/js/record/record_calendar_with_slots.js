document.addEventListener("DOMContentLoaded", function () {
  // Используем доступные слоты, переданные из Django
  const availableSlots = JSON.parse(
    document.querySelector('script[type="application/json"]').textContent
  );

  const datepicker = flatpickr("#date-picker", {
    locale: "uk",
    dateFormat: "Y-m-d",
    inline: true,
    enable: Object.keys(availableSlots),
    onChange: function (selectedDates, dateStr, instance) {
      const slotsContainer = document.getElementById("slots-container");
      slotsContainer.innerHTML = "";
      if (availableSlots[dateStr]) {
        document.getElementById("available-slots").style.display = "block";
        availableSlots[dateStr].forEach((slot) => {
          const slotElement = document.createElement("span");
          slotElement.className = "time-slot";
          slotElement.textContent = slot;
          slotElement.dataset.date = dateStr;
          slotElement.dataset.time = slot;
          slotsContainer.appendChild(slotElement);
        });
      } else {
        document.getElementById("available-slots").style.display = "none";
      }
    },
  });

  document
    .getElementById("slots-container")
    .addEventListener("click", function (event) {
      const target = event.target.closest(".time-slot");
      if (target) {
        const date = target.getAttribute("data-date");
        const time = target.getAttribute("data-time");

        document.getElementById("selected-date").value = date;
        document.getElementById("selected-time").value = time;

        // Удаляем класс "selected" у всех элементов
        const slots = document.querySelectorAll(".time-slot");
        slots.forEach((slot) => slot.classList.remove("selected"));

        // Добавляем класс "selected" к текущему элементу
        target.classList.add("selected");
      }
    });
});
