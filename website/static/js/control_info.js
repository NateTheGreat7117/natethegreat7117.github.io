// Buttons
let example = document.getElementById("return-button")
let time = document.getElementById("time-label");
let date = document.getElementById("date-label");
let open_close = document.getElementById("open-close-label");
let new_tab = document.getElementById("new-tab-label");
let close_tab = document.getElementById("close-tab-label");
let exit_full = document.getElementById("exit-full-label");
let enter_full = document.getElementById("enter-full-label");
let get_volume = document.getElementById("get-volume-label");
let change_volume = document.getElementById("change-volume-label");
let set_volume = document.getElementById("set-volume-label");
let mute = document.getElementById("mute-label");
let calculator = document.getElementById('calculator-label');
let youtube = document.getElementById('youtube-label');
let activate = document.getElementById('activate-label');
let show = document.getElementById('show-label');
let sleep = document.getElementById('sleep-label');
let switch_tab = document.getElementById("switch-tab-label");
let timer = document.getElementById('timer-label');
let reminder = document.getElementById('reminder-label');
let joke = document.getElementById('joke-label');
let translate = document.getElementById('translate-label');
let search = document.getElementById('search-label');
let call = document.getElementById('call-label');
let fact = document.getElementById('fun-fact-label');
let press = document.getElementById('press-label');
let type = document.getElementById('type-label');
let screen_shot = document.getElementById('screen-shot-label');
let schedule = document.getElementById("schedule-label");
let pause = document.getElementById('pause-label');
let screen = document.getElementById('screen-label');
let maximize = document.getElementById('maximize-label');
let zoom = document.getElementById('zoom-label');
let rotate = document.getElementById('rotate-label');

let buttons = [example, time, date, open_close, new_tab, close_tab,
    exit_full, enter_full, get_volume, change_volume, set_volume, mute,
    calculator, youtube, activate, show, sleep, switch_tab, timer, reminder,
    joke, translate, search, call, fact, press, type, screen_shot, schedule, 
    pause, screen, maximize, zoom, rotate
];

// Texts
let example_info = document.getElementById("example");
let time_info = document.getElementById("time-info");
let date_info = document.getElementById("date-info");
let open_close_info = document.getElementById("open-close-info");
let new_tab_info = document.getElementById('new-tab-info');

let texts = [example_info, time_info, date_info, open_close_info, new_tab_info];

for (let i = 1; i < texts.length; i++) {
    texts[i].style.display = "none";
}

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function() {
        for (let j = 0; j < texts.length; j++) {
            texts[j].style.display = "none";
        }
        texts[i].style.display = "grid";
    })
}