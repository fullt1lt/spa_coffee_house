const add_therapist_button = document.getElementById("Add_therapist_button");
const add_therapist_close_button = document.getElementById(
  "Add_Therapist_close_button"
);

const add_therapist_block = document.getElementById("Add_Therapist_block");

add_therapist_close_button.addEventListener("click", function () {
  add_therapist_block.style.display = "none";
  add_therapist_button.style.display = "flex";
});

add_therapist_button.addEventListener("click", function () {
  add_therapist_block.style.display = "flex";
  add_therapist_button.style.display = "none";

  const formList = add_therapist_block.querySelector(
    ".Add_Therapist_form_item"
  );
  const existingForm = formList.querySelector("form");

  if (!existingForm) {
    const form = document.createElement("form");
    form.method = "post";
    form.enctype = "multipart/form-data";
    form.classList.add("create_massage_therapist_form");

    while (formList.firstChild) {
      form.appendChild(formList.firstChild);
    }
    formList.appendChild(form);
  }
});
