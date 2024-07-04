const add_schedule_button = document.getElementById("Add_schedule_button");
const add_schedule_close_button = document.getElementById(
  "Add_schedule_close_button"
);

const admin_create_schedule = document.getElementById("Admin_create_schedule");

add_schedule_close_button.addEventListener("click", function () {
  admin_create_schedule.style.display = "none";
  add_schedule_button.style.display = "flex";
});

add_schedule_button.addEventListener("click", function () {
  admin_create_schedule.style.display = "flex";
  add_schedule_button.style.display = "none";
});
