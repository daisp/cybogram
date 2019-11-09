# 🤖 Cybogram - a Python- and Selenium-based Instagram bot
## Overview & Flow
This bot:
1. Opens an automated browser window.
2. Logs in to a predetermined Instagram account (chosen when running the bot) using a username and password.
3. Finds and loads random posts it finds via a predetermined list of hashtags.
4. Likes the chosen post (up to a predefined likes-per-run limit).
5. Comments on the chosen post (up to a predefined comments-per-run limit). The comments are randomly selected from a predefined comment list.
6. While there are still comments or likes to be placed, goes back to step 3. 
## Install the bot
1. Download and extract the Firefox Webdriver executable `geckodriver.exe` into `/bin/browser_drivers` (You may have to create these directories for yourself). You can download the driver executable from Mozilla's official repo [here](https://github.com/mozilla/geckodriver/releases). 
2. The required Python packages are listed in the `environment.yml` file. If you use Anaconda, you can create a new Anaconda environment by typing:
    ```bash
    conda env create -f environment.yml
    ```
3. Rename `/config/demo_user_config.yaml` to `/config/user_config.yaml` (i.e. remove the "`demo_`" part)
4. Rename the top-level account names in `/config/user_config.yaml` to ones you will remember easily (it is recommended to set them to your Instagram's username).
5. Fill in your accounts login credentials as well as the desired hashtags and comments for the bot to use.
6. You're all set.

## Run the bot
To run the bot:
1. From the project's root folder, type (On Linux or macOS):
    ```bash
    python3 ./run.py myaccount
    ```
   Or on Windows:
   ```cmd
    python3 .\run.py myaccount
    ```
   Where `myaccount` should be replaced by your account name, as listed in the top-level account names in `/config/user_config.yaml`.
