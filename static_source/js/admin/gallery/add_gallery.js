const add_gallery_close_button = document.getElementById(
  "Add_Gallery_close_button"
);
const add_gallery_button = document.getElementById("Add_Gallery_button");

const add_gallery_block = document.getElementById("Add_Gallery_block");

add_gallery_close_button.addEventListener("click", function () {
  add_gallery_block.style.display = "none";
  add_gallery_button.style.display = "flex";
});

add_gallery_button.addEventListener("click", function () {
  add_gallery_block.style.display = "flex";
  add_gallery_button.style.display = "none";
});
