const add_cafeproduct_close_button = document.getElementById(
  "Add_CafeProduct_close_button"
);
const add_cafeproduct_button = document.getElementById(
  "Add_CafeProduct_button"
);

const add_cafeproduct_block = document.getElementById("Add_CafeProduct_block");

add_cafeproduct_close_button.addEventListener("click", function () {
  add_cafeproduct_block.style.display = "none";
  add_cafeproduct_button.style.display = "flex";
});

add_cafeproduct_button.addEventListener("click", function () {
  add_cafeproduct_block.style.display = "flex";
  add_cafeproduct_button.style.display = "none";
});
