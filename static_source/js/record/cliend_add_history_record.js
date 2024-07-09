document.addEventListener("DOMContentLoaded", function () {
  var historyRecordsToggle = document.getElementById("history-records-toggle");
  var closeHistoryRecordsToggle = document.getElementById(
    "close-history-records-toggle"
  );
  var historyRecords = document.getElementById("history-records-list");
  var curentRecords = document.getElementById("current-records-list");

  historyRecordsToggle.addEventListener("click", function () {
    historyRecords.style.display = "flex";
    historyRecordsToggle.style.display = "none";
    closeHistoryRecordsToggle.style.display = "block";
    curentRecords.style.display = "none";
  });

  closeHistoryRecordsToggle.addEventListener("click", function () {
    historyRecords.style.display = "none";
    historyRecordsToggle.style.display = "flex";
    closeHistoryRecordsToggle.style.display = "none";
    curentRecords.style.display = "flex";
  });
});
