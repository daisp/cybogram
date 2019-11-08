import logging
import random
import time
from _datetime import datetime

import yaml
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys

logging.basicConfig(level=logging.INFO)


class Cybogram:
    def __init__(self):
        logging.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S - ') + 'New Cybogram bot instantiation initiated.')
        self.__seconds_to_sleep_after_login = 5
        self.__seconds_to_sleep_after_like = 3
        self.__seconds_to_sleep_after_comment = 21
        self.__account = None
        self.__load_config_files()
        self.__browser = webdriver.Firefox()
        self.__browser.implicitly_wait(4)
        logging.info(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S - ') + 'New Cybogram bot instance created successfully.')

    def __load_config_files(self):
        logging.info(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S - ') + 'Attempting to load configuration files from disk.')
        # system settings configuration file
        with open('./config/sys_config.yaml') as sys_config_file:
            self.__sys_config = yaml.full_load(sys_config_file)
            logging.info(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S - ') + 'System configuration file loaded successfully.')

        # user settings configuration file
        with open('./config/user_config.yaml') as user_config_file:
            self.__user_config = yaml.full_load(user_config_file)
            logging.info(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S - ') + 'User configuration file loaded successfully.')

    def __login(self, account: str):
        self.__account = account
        logging.info(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S - ') + f'Attempting to login using account {self.__account}.')
        username_field = self.__browser.find_element_by_xpath('//input[@name=\"username\"]')
        password_field = self.__browser.find_element_by_xpath('//input[@name=\"password\"]')
        login_button = self.__browser.find_element_by_xpath(
            f'//button[@type=\"submit\"]')

        username_field.send_keys(self.__user_config[self.__account]['username'])
        password_field.send_keys(self.__user_config[self.__account]['password'])
        login_button.click()
        logging.info(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S - ') + f'Successful login using account {self.__account}.')

    def __load_random_post_from_random_hashtag(self):
        hashtag_to_search = random.choice(self.__user_config[self.__account]['hashtag_list'])

        self.__run_hashtag_search(query=hashtag_to_search)
        candidate_posts = []
        candidate_posts.extend(
            self.__browser.find_elements_by_xpath('//img[@decoding=\"auto\"][@style=\"object-fit: cover;\"]'))
        chosen_post_url_suffix = random.choice(candidate_posts).find_element_by_xpath('../../..').get_attribute(
            'href')
        self.__browser.get(chosen_post_url_suffix)
        logging.info(datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S - ') + f'Successfully loaded the post {self.__browser.current_url} using the hashtag "{hashtag_to_search}".')

    def __run_hashtag_search(self, query: str):
        self.__browser.get(self.__sys_config['ig_explore_hashtag_url'] + query + '/')

    def __like_current_post(self) -> None:
        """
        This method likes the currently open post page and must be called immediately after
        __load_random_post_from_random_hashtag() has loaded a specific post page.
        """
        try:
            like_button = self.__browser.find_element_by_xpath('//span[@aria-label=\"Like\"]').find_element_by_xpath(
                '..')
            like_button.click()
            logging.info(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S - ') + f'Successfully liked the post {self.__browser.current_url}')
        except common.exceptions.NoSuchElementException:
            logging.error(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S - ') + f'The post {self.__browser.current_url} seems to already be liked by this account.')
        except:
            logging.error(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S - ') + f'An unknown error occurred on the page {self.__browser.current_url}')

    def __comment_on_current_post(self):
        """
        This method selects a random comment from the current user's comment list and posts it on the
        currently open post's page. This method must be called after __load_random_post_from_random_hashtag()
        has loaded a specific post page.
        """
        chosen_comment = random.choice(self.__user_config[self.__account]['comment_list'])
        try:
            comment_text_field = self.__browser.find_element_by_xpath('//textarea[@aria-label=\"Add a comment…\"]')
            comment_text_field.click()
            comment_text_field = self.__browser.find_element_by_xpath('//textarea[@aria-label=\"Add a comment…\"]')
            comment_text_field.send_keys(chosen_comment)
            comment_text_field.send_keys(Keys.ENTER)
        except common.exceptions.NoSuchElementException:
            logging.error(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S - ') + f'Could not find the comment field on the page {self.__browser.current_url}')
        except:
            logging.error(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S - ') + f'An unknown error occurred on the page {self.__browser.current_url}')

    def __follow_random_account_from_post(self):
        raise NotImplementedError

    """
    API Methods
    """

    def start(self, account: str):
        num_liked, num_commented = 0, 0
        self.__account = account
        self.__browser.get(self.__sys_config['ig_login_url'])
        self.__login(account)
        time.sleep(self.__seconds_to_sleep_after_login)
        while num_liked < self.__user_config[account]['likes_per_run'] or \
                num_commented <= self.__user_config[account]['comments_per_run']:
            if num_liked < self.__user_config[account]['likes_per_run']:
                self.__load_random_post_from_random_hashtag()
                self.__like_current_post()
                num_liked += 1
                time.sleep(self.__seconds_to_sleep_after_like)
            if num_commented < self.__user_config[account]['comments_per_run']:
                self.__load_random_post_from_random_hashtag()
                self.__comment_on_current_post()
                num_commented += 1
                time.sleep(self.__seconds_to_sleep_after_comment)
        # self.__follow_random_account_from_post()
