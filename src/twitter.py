
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from dataclasses import dataclass, field


TWITTER_AUTH_COOKIE = "09eee779a30306bfc76832606c01bfaf9a1a2af1"
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
        
    def scroll_to_element(browser:WebDriver, element:WebElement, scrollMarginTop:int) -> None:
        #browser.execute_script('const y = arguments[0].getBoundingClientRect().top + window.pageYOffset - 10; windows.scrollTo({top: y, behavior: "smooth"});', element)
        browser.execute_script(f'arguments[0].style.scrollMarginTop = "{scrollMarginTop}px";', element)
        browser.execute_script('arguments[0].scrollIntoView({behavior: "smooth"});', element)


class Twitter:
    def __init__(self, auth_cookie:str, headless:bool=True) -> None:
        # Turn off the browser window if not needed for debugging
        options = webdriver.FirefoxOptions()
        if headless: options.add_argument("--headless")

        # Create browser
        self.browser = webdriver.Firefox(options=options)

        # Variables
        self.auth_cookie = auth_cookie
        self.posts = self.Posts(self.browser)

        # Load and add cookies
        self.browser.get("https://twitter.com/")
        self.browser.add_cookie({"name":"d_prefs", "value":"MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw"}) # Cookie banner
        self.browser.add_cookie({"name":"auth_token", "value":auth_cookie}) # Login
        self.browser.refresh()

        # Wait for complete load
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
        def __init__(self, browser:WebDriver) -> None:
            self.browser = browser
            self.posts:list[Post] = []
            self.post_location:int = -1

        def get_post(self) -> Post:
            if len(self.posts) == 0: self.__load_posts()
            if self.post_location == -1: self.post_location = 0
            else: self.post_location += 1
            if self.post_location == len(self.posts): self.__load_posts()

            print(f"{self.post_location+1}/{len(self.posts)}")

            post:Post = self.posts[self.post_location]
            Utils.scroll_to_element(self.browser, post.element, 64)
            return post

        def __load_posts(self) -> None:
            posts:list[WebElement] = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[5]/div/section/div/div").find_elements(By.TAG_NAME, "article")
            for post in posts:
                self.posts.append(
                    Post(
                        Utils.find_element_text(post, By.XPATH, "div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/div[1]/div/a/div/div[1]/span/span"),
                        Utils.find_element_text(post, By.XPATH, "div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/div[2]/div/div[1]/a/div/span"),
                        Utils.find_element_text(post, By.XPATH, "div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/div[2]/div/div[3]/a/time"),
                        Utils.find_element_text(post, By.XPATH, "div/div/div[2]/div[2]/div[2]/div/span"),
                        post
                    )
                )


if __name__ == "__main__":
    twitter = Twitter(TWITTER_AUTH_COOKIE, headless=False)
    for _ in range(25):
        print(twitter.posts.get_post())
        time.sleep(1)
