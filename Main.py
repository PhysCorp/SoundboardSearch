# [Begin PHYSCORP Template]

# Try to import libraries
try:
    import os
    import os.path
    import sys
    import datetime
    import keyboard
    import time
    import json
    import re
    import pyautogui
    from bs4 import BeautifulSoup
    import requests
    from playsound import playsound
    import subprocess
    import win32gui
    import win32con
    import rich
    import rich.traceback
    rich.traceback.install()
except ImportError as e:
    print("[WARN] You are missing one or more libraries. This script cannot continue.")
    print("Try running in terminal >> Python\\python.exe -m pip install -r requirements.txt")
    print("Error: " + str(e))
    input()
    quit()

# Global Vars / Options
global program_name
program_name = "SoundboardSearch"

# Identify working directory and config directory
maindirectory = os.path.join(os.path.dirname(sys.executable))
config_location = os.path.join(os.environ["LOCALAPPDATA"], program_name)

# Create the folders if they don't exist
if not os.path.exists(maindirectory):
    os.makedirs(maindirectory)
if not os.path.exists(config_location):
    os.makedirs(config_location)

# Create a blank properties.json file if it doesn't exist
if not os.path.exists(os.path.join(config_location, "properties.json")):
    with open(os.path.join(config_location, "properties.json"), "w") as properties:
        properties.write("{}")
        properties.close()

# Show logo
print("--- Hello from PHYSCORP! ---")

# Custom functions
def print(string, hide=False):
    if hide:
        rich.print(string)
    else:
        rich.print("> " + string)
    # Append string to log file
    with open(os.path.join(config_location, "log.txt"), "a") as log:
        log.write(str(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")) + " " + string + "\n")
        log.close()

def command(command, verbose=True):
    try:
        commandoutput = subprocess.check_output(str(command), shell=True).decode("utf-8")
    except (subprocess.CalledProcessError, UnboundLocalError):
        commandoutput = ""
        pass
    if verbose:
        print("[italic grey66]" + command + "\n[bright_black]" + commandoutput)
    else:
        # Append string to log file
        with open(os.path.join(config_location, "log.txt"), "a") as log:
            log.write(str(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")) + " " + "[italic grey66]" + command + "\n[bright_black]" + commandoutput + "\n")
            log.close()
    return commandoutput

# [End PHYSCORP Template]

# [Begin Script]
if __name__ == "__main__":
    # Print "Soundboard Search" in giant ascii art
    print(
            """
[red] __                       _ _                         _   __                     _     
/ _\ ___  _   _ _ __   __| | |__   ___   __ _ _ __ __| | / _\ ___  __ _ _ __ ___| |__  
\ \ / _ \| | | | '_ \ / _` | '_ \ / _ \ / _` | '__/ _` | \ \ / _ \/ _` | '__/ __| '_ \ 
_\ \ (_) | |_| | | | | (_| | |_) | (_) | (_| | | | (_| | _\ \  __/ (_| | | | (__| | | |
\__/\___/ \__,_|_| |_|\__,_|_.__/ \___/ \__,_|_|  \__,_| \__/\___|\__,_|_|  \___|_| |_|
            """
    , hide=True)
    
    # # Read properties JSON file
    # with open(os.path.join(config_location, "properties.json"), "r") as properties:
    #     properties_file = json.load(properties)
    #     # Read properties here
    #     properties.close()

    # Functions
    def install_script():
        print("Installing script...")
        current_user = command("whoami")
        current_user = current_user.replace("\n", "")
        current_user = current_user[current_user.find("\\") + 1:]
        command('schtasks /create /sc onlogon /tn ' + str(program_name) + ' /tr "' + str(maindirectory) + '\\' + str(program_name) + '.exe --hide" /ru ' + current_user + ' /rl HIGHEST /f')
        print("[INFO] Script installed successfully.")

    def uninstall_script():
        print("Uninstalling script...")
        command('schtasks /delete /tn ' + str(program_name) + ' /f')
        print("[INFO] Script uninstalled successfully.")

    def hide_script():
        # Search through all open windows and hide the one that contains the title
        def enumHandler(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                if (program_name + ".exe") in win32gui.GetWindowText(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        win32gui.EnumWindows(enumHandler, None)

    def main_script():
        while True:
            # If the user presses WIN + SPACE, open the search prompt
            if keyboard.is_pressed("win + space"):
                searchterm = pyautogui.prompt(text="Please enter the name of the sound you wish to play:", title=str(program_name))
                if searchterm != None:
                    try:
                        # Search for the sound on MyInstants.com using BeautifulSoup
                        print("Searching for sound \"" + searchterm + "\"...")
                        # Convert search term to URL format
                        searchterm = searchterm.replace(" ", "+")
                        # Get the HTML of the search page
                        searchpage = requests.get("https://www.myinstants.com/search/?name=" + searchterm)
                        # Parse the HTML
                        soup = BeautifulSoup(searchpage.content, "html.parser")
                        # Get the first result
                        firstresult = soup.find("div", class_="instant")
                        # Get the URL of the first result
                        firstresulturl = firstresult.find("a")["href"]
                        # Get the HTML of the first result
                        firstresultpage = requests.get("https://www.myinstants.com" + firstresulturl)
                        # Parse the HTML
                        soup = BeautifulSoup(firstresultpage.content, "html.parser")
                        # Get the URL of the sound file by selecting the "a" record that contains /media/sounds/
                        soundurl = soup.find("a", href=re.compile("/media/sounds/"))["href"]
                        # Download the sound file
                        print("Downloading sound file " + soundurl + "...")
                        # Add the base URL to the sound URL
                        soundurl = "https://www.myinstants.com" + soundurl
                        soundfile = requests.get(soundurl)
                        # Save the sound file
                        with open(os.path.join(config_location, "sound.mp3"), "wb") as sound:
                            sound.write(soundfile.content)
                            sound.close()
                        # Play the sound file
                        print("Playing sound file...")
                        playsound(os.path.join(config_location, "sound.mp3"))
                        # Delete the sound file
                        print("Deleting sound file...")
                        os.remove(os.path.join(config_location, "sound.mp3"))
                        print("Done!")
                    except Exception as e:
                        print("An error occurred while searching for the sound.")
                        print("Error: " + str(e))
                time.sleep(1)
            else:
                time.sleep(0.1)

    # Perform different actions based on the arguments
    triggered = False
    if len(sys.argv) > 1:
        for argument in sys.argv:
            # Install
            if "install" in argument:
                triggered = True
                install_script()
            # Remove
            elif "remove" in argument:
                triggered = True
                uninstall_script()
            # Hide
            elif "hide" in argument:
                triggered = False
                hide_script()
    # If no arguments were passed, run the main script
    if not triggered:
        # Print startup info
        print(str(program_name) + " is running!")
        print("To invoke this program, press WIN + SPACE on your keyboard. Then, type the name of a sound to play. SoundboardSearch will then search MyInstants.com for the sound, and immediately play it.", hide=True)

        main_script()