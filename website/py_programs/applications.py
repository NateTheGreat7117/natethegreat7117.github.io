import subprocess
import webbrowser
import pyautogui
import psutil
import shutil
import glob
import os

predefined_programs = {"youtube": "lnk https://www.youtube.com/",
                       "google classroom": "lnk https://classroom.google.com/u/1/h",
                       "google docs": "lnk https://docs.google.com/document/u/1/?tgif=d",
                       "google drive": "lnk https://drive.google.com/drive/u/1/my-drive",
                       "arduino": "fl /home/nathanmon/Downloads/arduino-ide_2.1.1_Linux_64bit.AppImage",
                       "aspen": "lnk https://ma-triton.myfollett.com/aspen/logon.do",
                       "google": "src google",
                       "easyeda": "fl /home/nathanmon/Downloads/easyeda-linux-x64-6.5.34/easyeda-linux-x64/easyeda",
                       "terminal": "alt gnome-terminal",
                       "command prompt": "alt gnome-terminal",
                       "music": "ytb https://www.youtube.com/playlist?list=PLdxd7UUBk96Bh-DiZHtNEaQHfct8O1fhN",
                       "fbox": "lnk https://fboxz.to/",
                       "netflix": "lnk https://www.netflix.com/browse",
                       "disney plus": "lnk https://www.disneyplus.com/home"}

def launch_application(application_name):
    # Try to find the executable
    executable_path = shutil.which(application_name)

    # Try to find the desktop entry file
    desktop_file_path = shutil.which(application_name + ".desktop")

    if executable_path:
        subprocess.Popen([executable_path])
    elif desktop_file_path:
        subprocess.Popen(["xdg-open", desktop_file_path])
    else:
        return False
    return True


existing_names = {"terminal": "gnome-terminal-server",
                  "command prompt": "gnome-terminal-server",
                  "arduino": "arduino-snap",
                  "arduino ide": "arduino-snap"}


def open_app(app):
    try:
        command = predefined_programs[app.lower().strip()]
        command_type = command.split(" ")[0]
        app = command.split()[1]

        if command_type == "lnk":
            webbrowser.open_new_tab(app)
        elif command_type == "src":
            if any(app in i.name() for i in psutil.process_iter()): # Chrome is already open
                # Create a new separate window
                pyautogui.hotkey('ctrl', 'n')
            else: # If google is not open
                # Open chrome
                pyautogui.press("winleft")
                pyautogui.typewrite(app)
                pyautogui.press("enter")
        elif command_type == "alt":
            launch_application(app)
        elif command_type == "fl":
            subprocess.Popen([app], restore_signals=False)

    except:
        if not launch_application(app):
            search_query = f"{app}"
            webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")

def close_app(process_name):
    if process_name.strip() in existing_names.keys():
        process_name = existing_names[process_name]
    
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == process_name.lower():
            pid = process.info['pid']
            try:
                process = psutil.Process(pid)
                process.terminate()
                print(f"{process_name} has been closed.")
                return
            except psutil.NoSuchProcess:
                print(f"Error: Process {pid} not found.")
                return

    print(f"{process_name} is not running.")


def get_most_recent_file(directory):
    # Get a list of all files in the directory
    list_of_files = glob.glob(os.path.join(directory, '*'))
    
    # Sort the files by modification time
    if list_of_files:
        most_recent_file = max(list_of_files, key=os.path.getmtime)
        return most_recent_file
    return None

def file_search(root_folder, filename):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None

def open_file(name):
    if "recent" in name:
        file = get_most_recent_file()
    else:
        file = file_search(name)
    
    subprocess.call(['xdg-open', file])