let dropDownButton = document.getElementById("drop-down");
let speechHistoryContent = document.getElementById("speech-history-content");

state = "up";
dropDownButton.addEventListener("click", function() {
    if (state === "up") {
        speechHistoryContent.style.display = "grid";
        state = "down";
    }else {
        speechHistoryContent.style.display = "none";
        state = "up";
    }
});