const add_categories_button = document.getElementById("Add_Categories_button");
const add_categories_close_button = document.getElementById(
  "Add_Categories_close_button"
);

const add_spa_categories_block = document.getElementById(
  "Add_Spa_Categories_block"
);

add_categories_close_button.addEventListener("click", function () {
  add_spa_categories_block.style.display = "none";
  add_categories_button.style.display = "flex";
});

add_categories_button.addEventListener("click", function () {
  add_spa_categories_block.style.display = "flex";
  add_categories_button.style.display = "none";
});
