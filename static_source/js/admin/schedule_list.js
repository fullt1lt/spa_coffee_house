document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("view_therapist")
    .addEventListener("change", function () {
      const therapistId = this.value;
      if (therapistId) {
        fetch(`/schedule/${therapistId}/`)
          .then((response) => response.json())
          .then((data) => {
            const scheduleDiv = document.getElementById("therapist-schedule");
            scheduleDiv.innerHTML = "";
            if (data.schedule.length > 0) {
              const ul = document.createElement("ul");
              ul.classList.add("schedule-list-items");
              data.schedule.forEach((item) => {
                const date = new Date(item.day);
                const day = date.getDate().toString().padStart(2, "0");
                const month = (date.getMonth() + 1).toString().padStart(2, "0");
                const formattedDate = `${day}.${month}`;

                const li = document.createElement("li");
                li.classList.add("schedule-list-item");

                const dateSpan = document.createElement("span");
                dateSpan.classList.add("schedule-date");
                dateSpan.textContent = formattedDate;

                const timeUl = document.createElement("ul");
                timeUl.classList.add("schedule-time-list");

                const startTimeLi = document.createElement("li");
                startTimeLi.classList.add("schedule-time-item");
                startTimeLi.textContent = `${item.start_time}`;

                const endTimeLi = document.createElement("li");
                endTimeLi.classList.add("schedule-time-item");
                endTimeLi.textContent = `${item.end_time}`;

                timeUl.appendChild(startTimeLi);
                timeUl.appendChild(endTimeLi);

                li.appendChild(dateSpan);
                li.appendChild(timeUl);
                ul.appendChild(li);
              });
              scheduleDiv.appendChild(ul);
            } else {
              scheduleDiv.textContent = "No schedule available";
              scheduleDiv.classList.add("no-schedule");
            }
          });
      } else {
        document.getElementById("therapist-schedule").innerHTML = "";
      }
    });
});
