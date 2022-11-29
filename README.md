# Music-Data-To-Excel
### Python script to obtain key, bpm and camelot key from a list of songs using selenium and applying web scraping to the [Tunebat](https://tunebat.com/) site 

## Quick notes

### The project uses selenium and Firefox browser so you need to download the [Firefox web driver](https://github.com/mozilla/geckodriver) or modify the code to work with your prefered browser

### You need to create the following variables in a .env file for it to run correctly:
  - DRIVER_PATH (absolute path to the .exe file of the web drive)
  - BINARY_PATH (absolute path to the .exe file of your web browser)
  - MUSIC_DIRECTORY (absolute path to the music folder)
  - EMAIL_SENDER (self explanatory)
  - EMAIL_PASSWORD (self explanatory)
  - EMAIL_RECEIVER (self explanatory)
