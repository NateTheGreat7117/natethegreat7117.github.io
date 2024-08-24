from py_programs.shows import enter_full_screen, press_button, show
from py_programs.applications import open_app, close_app, open_file
from py_programs.word2num import word2num
from py_programs.chatbot import evaluate
from py_programs.youtube import youtube
from py_programs.volume import volume

from bs4 import BeautifulSoup as bs4
from PIL import ImageGrab
import numpy as np
import subprocess
import webbrowser
import pyautogui
import wikipedia
import randfacts
import datetime
import requests
import pyjokes


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
def weather(city, wob):
    res = requests.get(
        f'https://www.google.com/search?q={city}+weather&rlz=1C1VDKB_enUS1016US1016&oq={city}&aqs=chrome.0.69i59j69i57j69i59l2j0i271l2j69i61l2.905j0j7&sourceid=chrome&ie=UTF-8',
        headers=headers
    )
    soup = bs4(res.text, 'html.parser')
    return soup.select(f"#wob_{wob}")[0].getText().strip()

def timer(command):
    time = word2num(command)
    desired_seconds = time
    
    if "minute" in command:
        desired_seconds = time * 60
    if "hour" in command:
        desired_seconds = time * 3600
    return desired_seconds

def reminder(command):
    # If no meridiem
    command = command.lower()
    hours = int(word2num(command.split(" ")[0]))
    minutes = 0
    add = 0
    
    i = 2
    if "am" in command or "pm" in command:
        i = 3
        if "pm" in command:
            add = 12
        
    if len(command.split()) == i:
        minutes = word2num(command.split(" ")[1])
    elif len(command.split()) == i+1: # Skip the 'o' in four o' five
        minutes = word2num(command.split(" ")[2])
        
    return hours+add, int(minutes)


def respond(chat):
    response = evaluate(chat)
    original_response = np.copy(response)
    print(response)
    print()
    print()
    desired_seconds = None
    desired_time = (-1, -1)

    if response == "":
        motion = ""
    else:
        motion = "saveLine "
    
    # Get the date
    if "/u date" in response:
        response = response.replace("/u date", datetime.date.today().strftime("%B %d, %Y"))
        motion += "datetime "
    # Get the time
    if "/u time" in response:
        response = response.replace("/u time", datetime.datetime.now().strftime("%I:%M"))
        motion += "datetime "
    # Get the temperature
    if "/u temp" in response:
        response = response.replace("/u temp", weather("boston", "tm"))
    if "/dweather" in response:
        motion += "hourly "
    # Get a joke
    if "/u joke" in response:
        response = response.replace("/u joke", pyjokes.get_joke(language="en", category="neutral"))
    # Get a fun fact
    if "/u funfact" in response:
        response = response.replace("/u funfact", randfacts.get_fact())
    # Get the humidity
    if "/u humidity" in response:
        response = response.replace("/u humidity", weather("boston", "hm"))
    # Get the wind speed
    if "/u wind" in response:
        response = response.replace("/u wind", weather("boston", "ws"))
    # Get the amount of precipitation
    if "/u precipitation" in response:
        response = response.replace("/u precipitation", weather("boston", "pp"))
    if "/u sky" in response:
        response = response.replace("/u sky", weather("boston", "dc"))
    if "/u volume" in response:
        after = response.split("/u volume")[-1]
        vol = after.split("'")[1]
        response = response.replace("/u volume'"+vol+"' ", str(volume(vol)))
    if "/u newtab" in response:
        response = response.replace("/u newtab", "")
        pyautogui.hotkey('ctrl', 't')
    if "/u closetab" in response:
        if "/u closetab '" in response:
            after = response.split("/u closetab")[-1]
            new = after.split("'")[1]
            
            response = response.replace(f"/uclosetab '{new}' ")
            pyautogui.hotkey('ctrl', str(word2num(new)))
        else:
            response = response.replace("/u closetab", "")
            pyautogui.hotkey('ctrl', 'w')
    if "/u switchtab" in response:
        after = response.split("/u switchtab")[-1]
        new = after.split("'")[1]
        
        response = response.replace("/u switchtab'"+new+"' ", "")

        if "next" in new:
            pyautogui.hotkey("ctrl", "tab")
        elif "back" in new:
            pyautogui.hotkey("ctrl", "shift", "tab")
        elif "last" in new:
            pyautogui.hotkey("ctrl", "9")
        else:
            new = int(word2num(new))
            if new < 9:
                pyautogui.hotkey('ctrl', str(new))
            else:
                pyautogui.hotkey('ctrl', '8')
                for i in range(new - 8):
                    pyautogui.hotkey('ctrl', 'tab')
    if "/u open" in response:
        after = response.split("/u open")[-1]
        command = after.split("'")[1]
        response = response.replace("/u open'"+command+"' ", "")
        open_app(command)
    if "/u close" in response:
        after = response.split("/u close")[-1]
        command = after.split("'")[1]
        response = response.replace("/u close'"+command+"' ", "")
        close_app(command)
    if "/u pause" in response:
        response = response.replace("/u pause", "")
        
        pyautogui.press("space")
    if "/u screenoff" in response:
        response = response.replace("/u screenoff", "")
        subprocess.run("sleep 1 && xset dpms force off", shell=True)
    if "/u screenon" in response:
        response = response.replace("/u screenon", "")
        subprocess.run("xset dpms force on", shell=True)
    if "/u timer" in response:
        after = response.split("/u timer")[-1]
        command = after.split("'")[1]
        response = response.replace("/u timer'"+command+"' ", "")
        desired_seconds = timer(command)
    if "/u reminder" in response:
        after = response.split("/u reminder")[-1]
        command = after.split("'")[1]
        response = response.replace("/u reminder'"+command+"' ", "")
        desired_time = reminder(command)
    if "/u youtube" in response:
        after = response.split("/u youtube")[-1]
        command = after.split("'")[1]
        print(response)
        response = response.replace("/u youtube'"+command+"' ", "")
        youtube(command)
    if "/u show" in response:
        after = response.split("/u show")[-1]
        command = after.split("'")[1]
        
        response = response.replace("/u show'"+command+"' ", "")
        show(command)
    if "/u enterfull" in response:
        response = response.replace("/u enterfull", "")
        enter_full_screen()
    if "/u exitfull" in response:
        response = response.replace("/u exitfull", "")
        pyautogui.press("escape")
    if "/u press" in response:
        after = response.split("/u press")[-1]
        command = after.split("'")[1]
        
        response = response.replace(f"/u press '{command}' ", "")
        press_button(command, enter=False)
    if "/u type" in response:
        after = response.split("/u type")[-1]
        command = after.split("'")[1]
        
        response = response.replace(f"/u type '{command}' ", "")
        pyautogui.typewrite(command)
    if "/u search" in response:
        after = response.split("/u search")[-1]
        command = after.split("'")[1]
        
        response = response.replace(f"/u search '{command}' ", "")
        webbrowser.open_new_tab(f"https://www.google.com/search?q={command.replace(' ', '+')}")
    if "/u screenshot" in response:
        response = response.replace("/u screenshot", "")
        
        screenshot = ImageGrab.grab()
        screenshot.save("screenshot.png")
        screenshot.close()
    if "/u maximize" in response:   
        response = response.replace("/u maximize", "")
        # I don't know bruh
    if "/u rotate" in response:
        response = response.replace("/u rotate", "")
        pyautogui.hotkey("ctrl", "r")
    if "/u zoomin" in response:
        response = response.replace("/u zoomin", "")
        pyautogui.hotkey("ctrl", "+")
    if "/u zoomout" in response:
        response = response.replace("/u zoomout", "")
        pyautogui.hotkey("ctrl", "+")
    if "/u scrolldown" in response:
        response = response.replace("/u scrolldown", "")
        pyautogui.hotkey('pagedown')
    if "/u scrollup" in response:
        response = response.replace("/u scrollup", "")
        pyautogui.hotkey("pageup")
    if "/u prev" in response:
        response = response.replace("/u prev", "")
        pyautogui.hotkey("alt", "left")
    if "/u fileopen" in response:
        after = response.split("/u fileopen")[-1]
        command = after.split("'")[1]
        
        response = response.replace(f"/u fileopen '{command}' ", "")
        open_file(command)
    if "/u display" in response:
        after = response.split("/u display")[-1]
        command = after.split("'")[1]

        response = response.replace(f"/u display '{command}' ", "")
        motion += command
    if "/u list" in response:
        specific = True
        after = response.split("/u list")[-1]
        command = after.split("'")[1]
        
        # Prompts with subjects
        if ":" in command:
            specifics = command.split(":")[0]
            file = specifics.split(" ")[1]
            request = specifics.split(" ")[2]
            item = command.split(":")[1]
            specific = False
        # Prompts for entire list
        else:
            file = command.split(" ")[1]
            request = command.split(" ")[2]

        response = response.replace("/u list'"+command+"' ", "")
        with open(f"/home/nathanmon/Documents/{file}.txt", "a") as f:
            if specific:
                if request == "add":
                    f.write(item)
                elif request == "filter":
                    # Need to add
                    pass
                elif request == "remove":
                    # Need to add
                    pass
            else:
                if request == "clear":
                    f.truncate(0)
                elif request == "organize":
                    # Need to add
                    pass
    if "/u calculator" in response:
        after = response.split("/u calculator")[-1]
        ans = after.split(":")[0]

        command = ""
        for inp in after.split(":")[1:]:
            if inp == "minus" or inp == "plus" or inp == "times" or inp == "divided by":
                command = inp
            elif inp == "squared":
                ans = ans * ans
            elif inp == "cubed":
                ans = ans * ans * ans
            elif inp == "square root":
                ans = np.sqrt(ans)
            elif inp == "cube root":
                ans = np.cbrt(ans)
            else:
                if command == "minus":
                    ans -= int(inp)
                elif command == "plus":
                    ans += int(inp)
                elif command == "times":
                    ans *= int(inp)
                elif command == "divided by":
                    ans *= int(inp)
        response = response.replace("/u calculator"+after, ans)
        
    if "/u wiki" in response:
        after = response.split("/u wiki")[-1]
        command = after.split("'")[1]
        try:
            result = wikipedia.summary(command, sentences = 2)
            response = response.replace("/u wiki'"+command+"' ", result)
        except wikipedia.DisambiguationError:
            pass
        except Exception as e:
            print(e)
            
    if "/u turnoff" in response:
        after = response.split("/u wiki")[-1]
        machine = after.split("'")[1]
        
        if machine == "desktop assistant":
            # Turn off desktop assistant
            pass

    if "/u sleep" in response:
        response = response.replace("/u sleep", "")
        return original_response, response, desired_seconds, desired_time, motion
        
#     tts.tts_to_file(text=response, \
#             speaker_wav="jarvis_speech_files/killing.wav", language="en", file_path="output.wav")
#     playsound('output.wav')

    return original_response, response, desired_seconds, desired_time, motion