document.addEventListener("DOMContentLoaded", function () {
  const customButton = document.getElementById("cafe-product-custom-button");
  const customText = document.getElementById("cafe-product-custom-text");
  const fileInput = document.getElementById("id_product_image");

  if (customButton && customText && fileInput) {
    customButton.addEventListener("click", function () {
      fileInput.click();
    });

    fileInput.addEventListener("change", function () {
      const fileName = fileInput.files[0]?.name;
      if (fileName) {
        customText.textContent = fileName;
      } else {
        customText.textContent = "Файл не вибрано";
      }
    });
  } else {
    console.error("Custom button, text, or file input element not found.");
  }
});
