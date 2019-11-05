# TODO import logging
import yaml
from selenium import webdriver


class Cybogram:
    def __init__(self):
        self.__account = None
        self.__load_config_files()
        self.__browser = webdriver.Firefox()
        self.__browser.implicitly_wait(4)

    def __load_config_files(self):
        # system settings configuration file
        with open('./config/sys_config.yaml') as sys_config_file:
            self.__sys_config = yaml.full_load(sys_config_file)

        # user settings configuration file
        with open('./config/user_config.yaml') as user_config_file:
            self.__user_config = yaml.full_load(user_config_file)

    """
    API Methods
    """

    def start(self, account: str):
        self.__account = account
        self.__browser.get(self.__sys_config['ig_login_url'])
        self.__login(account)
        while True:
            self.__get_posts_random_hashtag()
            self.__like_random_post()
            self.__comment_random_post()
            self.__follow_random_account_from_post()

    def __login(self, account: str):
        username_field = self.__browser.find_element_by_xpath('//input[@name=\"username\"]')
        password_field = self.__browser.find_element_by_xpath('//input[@name=\"password\"]')
        login_button = self.__browser.find_element_by_xpath(
            f'//button[@type=\"submit\"]')

        username_field.send_keys(self.__user_config[account]['username'])
        password_field.send_keys(self.__user_config[account]['password'])
        login_button.click()
        self.__close_notifications_windows()

    def __close_notifications_windows(self):
        not_now_button = self.__browser.find_element_by_xpath("//button[contains(text(), \"Not Now\")]")
        if not_now_button is not None:
            not_now_button.click()

    def __get_posts_random_hashtag(self):
        pass

    def __like_random_post(self):
        pass

    def __comment_random_post(self):
        pass

    def __follow_random_account_from_post(self):
        pass
