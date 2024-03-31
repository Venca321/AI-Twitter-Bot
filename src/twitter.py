
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dataclasses import dataclass, field
import time, random


DEBUG = True
PAGE_LOAD_WAIT = 2.5 # seconds


@dataclass
class Post:
    author:str
    author_tag:str
    posted:str
    text:str
    element:WebElement = field(repr=False)


class Utils:
    def find_element(parent:WebElement, find_by, find_by_value:str) -> WebElement|None:
        try: return parent.find_element(find_by, find_by_value)
        except: return None

    def find_element_text(parent:WebElement, find_by, find_by_value:str) -> str|None:
        try: return parent.find_element(find_by, find_by_value).text
        except: return None

    def click_element(element:WebElement) -> bool:
        try: 
            element.click()
            return True
        except: 
            return False
        
    def write_input_by_chars(element:WebElement, text:str) -> None:
        for character in text:
            element.send_keys(character)
            time.sleep(random.randint(15, 100)/920)

    def write(element:WebElement, text:str) -> None:
        text = text.split("\n")
        for line in text:
            Utils.write_input_by_chars(element, line)
            element.send_keys(Keys.ENTER)
        
    def scroll_to_element(browser:WebDriver, element:WebElement, scrollMarginTop:int) -> None:
        #browser.execute_script('const y = arguments[0].getBoundingClientRect().top + window.pageYOffset - 10; windows.scrollTo({top: y, behavior: "smooth"});', element)
        browser.execute_script(f'arguments[0].style.scrollMarginTop = "{scrollMarginTop}px";', element)
        browser.execute_script('arguments[0].scrollIntoView({behavior: "smooth"});', element)


class Twitter:
    def __init__(self, auth_cookie:str, user_tag:str, headless:bool=True) -> None:
        # Turn off the browser window if not needed for debugging
        options = webdriver.FirefoxOptions()
        if headless: options.add_argument("--headless")

        # Create browser
        self.browser = webdriver.Firefox(options=options)

        # Variables
        self.auth_cookie = auth_cookie
        self.posts = self.Posts(self.browser, user_tag)

        # Load and add cookies
        self.browser.get("https://twitter.com/")
        self.browser.add_cookie({"name":"d_prefs", "value":"MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw"}) # Cookie banner
        self.browser.add_cookie({"name":"auth_token", "value":auth_cookie}) # Login
        self.browser.refresh()

        # Wait for complete load
        time.sleep(PAGE_LOAD_WAIT)

    def close(self) -> None:
        self.browser.quit()

    def reload(self) -> None:
        self.browser.refresh()
        self.posts = self.Posts(self.browser)
        time.sleep(PAGE_LOAD_WAIT)

    def switch_to_following_tab(self) -> None:
        following_tab_element = Utils.find_element(self.browser, By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/nav/div/div[2]/div/div[2]/a")
        if following_tab_element:
            Utils.click_element(following_tab_element)
            time.sleep(PAGE_LOAD_WAIT)

    def switch_to_for_you_tab(self) -> None:
        for_you_tab_element = Utils.find_element(self.browser, By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/nav/div/div[2]/div/div[1]/a")
        if for_you_tab_element:
            Utils.click_element(for_you_tab_element)
            time.sleep(PAGE_LOAD_WAIT)

    class Posts:
        def __init__(self, browser:WebDriver, user_tag:str) -> None:
            self.browser = browser
            self.user_tag = user_tag
            self.posts:list[Post] = []
            self.post_location:int = -1

        def create(self, text:str) -> None:
            Utils.click_element(Utils.find_element(self.browser, By.XPATH, "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div"))
            time.sleep(0.2)
            Utils.write(Utils.find_element(self.browser, By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div"), text)
            time.sleep(0.1)
            Utils.click_element(Utils.find_element(self.browser, By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/div[4]"))

        def get_post(self) -> Post:
            if len(self.posts) == 0: self.__load_posts()
            if self.post_location == -1: self.post_location = 0
            else: self.post_location += 1
            if self.post_location == len(self.posts): 
                if len(self.posts) > 100:
                    self.browser.refresh()
                    self.posts = []
                    self.post_location = 0
                    time.sleep(5)
                self.__load_posts()

            print(f"{self.post_location+1}/{len(self.posts)}")

            post:Post = self.posts[self.post_location]
            Utils.scroll_to_element(self.browser, post.element, 64)
            return post

        def __load_posts(self) -> None:
            posts:list[WebElement] = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[5]/div/section/div/div").find_elements(By.TAG_NAME, "article")
            for post in posts:
                try:
                    author = Utils.find_element_text(post, By.XPATH, "div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/div[1]/div/a/div/div[1]/span/span")
                    author_tag = Utils.find_element_text(post, By.XPATH, "div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/div[2]/div/div[1]/a/div/span")
                    posted = Utils.find_element_text(post, By.XPATH, "div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/div[2]/div/div[3]/a/time")
                    text = Utils.find_element_text(post, By.XPATH, "div/div/div[2]/div[2]/div[2]/div/span")

                    seen = len(text) < 5
                    if author_tag == self.user_tag: seen = True

                    for posts in self.posts:
                        if posts.author == author and posts.text == text: seen = True; break

                    if not seen: self.posts.append(Post(author, author_tag, posted, text, post))
                except: None

        def comment(self, post:Post, text:str) -> None:
            comment_button = Utils.find_element(post.element, By.XPATH, "div/div/div[2]/div[2]/div[4]/div/div/div[1]/div")
            if comment_button:
                Utils.click_element(comment_button)
                input_field = Utils.find_element(self.browser, By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div")
                if input_field:
                    Utils.write(input_field, text)
                    reply_button = Utils.find_element(self.browser, By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]")
                    if reply_button: Utils.click_element(reply_button)

        def like(self, post:Post) -> None:
            like_button = Utils.find_element(post.element, By.XPATH, "div/div/div[2]/div[2]/div[4]/div/div/div[3]/div")
            if like_button: Utils.click_element(like_button)

        def repost(self, post:Post) -> None:
            repost_button = Utils.find_element(post.element, By.XPATH, "div/div/div[2]/div[2]/div[4]/div/div/div[2]/div")
            if repost_button: 
                Utils.click_element(repost_button)
                repost_button = Utils.find_element(self.browser, By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div")
                if repost_button: Utils.click_element(repost_button)

