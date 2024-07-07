document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll(".Basket_TypeCafeProduct_image")
    .forEach((button) => {
      button.addEventListener("click", (event) => {
        document
          .querySelectorAll(".TypeCafeProduct_delete_item_list")
          .forEach((form) => {
            form.style.display = "none";
          });
        const typeCafeProductId = button.getAttribute(
          "delete-type_cafe_product-id"
        );
        const deleteForm = document.getElementById(
          `type_cafe_product_delete_${typeCafeProductId}`
        );
        if (deleteForm) {
          deleteForm.style.display = "flex";
        }
      });
    });

  document
    .querySelectorAll(".cancel_delete_type_cafe_product")
    .forEach((button) => {
      button.addEventListener("click", (event) => {
        const typeCafeProductId = button.getAttribute(
          "cancel-delete-type-cafe-product-id"
        );
        const deleteForm = document.getElementById(
          `type_cafe_product_delete_${typeCafeProductId}`
        );
        if (deleteForm) {
          deleteForm.style.display = "none";
        }
      });
    });
});
