document.addEventListener("DOMContentLoaded", function () {
  const navItems = document.querySelectorAll(".Admin_navigations_item");
  const scheduleList = document.getElementById("schedule-list");
  const categoriesList = document.getElementById("categories-list");
  const therapistList = document.getElementById("therapist-list");

  navItems.forEach((item) => {
    item.addEventListener("click", function () {
      // Убираем класс Admin_active у всех элементов
      navItems.forEach((nav) => nav.classList.remove("Admin_active"));

      // Добавляем класс Admin_active текущему элементу
      item.classList.add("Admin_active");

      // Обновляем отображение соответствующего контента
      if (item.id === "schedule") {
        scheduleList.style.display = "flex";
        categoriesList.style.display = "none";
        therapistList.style.display = "none";
      } else if (item.id === "categories") {
        scheduleList.style.display = "none";
        categoriesList.style.display = "flex";
        therapistList.style.display = "none";
      } else if (item.id === "therapist") {
        scheduleList.style.display = "none";
        categoriesList.style.display = "none";
        therapistList.style.display = "flex";
      }
    });
  });
});
