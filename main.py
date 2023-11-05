import os
import time
import logging
import copy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


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
    x = row_element.get_attribute("class").split(" ")
    print(x)
    for cls in x:
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
    
class Colors:
    '''https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit'''
    RESET =     '\033[0m'
    GRAY =      '\033[48;5;235m'
    YELLOW =    '\033[48;5;226m'
    GREEN =     '\033[48;5;118m'

def state_to_grid(state_list):
    grid = []
    for row in range(6):
        grid.append(copy.copy(state_list[row*5:(row*5) + 5]))
    return grid

def format_str(letter, state, formatted=False):
    d = {
        "correct":  Colors.GREEN,
        "present":  Colors.YELLOW,
        "absent":   Colors.GRAY,
        "empty":    Colors.RESET
    }
    color = d[state]
    if formatted and (state == "empty"):
        letter = "\u25A1"
    return color + letter + Colors.RESET

def grid_to_str(grid_list, formatted=False):
    return "\n".join(
        [
            " ".join( 
                [ 
                    format_str(letter, state, formatted) if formatted else letter
                    for (state, letter) in row
                ]
            ) 
            for row in grid_list
        ]
    )
        
def main():
    driver = init_driver()

    open_wordle_page(driver)

    # Play Valid Word #1
    current_row = 0
    play_word(driver, "WORDS")
    b_err = wait_for_error(driver, current_row)
    print(f"b_err={b_err}")
    current_state = get_state(driver)
    # print(current_state)
    current_grid = state_to_grid(current_state)
    # print(current_grid)
    grid_str = grid_to_str(current_grid, formatted=False)
    print(grid_str)
    grid_str = grid_to_str(current_grid, formatted=True)
    print(grid_str)

    # Play Valid Word #2
    current_row += 1
    play_word(driver, "FJORD")
    b_err = wait_for_error(driver, 0)
    print(f"b_err={b_err}")
    grid_str =  grid_to_str(state_to_grid(get_state(driver)), formatted=True)
    print(grid_str)
    
    # Play Invalid Word - Not Enough Letter
    current_row +=1
    play_word(driver, "ZZ")
    b_err = wait_for_error(driver, current_row)
    print(f"b_err={b_err}")
    
    delete_current_word(driver)

    # Play Invalid Word - Not in Word List
    play_word(driver, "YEROX")
    b_err = wait_for_error(driver, current_row)
    print(f"b_err={b_err}")
    
    delete_current_word(driver)

    grid_str =  grid_to_str(state_to_grid(get_state(driver)), formatted=True)
    print(grid_str)

    time.sleep(20)
    driver.quit()

if __name__ == "__main__":
    main()
