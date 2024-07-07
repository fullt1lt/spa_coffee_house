document.addEventListener("DOMContentLoaded", function () {
  const addButton = document.getElementById("Add_TypeCafeProduct_button");
  const closeButton = document.getElementById(
    "Add_TypeCafeProduct_close_button"
  );
  const addBlock = document.getElementById("Add_TypeCafeProduct_block");

  if (addButton && closeButton && addBlock) {
    addButton.addEventListener("click", () => {
      addBlock.style.display = "block";
    });

    closeButton.addEventListener("click", () => {
      addBlock.style.display = "none";
    });
  } else {
    console.error("Add or close button, or add block not found.");
  }
});
