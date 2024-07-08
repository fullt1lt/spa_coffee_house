document.addEventListener("DOMContentLoaded", function () {
  const scheduleDiv = document.getElementById("therapist-schedule");

  function fetchSchedule() {
    fetch("/therapist-schedule-data/")
      .then((response) => response.json())
      .then((data) => {
        scheduleDiv.innerHTML = "";
        if (data.schedules.length > 0) {
          scheduleDiv.style.display = "flex";
          data.schedules.forEach((schedule) => {
            const ul = document.createElement("ul");
            ul.classList.add("schedule_list");

            const dateHeader = document.createElement("li");
            dateHeader.classList.add("schedule_data_header");
            const dateH1 = document.createElement("h1");
            dateH1.textContent = schedule.day;
            dateHeader.appendChild(dateH1);
            ul.appendChild(dateHeader);

            const startWorkDay = document.createElement("li");
            startWorkDay.classList.add("start_work_day");
            const startWorkTime = document.createElement("span");
            startWorkTime.classList.add("start_work_time");
            startWorkTime.textContent = schedule.start_time;
            startWorkDay.appendChild(startWorkTime);
            ul.appendChild(startWorkDay);

            const recordsList = document.createElement("li");
            recordsList.classList.add("schedule_list_records");
            const recordsUl = document.createElement("ul");
            recordsUl.classList.add("schedule_list_records_list");

            schedule.records.forEach((record) => {
              const recordLi = document.createElement("li");
              recordLi.classList.add("schedule_list_records_item");

              const durations = document.createElement("span");
              durations.classList.add("durations");
              durations.textContent = `${record.start_time} - ${record.end_time}`;
              recordLi.appendChild(durations);

              const procedureName = document.createElement("span");
              procedureName.classList.add("name_procedure");
              procedureName.textContent = record.procedure_name;
              recordLi.appendChild(procedureName);

              const userList = document.createElement("div");
              userList.classList.add("user_list");

              const userName = document.createElement("span");
              userName.classList.add("user_name");
              userName.textContent = record.client_first_name;
              userList.appendChild(userName);

              const userLastName = document.createElement("span");
              userLastName.classList.add("user_lastname");
              userLastName.textContent = record.client_last_name;
              userList.appendChild(userLastName);

              recordLi.appendChild(userList);
              recordsUl.appendChild(recordLi);
            });

            recordsList.appendChild(recordsUl);
            ul.appendChild(recordsList);

            const endWorkDay = document.createElement("li");
            endWorkDay.classList.add("end_work_day");
            const endWorkTime = document.createElement("span");
            endWorkTime.classList.add("end_work_time");
            endWorkTime.textContent = schedule.end_time;
            endWorkDay.appendChild(endWorkTime);
            ul.appendChild(endWorkDay);

            if (schedule.records.length === 0) {
              const deleteForm = document.createElement("form");
              deleteForm.method = "post";
              deleteForm.classList.add("delete_schedule_form");
              deleteForm.dataset.scheduleId = schedule.id;

              const csrfToken = document.createElement("input");
              csrfToken.type = "hidden";
              csrfToken.name = "csrfmiddlewaretoken";
              csrfToken.value = document.querySelector(
                "[name=csrfmiddlewaretoken]"
              ).value;
              deleteForm.appendChild(csrfToken);

              const scheduleIdInput = document.createElement("input");
              scheduleIdInput.type = "hidden";
              scheduleIdInput.name = "schedule_id";
              scheduleIdInput.value = schedule.id;
              deleteForm.appendChild(scheduleIdInput);

              const deleteButton = document.createElement("button");
              deleteButton.type = "submit";
              deleteButton.classList.add("delete_schedule_button");
              deleteButton.textContent = "Удалить расписание";
              deleteForm.appendChild(deleteButton);

              ul.appendChild(deleteForm);

              deleteForm.addEventListener("submit", function (event) {
                event.preventDefault();
                const scheduleId = this.dataset.scheduleId;
                fetch(`/delete-schedule/${scheduleId}/`, {
                  method: "POST",
                  headers: {
                    "X-CSRFToken": csrfToken.value,
                  },
                })
                  .then((response) => {
                    if (response.ok) {
                      fetchSchedule();
                    }
                  })
                  .catch((error) => {
                    console.error("Error deleting schedule:", error);
                  });
              });
            }

            scheduleDiv.appendChild(ul);
          });
        } else {
          scheduleDiv.textContent = "No schedule available";
          scheduleDiv.classList.add("no-schedule");
          scheduleDiv.style.display = "none";
        }
      })
      .catch((error) => {
        console.error("Error fetching schedule:", error);
        scheduleDiv.textContent = "Error fetching schedule";
        scheduleDiv.style.display = "none";
      });
  }

  fetchSchedule();
});
