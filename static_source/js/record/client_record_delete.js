document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".Basket_record_image").forEach((button) => {
    button.addEventListener("click", (event) => {
      document.querySelectorAll(".back_records_list").forEach((form) => {
        form.style.display = "none";
      });
      document.querySelectorAll(".front_records_list").forEach((form) => {
        form.style.display = "flex";
      });
      const recordId = button.getAttribute("delete-record-id");
      const deleteForm = document.getElementById(
        `records_list_delete_${recordId}`
      );
      const frontForm = document.getElementById(
        `records_list_front_${recordId}`
      );
      if (deleteForm && frontForm) {
        deleteForm.style.display = "flex";
        frontForm.style.display = "none";
      }
    });
  });

  document.querySelectorAll(".cancel_delete").forEach((button) => {
    button.addEventListener("click", (event) => {
      const recordId = button.getAttribute("cancel-delete-record-id");
      const deleteForm = document.getElementById(
        `records_list_delete_${recordId}`
      );
      const frontForm = document.getElementById(
        `records_list_front_${recordId}`
      );
      if (deleteForm && frontForm) {
        deleteForm.style.display = "none";
        frontForm.style.display = "flex";
      }
    });
  });
});
