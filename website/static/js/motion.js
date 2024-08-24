$(document).ready(function(){
    let dropDownButton = document.getElementById("drop-down");
    let speechHistoryContent = document.getElementById("speech-history-content");
    let visualizer = document.getElementById("circle");

    let saved = false;

    state2 = "up";
    dropDownButton.addEventListener("click", function() {
        if (state2 === "up") {
            speechHistoryContent.style.display = "grid";
            state2 = "down";
        }else {
            speechHistoryContent.style.display = "none";
            state2 = "up";
        }
    });

    let time = 0;
    let prev_motion = "";

    function timer() { 
        time += 1;
    }

    setInterval(function(){
        $.ajax({
            type: 'POST',
            url: '/speech',
            contentType: 'application/json',
            data: JSON.stringify({stop: stopped}),
            success: function(data){
                $('#speechText').text(data.speech);
                $('#responseText').text(data.response);
                $('#speechDetection').text(data.detection);

                wav = data.waveform;

                // Set the speech detection color
                if (data.detection > 0.8) {
                    detection_text.style.color = "green";
                }else {
                    detection_text.style.color = "red";
                }

                // Save a line to the conversation history
                if (saved != true && data.motion.includes("saveLine")) {
                    let response = document.createElement("p");
                    let response_text_content = document.createTextNode("assistant: " + data.output);
                    response.prepend(response_text_content);
                    response.style.margin = "1%";
                    history.prepend(response);
                    saved = true;


                    let speech = document.createElement("p");
                    let speech_text_content = document.createTextNode("user: " + speech_text.textContent);
                    speech.prepend(speech_text_content);
                    speech.style.margin = "1%";
                    speech.style.marginTop = "2%";
                    history.prepend(speech);
                }

                if (saved && data.response == "...") {
                    saved = false;
                }


                // Display the current date and time
                if (data.motion.includes("datetime")) {
                    datetime.style.animation = "slide-right 2s forwards";
                    temp.style.animation = "fade-out 2s forwards";
                    bubble.style.animation = 'move-top-corner 2s forwards';
                    bubble_container.style.animation = "create-border 2s forwards";
                    speech_text.style.animation = "small-speech-text 2s forwards";
                    response_text.style.animation = "small-speech-text 2s forwards";
                    detection_text.style.animation = "small-detection-text 2s forwards";
                    visualizer.style.animation = "small-visualizer 2s forwards";

                    time = 0;
                    prev_motion = "datetime";
                    setInterval(timer, 1000);
                    console.log("start");
                }

                if (data.motion.includes("home")) {
                    today.style.display = "grid";
                    hourly.style.display = "none";
                    // daily.style.display = "none";
                }

                if (data.motion.includes("hourly")) {
                    datetime.style.animation = "fade-out 2s forwards";
                    temp.style.animation = "fade-out 2s forwards";
                    bubble.style.animation = 'move-top-corner 2s forwards';
                    bubble_container.style.animation = "create-border 2s forwards";
                    speech_text.style.animation = "small-speech-text 2s forwards";
                    response_text.style.animation = "small-speech-text 2s forwards";
                    detection_text.style.animation = "small-detection-text 2s forwards";
                    visualizer.style.animation = "small-visualizer 2s forwards";

                    today.style.display = "none";
                    hourly.style.display = "grid";
                    // daily.style.display = "none";
                }

                if (data.motion.includes("daily")) {
                    today.style.display = "none";
                    hourly.style.display = "none";
                    // daily.style.display = "block";
                }

                // if (prev_motion === "datetime") {
                //     // clearInterval(timer);
                //     time = 0;
                //     prev_motion = "";

                //     datetime.style.animation = "slide-left 2s forwards";
                //     temp.style.animation = "fade-in 2s forwards";
                //     bubble.style.animation = 'move-center 2s forwards';
                //     bubble_container.style.animation = "remove-border 2s forwards";
                //     speech_text.style.animation = "large-speech-text 2s forwards";
                //     response_text.style.animation = "large-speech-text 2s forwards";
                //     detection_text.style.animatino = "large-detection-text 2s forwards";
                //     visualizer.style.animation = "large-visualizer 2s forwards";
                // }
            }
        });
    }, 20); // Repeat every 1ms
});