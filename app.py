import os, time, random
import xlsxwriter
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from email_sender import send_success_email, send_error_email

# Load dot environment
load_dotenv()

# Setup for Selenium browser
driver_path = os.getenv("DRIVER_PATH")
binary_path = os.getenv("BINARY_PATH")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
firefox_service = Service(driver_path)
firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)

# Variables for the program
music_directory = os.listdir(os.getenv("MUSIC_DIRECTORY"))
music_list = []
music_error_list = []
index = 1

# Create Excel Workbook
workbook = xlsxwriter.Workbook("SongList.xlsx")
workbook_song_list = workbook.add_worksheet(name="Song-List")
workbook_song_list.write('A1', "Song Name")
workbook_song_list.write('B1', "Key")
workbook_song_list.write('C1', "BPM")
workbook_song_list.write('D1', "Camelot")


# Get the song from tunebat
def get_song(song_name, index):

    # Launch firefox
    browser = webdriver.Firefox(service=firefox_service,
                                options=firefox_options)

    browser.get("https://tunebat.com/")

    search_input = browser.find_element(By.TAG_NAME, "input")
    search_input.send_keys(song_name)
    search_input.send_keys(Keys.RETURN)

    time.sleep(2)

    try:
        song_key = browser.find_element(
            By.XPATH,
            "/html/body/div[2]/section/section/main/div/div[2]/div[2]/div[1]/a/div/div[2]/div/div[2]/div[1]/p[1]"
        )
        song_bpm = browser.find_element(
            By.XPATH,
            "/html/body/div[2]/section/section/main/div/div[2]/div[2]/div[1]/a/div/div[2]/div/div[2]/div[2]/p[1]"
        )
        song_camelot = browser.find_element(
            By.XPATH,
            "/html/body/div[2]/section/section/main/div/div[2]/div[2]/div[1]/a/div/div[2]/div/div[2]/div[3]/p[1]"
        )

        workbook_song_list.write(f'A{index}', song_name)
        workbook_song_list.write(f'B{index}', song_key.text)
        workbook_song_list.write(f'C{index}', song_bpm.text)
        workbook_song_list.write(f'D{index}', song_camelot.text)
        browser.close()
        print(f"Song {song_name}: obtained correctly")
    except Exception as e:
        music_error_list.append(song_name)
        print(f"There was an error getting the song {song_name}. Error: {e}")
        browser.close()


# Get song titles from the directory
for file in music_directory:
    music_list.append(os.path.splitext(file)[0])

# Make the request to get the data from the page
for song_title in music_list:
    try:
        get_song(song_title, index)
        time.sleep(random.randint(1, 5))
        index += 1
    except Exception as e:
        send_error_email(os.getenv("EMAIL_SENDER"),
                         os.getenv("EMAIL_PASSWORD"),
                         os.getenv("EMAIL_RECEIVER"), e)

# Close the workbook and create the file
workbook.close()
send_success_email(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"),
                   os.getenv("EMAIL_RECEIVER"), music_error_list)
