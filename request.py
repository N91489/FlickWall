import requests
import random
import subprocess
import platform
import os
import ctypes
from dotenv import load_dotenv, find_dotenv

operating_system = platform.system()
load_dotenv(find_dotenv())
api_key=os.getenv('TMDB_API_KEY')

def getAspectRatio():

    # Windows
    if operating_system == "Windows":
        command = ['powershell', '-Command', 'Get-WmiObject Win32_VideoController | Select-Object -First 1 SystemName, 	CurrentHorizontalResolution, CurrentVerticalResolution']
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8').stdout
        
        # Parsing the result
        lines = result.strip().split('\n')
        header, values = lines[0], lines[2]
        resolution_parts = values.split()
        screen_width = int(resolution_parts[1])
        screen_height = int(resolution_parts[2])

    # MacOS
    elif operating_system == "Darwin":
        command = ['system_profiler','SPDisplaysDataType']
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8').stdout

        # Parsing the result
        for line in result.splitlines():
            if "Resolution" in line:
                screen_width = int(line.split(": ")[1].split(" x ")[0])
                screen_height = int(line.split(": ")[1].split(" x ")[1].split(" ")[0])

    # Linux
    elif operating_system == "Linux":
        command = ["xdpyinfo"]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8').stdout

        # Parsing the result
        for line in result.splitlines():
            if "dimensions:" in line:
                screen_width = int(line.split()[1].split("x")[0])
                screen_height = int(line.split()[1].split("x")[1])
    
    aspect_ratio = (screen_width / screen_height)
    return aspect_ratio

def getWallpaper(include_adult = "false", accordingToScreenRatio = True, removePoster = True, max_page_no = 400):
    
        # Auth Initialization
        auth = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Pull Image 
        while(True):
        
            page_no = random.randint(0,max_page_no)
            
            # Get Movie url
            getMovie_url = f"https://api.themoviedb.org/3/discover/movie?include_adult={include_adult}&include_video=false&page={page_no}&sort_by=popularity.desc"
            getMovie_response = requests.get(getMovie_url, headers=auth)
            if getMovie_response.status_code == 200:
                getMovie_data = getMovie_response.json()
                getMovieIds = [movie['id'] for movie in getMovie_data["results"]]
                getMovieId = random.choice(getMovieIds)
                
                # Get Image url
                getImage_url =f"https://api.themoviedb.org/3/movie/{getMovieId}/images"
                getImage_response = requests.get(getImage_url,headers=auth)
                if getImage_response.status_code == 200:
                    getImage_data = getImage_response.json()
                    getImage ={}
                    for image in getImage_data["backdrops"]:
                        value = {image["aspect_ratio"]:image["file_path"]}
                        getImage.update(value)

                    # Based Condition
                    if removePoster == True:
                        getImage.pop(next(iter(getImage)))
                    
                    if accordingToScreenRatio == True:
                        aspect_ratio = getAspectRatio()
                        for key in getImage:
                            if(float(key) <= aspect_ratio):
                                getImage.pop(key)

                    if getImage:
                        return random.choice(list(getImage.values()))
                    
def downloadImage(img_url):

    # Exit if not new image is pulled
    if img_url == -1:
        return

    # Create Image url
    url = "https://image.tmdb.org/t/p/original" + img_url
    response = requests.get(url)

    # Download Image 
    if response.status_code == 200:
        with open ("wallpaper.jpg","wb") as file:
            file.write(response.content)

    else:
        print("Could not Download")

def setWallpaper():

    # Full Path to Image
    abpath = os.path.abspath("wallpaper.jpg")
    
    # Linux
    if operating_system == "Linux":
        subprocess.run([
            "gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{abpath}"
        ])

    # Windows
    elif operating_system == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abpath, 3)

    # MacOS
    """elif operating_system == "Darwin":
        command = f'''
        /usr/bin/osascript -e 'tell application "System Events"
        set desktop picture to POSIX file "{abpath}"
        end tell'
        '''
        subprocess.run(command, shell=True)
        subprocess.run("killall Dock", shell=True)"""


downloadImage(getWallpaper())
setWallpaper()
