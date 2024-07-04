function validateTimeInput(timeInput) {
  const time = timeInput.value;
  if (time) {
    const [hours, minutes] = time.split(":").map(Number);
    if (minutes !== 0 && minutes !== 30) {
      timeInput.value = `${hours.toString().padStart(2, "0")}:${
        minutes < 15 ? "00" : "30"
      }`;
    }
  }
}

document.getElementById("start_time").addEventListener("change", function () {
  validateTimeInput(this);
});

document.getElementById("end_time").addEventListener("change", function () {
  validateTimeInput(this);
});
