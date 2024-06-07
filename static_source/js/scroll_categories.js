document.addEventListener("DOMContentLoaded", function () {
  let horizontScroll = document.querySelector(".Categories_list");
  let rightBtn = document.getElementById("rightBtn");
  let leftBtn = document.getElementById("leftBtn");

  rightBtn.addEventListener("click", () => {
    horizontScroll.scrollBy({
      left: 600,
      behavior: "smooth",
    });
  });

  leftBtn.addEventListener("click", () => {
    horizontScroll.scrollBy({
      left: -600,
      behavior: "smooth",
    });
  });
});
