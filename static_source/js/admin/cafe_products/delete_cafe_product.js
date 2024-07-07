document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".Basket_CafeProduct_image").forEach((button) => {
    button.addEventListener("click", (event) => {
      document
        .querySelectorAll(".CafeProduct_delete_item_list")
        .forEach((form) => {
          form.style.display = "none";
        });
      const cafeProductId = button.getAttribute("delete-cafe_product-id");
      const deleteForm = document.getElementById(
        `cafe_product_delete_${cafeProductId}`
      );
      if (deleteForm) {
        deleteForm.style.display = "flex";
      }
    });
  });

  document.querySelectorAll(".cancel_delete_cafe_product").forEach((button) => {
    button.addEventListener("click", (event) => {
      const cafeProductId = button.getAttribute(
        "cancel-delete-cafe-product-id"
      );
      const deleteForm = document.getElementById(
        `cafe_product_delete_${cafeProductId}`
      );
      if (deleteForm) {
        deleteForm.style.display = "none";
      }
    });
  });
});
