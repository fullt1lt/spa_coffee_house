document.addEventListener("DOMContentLoaded", function () {
  const calendarElement = document.getElementById("calendar");
  const selectedDatesInput = document.getElementById("selected-dates");

  flatpickr(calendarElement, {
    mode: "multiple",
    dateFormat: "Y-m-d",
    locale: "uk",
    minDate: "today",
    onChange: function (selectedDates) {
      const formattedDates = selectedDates.map((date) =>
        date.toLocaleDateString("en-CA")
      );
      selectedDatesInput.value = formattedDates.join(",");
    },
  });
});
