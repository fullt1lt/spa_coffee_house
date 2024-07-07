document.addEventListener("DOMContentLoaded", function () {
  const categoryItems = document.querySelectorAll(".category_item");
  const proceduresList = document.getElementById("procedures-list");
  const procedureEditForm = document.getElementById("procedure-edit-form");
  const procedureForm = document.querySelector(".procedure_update_form");

  categoryItems.forEach((item) => {
    item.addEventListener("click", function () {
      const categoryId = this.dataset.categoryId;

      fetch(`/admin-main-page/procedures/${categoryId}/`)
        .then((response) => response.json())
        .then((data) => {
          proceduresList.innerHTML = "";
          data.forEach((procedure) => {
            const procedureItem = document.createElement("div");
            procedureItem.classList.add("procedure_item");
            procedureItem.innerHTML = `
                            <div class="procedure_header">
                                <h3>${procedure.type_category}</h3>
                            </div>
                            <div class="procedure_duration">
                                <span>Тривалість: ${procedure.duration}</span>
                            </div>
                            <div class="procedure_price">
                                <span>Ціна: ${procedure.price} грн</span>
                            </div>
                            <div class="procedure_actions">
                                <button class="edit_procedure_button" data-procedure-id="${procedure.id}">Редагувати</button>
                            </div>
                        `;
            proceduresList.appendChild(procedureItem);
          });
        });
    });
  });

  proceduresList.addEventListener("click", function (event) {
    if (event.target.classList.contains("edit_procedure_button")) {
      const procedureId = event.target.dataset.procedureId;

      // Получаем данные процедуры для редактирования
      fetch(`/admin-main-page/procedure/${procedureId}/`)
        .then((response) => response.json())
        .then((data) => {
          // Заполняем форму данными процедуры
          document.getElementById("procedure-id").value = data.id;
          document.getElementById("id_duration").value = data.duration;
          document.getElementById("id_price").value = data.price;

          // Показываем форму редактирования
          procedureEditForm.style.display = "block";
        });
    }
  });
});
