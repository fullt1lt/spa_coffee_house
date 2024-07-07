const add_typecategories_button = document.getElementById(
  "Add_TypeCategories_button"
);
const add_typecategories_close_button = document.getElementById(
  "Add_TypeCategories_close_button"
);

const add_typecategories_block = document.getElementById(
  "Add_TypeCategories_block"
);

add_typecategories_close_button.addEventListener("click", function () {
  add_typecategories_block.style.display = "none";
  add_typecategories_button.style.display = "flex";
});

add_typecategories_button.addEventListener("click", function () {
  add_typecategories_block.style.display = "flex";
  add_typecategories_button.style.display = "none";
});
