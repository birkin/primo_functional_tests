# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestToaeon():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def wait_for_window(self, timeout = 2):
    time.sleep(round(timeout / 1000))
    wh_now = self.driver.window_handles
    wh_then = self.vars["window_handles"]
    if len(wh_now) > len(wh_then):
      return set(wh_now).difference(set(wh_then)).pop()
  
  def test_toaeon(self):
    # Test name: to aeon
    # Step # | name | target | value
    # 1 | open | /discovery/fulldisplay?docid=alma991007439769706966&context=L&vid=01BU_INST:BROWN&lang=en | 
    self.driver.get("https://bruknow.library.brown.edu/discovery/fulldisplay?docid=alma991007439769706966&context=L&vid=01BU_INST:BROWN&lang=en")
    # 2 | setWindowSize | 871x850 | 
    self.driver.set_window_size(871, 850)
    # 3 | waitForElementPresent | css=prm-location-items > .section-title > span | 30000
    WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "prm-location-items > .section-title > span")))
    # 4 | runScript | window.scrollTo(0,1150) | 
    self.driver.execute_script("window.scrollTo(0,1150)")
    # 5 | waitForElementPresent | xpath=//span[contains(.,'Reading Room Request')] | 30000
    WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//span[contains(.,\'Reading Room Request\')]")))
    # 7 | waitForElementVisible | xpath=//span[contains(.,'Reading Room Request')] | 30000
    WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Reading Room Request\')]")))
    # 8 | click | xpath=//span[contains(.,'Reading Room Request')] | 
    # click command without new window config -- just to show that the xpath specification is perceived.
    self.driver.find_element(By.XPATH, "//span[contains(.,\'Reading Room Request\')]").click()
    # 9 | click | xpath=//span[contains(.,'Reading Room Request')] | 
    # click with (I think) proper new window specification. Why doesn't this work?
    self.vars["window_handles"] = self.driver.window_handles
    # 10 | selectWindow | handle=${aeon_window} | 
    self.driver.find_element(By.XPATH, "//span[contains(.,\'Reading Room Request\')]").click()
    # 11 | click | xpath=(//input[@value='Login'])[2] | 
    self.vars["aeon_window"] = self.wait_for_window(5000)
    self.driver.switch_to.window(self.vars["aeon_window"])
    self.driver.find_element(By.XPATH, "(//input[@value=\'Login\'])[2]").click()
  
