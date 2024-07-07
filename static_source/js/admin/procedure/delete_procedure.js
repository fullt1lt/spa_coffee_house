document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".Basket_procedure_image").forEach((button) => {
    button.addEventListener("click", (event) => {
      document
        .querySelectorAll(".Procedure_delete_item_list")
        .forEach((form) => {
          form.style.display = "none";
        });
      const procedureId = button.getAttribute("delete-procedure-id");
      const deleteForm = document.getElementById(
        `procedure_delete_${procedureId}`
      );
      if (deleteForm) {
        deleteForm.style.display = "flex";
      }
    });
  });

  document.querySelectorAll(".cancel_delete_procedure").forEach((button) => {
    button.addEventListener("click", (event) => {
      const procedureId = button.getAttribute("cancel-delete-procedure-id");
      const deleteForm = document.getElementById(
        `procedure_delete_${procedureId}`
      );
      if (deleteForm) {
        deleteForm.style.display = "none";
      }
    });
  });
});
