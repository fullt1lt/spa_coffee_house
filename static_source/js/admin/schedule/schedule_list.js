document.addEventListener("DOMContentLoaded", function () {
  const viewTherapistSelect = document.getElementById("view_therapist");
  const scheduleDiv = document.getElementById("therapist-schedule");

  viewTherapistSelect.addEventListener("change", function () {
    const therapistId = this.value;
    if (therapistId) {
      fetch(`/schedule/${therapistId}/`)
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

                const procedureprice = document.createElement("span");
                procedureName.classList.add("price_procedure");
                procedureName.textContent = record.procedure_price + " грн";
                recordLi.appendChild(procedureprice);

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

              scheduleDiv.appendChild(ul);
            });
          } else {
            scheduleDiv.textContent = "No schedule available";
            scheduleDiv.classList.add("no-schedule");
            scheduleDiv.style.display = "none"; //
          }
        })
        .catch((error) => {
          console.error("Error fetching schedule:", error);
          scheduleDiv.textContent = "Error fetching schedule";
          scheduleDiv.style.display = "none";
        });
    } else {
      scheduleDiv.innerHTML = "";
      scheduleDiv.style.display = "none";
    }
  });
});
