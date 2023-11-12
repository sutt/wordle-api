import time
import json
import uuid
import copy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from utils import grid_to_str

def init_driver():
    options = Options()
    options.add_argument('--incognito')
    options.add_argument('--log-level=3')  # suppress console output
    driver = webdriver.Chrome(options=options)
    return driver

def open_wordle_page(driver, tic=1):
    url = "https://www.nytimes.com/games/wordle/index.html"
    driver.get(url)
    time.sleep(tic)
    play_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="Play"]')
    play_button.click()
    time.sleep(tic)
    close_button = driver.find_element(By.CLASS_NAME, 'Modal-module_closeIcon__TcEKb')
    close_button.click()
    time.sleep(tic)

def play_word(driver, word, tic=0.5):
    letters = list(word)
    for letter in letters:
        driver.find_element(By.TAG_NAME, 'body').send_keys(letter)
        time.sleep(tic)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RETURN)
    time.sleep(tic)

def get_state(driver):
    elements = driver.find_elements(By.CLASS_NAME, 'Tile-module_tile__UWEHN')
    states_and_letters = [
        (element.get_attribute('data-state'), element.text) 
        for element in elements
    ]
    return states_and_letters

def get_row_results(driver, row_index):
    state_list = get_state(driver)
    state_list = state_list[row_index*5:(row_index*5) + 5]
    state_list = [state for (state, letter) in state_list]
    return state_list

def check_state_for_win(driver, row_index):
    state_list = get_row_results(driver, row_index)
    return all([item == 'correct' for item in state_list])
    
def delete_current_word(driver, tic=0.5):
    for i in range(5):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.BACKSPACE)
        time.sleep(tic)

class error_callback(object):
    def __init__(self, row_index):  
        self.row_index = row_index

    def __call__(self, driver):
        if self._check_row(driver):
            time.sleep(0.1)
            return self._check_toast(driver)
        return False
  
    def _check_row(self, driver):
        row_loc = (By.CLASS_NAME, 'Row-module_row__pwpBq')
        indicator_str = 'Row-module_invalid'  # not full string
        row_elements = driver.find_elements(*row_loc)
        row_element = row_elements[self.row_index]
        for cls in row_element.get_attribute("class").split(" "):
            if indicator_str in cls:  # not full string; check for contains substring
                return True
        return False
  
    def _check_toast(self, driver):
        toast_cls = 'ToastContainer-module_toaster__TYGMD'
        toast_id = 'ToastContainer-module_gameToaster__HPkaC'
        toast_loc = (By.ID, toast_id)
        toast_element = driver.find_element(*toast_loc)
        toast_text = toast_element.text
        return toast_text
      
def wait_for_error(driver, row_index, wait_time=1.0):
    try:
        wait = WebDriverWait(driver, wait_time)
        toast_text = wait.until(error_callback(row_index))
        return toast_text
    except TimeoutException:
        return False
    except Exception as e:
        return f'Unknown Error: {e}'
    
def check_page_for_win(driver, wait_time=3.0):
    time.sleep(wait_time)
    win_modal_class_name = 'Modal-module_modalOverlay__cdZDa'
    try:
        win_modal = driver.find_element(By.CLASS_NAME, win_modal_class_name)
        if win_modal:
            return True
    except:
        pass
    return False

def state_to_grid(state_list):
    grid = []
    for row in range(6):
        grid.append(copy.copy(state_list[row*5:(row*5) + 5]))
    return grid

class NYTWordleGame:

    def __init__(self):
        self.current_row = 0
        self.driver = init_driver()
        self.uuid = str(uuid.uuid4())
        open_wordle_page(self.driver)
        print(f'init {self.uuid}')

    def play_round(self, word, retries=2):
        for iter_try in range(retries):
            play_word(self.driver, word)
            err = wait_for_error(self.driver, self.current_row, wait_time=1.0)
            if not(err):
                break
            delete_current_word(self.driver)
        b_win = check_state_for_win(self.driver, self.current_row)
        results_list = get_row_results(self.driver, self.current_row)
        grid_str =  grid_to_str(state_to_grid(get_state(self.driver)), formatted=True)
        info = {
            "word": word,
            "current_row": self.current_row,
            "error": True if err else False,
            "error_text": err if err else None,
            "win": b_win,
            "results": None if err else results_list,
            "grid_formatted": grid_str,
        }
        if not(err):
            self.current_row += 1
        if b_win:
            self.driver.quit()
        return info

    def get_state(self):
        pass


def main():

    game = NYTWordleGame()

    word_list = [
        "WORDS",
        "FJORD",
        "ZZ",
        "YEROX",
        "FLARE",
    ]

    for word in word_list:
        info = game.play_round(word)
        print(info['grid_formatted'])
        print(json.dumps(info, indent=4))


if __name__ == "__main__":
    main()