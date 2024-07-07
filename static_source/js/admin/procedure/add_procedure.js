const add_procedures_button = document.getElementById("Add_Procedures_button");
const add_procedures_close_button = document.getElementById(
  "Add_Procedures_close_button"
);

const add_procedures_block = document.getElementById("Add_Procedures_block");

add_procedures_close_button.addEventListener("click", function () {
  add_procedures_block.style.display = "none";
  add_procedures_button.style.display = "flex";
});

add_procedures_button.addEventListener("click", function () {
  add_procedures_block.style.display = "flex";
  add_procedures_button.style.display = "none";
});
