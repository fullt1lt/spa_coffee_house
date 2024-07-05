document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".Basket_image").forEach((button) => {
    button.addEventListener("click", (event) => {
      document
        .querySelectorAll(".TypeCategory_delete_item_list")
        .forEach((form) => {
          form.style.display = "none";
        });
      const categoryId = button.getAttribute("delete-type_category-id");
      const deleteForm = document.getElementById(
        `type_category_delete_${categoryId}`
      );
      if (deleteForm) {
        deleteForm.style.display = "flex";
      }
    });
  });

  document
    .querySelectorAll(".cancel_delete_type_category")
    .forEach((button) => {
      button.addEventListener("click", (event) => {
        const categoryId = button.getAttribute(
          "cancel-delete-type-category-id"
        );
        const deleteForm = document.getElementById(
          `type_category_delete_${categoryId}`
        );
        if (deleteForm) {
          deleteForm.style.display = "none";
        }
      });
    });
});
