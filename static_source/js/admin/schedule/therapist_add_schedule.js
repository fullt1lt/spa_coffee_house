document.addEventListener("DOMContentLoaded", function () {
  const addScheduleButton = document.getElementById("Add_schedule_button");
  const createScheduleForm = document.getElementById(
    "Therapist_create_schedule"
  );
  const closeScheduleFormButton = document.getElementById(
    "Add_schedule_close_button"
  );

  addScheduleButton.addEventListener("click", function () {
    createScheduleForm.style.display = "block";
  });

  closeScheduleFormButton.addEventListener("click", function () {
    createScheduleForm.style.display = "none";
  });
});
