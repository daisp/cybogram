# TODO import logging
import random
import time

import yaml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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

    def __login(self, account: str):
        self.__account = account
        username_field = self.__browser.find_element_by_xpath('//input[@name=\"username\"]')
        password_field = self.__browser.find_element_by_xpath('//input[@name=\"password\"]')
        login_button = self.__browser.find_element_by_xpath(
            f'//button[@type=\"submit\"]')

        username_field.send_keys(self.__user_config[self.__account]['username'])
        password_field.send_keys(self.__user_config[self.__account]['password'])
        login_button.click()
        time.sleep(1.5)

    def __load_random_post_from_random_hashtag(self, num_of_post_rows: int = 1):
        assert num_of_post_rows >= 1
        hashtag_to_search = random.choice(self.__user_config[self.__account]['hashtag_list'])
        self.__run_hashtag_search(query=hashtag_to_search)
        candidate_posts = []
        for i in range(num_of_post_rows):
            candidate_posts.extend(
                self.__browser.find_elements_by_xpath(
                    '//img[@decoding=\"auto\"][@style=\"object-fit: cover;\"]'))
        chosen_post_url_suffix = random.choice(candidate_posts).find_element_by_xpath('../../..').get_attribute(
            'href')
        self.__browser.get(chosen_post_url_suffix)

    def __run_hashtag_search(self, query: str):
        self.__browser.get(self.__sys_config['ig_explore_hashtag_url'] + query + '/')
        # time.sleep(3)

    def __like_current_post(self) -> None:
        """
        This method likes the currently open post page and must be called immediately after
        __load_random_post_from_random_hashtag() has loaded a specific post page.
        """
        like_button = self.__browser.find_element_by_xpath('//span[@aria-label=\"Like\"]').find_element_by_xpath('..')
        like_button.click()

    def __comment_on_current_post(self):
        """
        This method selects a random comment from the current user's comment list and posts it on the
        currently open post's page. This method must be called after __load_random_post_from_random_hashtag()
        has loaded a specific post page.
        """
        chosen_comment = random.choice(self.__user_config[self.__account]['comment_list'])
        comment_text_field = self.__browser.find_element_by_xpath('//textarea[@aria-label=\"Add a comment…\"]')
        comment_text_field.click()
        comment_text_field = self.__browser.find_element_by_xpath('//textarea[@aria-label=\"Add a comment…\"]')
        comment_text_field.send_keys(chosen_comment)
        comment_text_field.send_keys(Keys.ENTER)

    def __follow_random_account_from_post(self):
        pass

    """
    API Methods
    """

    def start(self, account: str):
        self.__account = account
        self.__browser.get(self.__sys_config['ig_login_url'])
        self.__login(account)
        self.__load_random_post_from_random_hashtag()
        self.__like_current_post()
        self.__load_random_post_from_random_hashtag()
        self.__comment_on_current_post()
        # self.__follow_random_account_from_post()
