import webbrowser
import pyautogui
import time

def enter_full_screen():
    time.sleep(1)
    pyautogui.press("home")
    pyautogui.moveTo(x=1400, y=600)
    time.sleep(0.5)
    pyautogui.click()
    pyautogui.click()
    
def press_button(button, enter=True):
    time.sleep(2)
    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.1)
    pyautogui.typewrite(button)
    if enter:
        time.sleep(0.1)
        pyautogui.hotkey("enter")
    time.sleep(0.1)
    pyautogui.hotkey("ctrl", "enter")

def show(command):
    command = command.lower()
    
    season = ""
    episode = "episode 1"
    if ":" not in command:
        webbrowser.open_new_tab(f"https://fboxz.to/filter?keyword={command.replace(' ', '+')}")
        press_button(command)
    else:
        split = command.split(":")
        if len(split) == 3:
            season = split[1].strip()
            episode = split[2].strip()
        elif len(split) == 2 and "season" in split[1].strip():
            season = split[1].strip()
        elif len(split) == 2 and "episode" in split[1].strip():
            episode = split[1].strip()
    
    if season != "":
        press_button("season")
        press_button(season)
        # Must fix !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    # Episode
    press_button(episode, enter=False)
    
    # Movie
    press_button("movie 1")
    
    enter_full_screen()