# FlickWall
A  script service that automatically fetches a new wallpaper from MovieDB and sets it as your desktop background on every reboot.

## Description
A Dynamic Movie Wallpaper Setter using Python script that enhances your desktop experience by automatically fetching and setting a stunning wallpaper from the Movie Database (TMDb) every time your computer reboots.

## Features
- **Automated Wallpaper Updates:** The script queries the TMDb API to retrieve a random wallpaper from its extensive collection of movie posters and backgrounds.
  
- **Background Execution:** It runs silently in the background, ensuring that your desktop background is updated seamlessly without user intervention during startup.

- **Cross-Platform Compatibility:** Designed to work on multiple operating systems, including Windows and Linux, ensuring that everyone can enjoy fresh movie-themed wallpapers.

## How It Works

- **API Integration:** The script connects to the TMDb API using a secure API key to fetch the latest movie wallpapers.
  
- **Wallpaper Setting:** After retrieving the wallpaper URL, it downloads the image and sets it as the desktop background using platform-specific methods.
  
- **Startup Configuration:** The script runs on system startup, ensuring a new wallpaper is set every time the computer boots up.
  
- **Automated Installation & Uninstallation:** Uses native Bash (Linux/macOS) and PowerShell (Windows) scripts for fully automated installation, startup configuration, and easy uninstallation.

  ---

  ## Installation

1. Clone the Repository:
   ```bash
   git clone
   ```

2. Change Directory:
   ```bash
   cd flickwall
   ```

3. Run the Installation Script:
   - For Linux:
     ```bash
     ./install.sh
     ```
   - For Windows:
     ```bash
     .\install.ps1
     ```

  ---

  ## Uninstallation
  - For Linux:
    1. Change Directory:
       ```bash
       cd /opt/flickwall/
       ```

    2. Run the Uninstallation Script:
       ```bash
       ./uninstall.sh
       ```
  - For Windows:
  - 
