document.addEventListener("DOMContentLoaded", function () {
  let items = document.querySelectorAll(".item_description");
  let maxHeight = 0;

  console.log(items);
  items.forEach(function (item) {
    if (item.offsetHeight > maxHeight) {
      maxHeight = item.offsetHeight;
    }
  });

  // Устанавливаем всем элементам высоту самого высокого элемента
  items.forEach(function (item) {
    item.style.height = maxHeight + "px";
    console.log(item.style.height);
  });
});
