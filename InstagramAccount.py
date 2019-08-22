from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pyttsx3


class InstagramAccount:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.engine = pyttsx3.init()

    def login(self):
        driver = self.driver
        # Get the Instagram page from web driver
        driver.get("https://www.instagram.com")
        # Bot needs time to load
        time.sleep(1)
        login = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login.click()
        time.sleep(1)
        username = driver.find_element_by_name('username')
        username.clear()
        username.send_keys(self.username)
        password = driver.find_element_by_name('password')
        password.clear()
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def like_photo_with_hashtag(self, hashtag):
        time.sleep(3)
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(1)
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(2)
        hrefs = driver.find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
        print(hashtag + " photos: " + str(len(pic_hrefs)))

        time.sleep(2)
        like = None
        for pic_href in pic_hrefs:
            time.sleep(1)
            driver.get(pic_href)
            try:
                time.sleep(1)
                if self.has_xpath("//span[contains(@class,\"glyphsSpriteHeart__outline__24__grey_9 u-__7\") "
                                  "and contains(@aria-label,\"Like\")]"):
                    like = driver.find_element_by_xpath(
                        "//span[contains(@class,\"glyphsSpriteHeart__outline__24__grey_9 u-__7\") "
                        "and contains(@aria-label,\"Like\")]")
                    like.click()
            except NoSuchElementException as e:
                print("Not able to find hashtag and/or like button. Contact administration for assistance")
                self.close_browser()

    def follow(self, username):
        """Follow the specified user
        If username is already followed, you will be notified
        """
        time.sleep(3)
        self.driver.get('https://www.instagram.com/' + username + '/')

        follow_button = self.driver.find_element_by_css_selector('button')
        time.sleep(3)
        if follow_button.text != 'Following':
            print("Congratulations, you just followed: " + username);
            follow_button.click()
            time.sleep(3)
        else:
            print("You are already following this user: " + "username")

    def get_daily_homepage_feed(self, like_images):
        """ Returns a string containing news from the explore page
        Args:
            :param like_images: A boolean specifying whether to like posts on explore page
        """
        time.sleep(3)
        daily_descriptions = ""
        driver = self.driver
        if self.has_xpath("//button[@class='aOOlW   HoLwm ']"):
            not_now = driver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']")
            not_now.click()
        explore_button = driver.find_element_by_xpath(
            "/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[1]/a/span")
        explore_button.click()
        try:
            for i in range(1, 4):
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                time.sleep(1)
            list_of_href = []
            explore = driver.find_element_by_class_name("v1pSD")
            elements = explore.find_elements_by_tag_name("a")
            for elem in elements:
                href = elem.get_attribute("href")
                list_of_href.append(href)

            old_time = time.time()
            for pic_href in list_of_href:
                time.sleep(3)
                driver.get(pic_href)
                time.sleep(3)
                has_description = driver.find_element_by_xpath(
                    "/html/body/span/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span")
                if has_description:
                    daily_descriptions += driver.find_element_by_xpath(
                        "/html/body/span/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span").text
                time.sleep(2)
                has_xpath = self.has_xpath(
                        "/html/body/span/section/main/div/div/article/div[2]/section[1]/span[1]/button/span")
                print(has_xpath)
                if like_images and has_xpath:
                    likes = driver.find_element_by_xpath(
                            "/html/body/span/section/main/div/div/article/div[2]/section[1]/span[1]/button/span")
                    likes.click()
                if time.time() - old_time >= 20:
                    break
        except Exception as e:
            self.close_browser()
        finally:
            self.text_to_speech(daily_descriptions)

    def text_to_speech(self, text):
        """ Returns a string containing news from the explore page
            Args:
                :param text: A string specifying the text the be said verbally by pyttsx3 voice bot
        """
        self.engine.setProperty("volume", 2.0)
        self.engine.setProperty("rate", 150)
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[0].id)
        self.engine.say(text)
        self.engine.runAndWait()

    def close_browser(self):
        self.driver.quit()

    def has_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False

