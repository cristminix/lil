from robots import Login
from robots.fn import log,lang,errors
from robots.config import linkedin_url, linkedin_learning_url
import sys
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir,download_dir

import browser_cookie3
import http.cookiejar
import json
import os
class LoginBrowserCookie(Login):
    def start(self):    
        browser_name=self.m_config.get('browser_cookie_browser')

        log(lang('using_account',"Browser Cookie"))
        log(lang('browser_name')+f" {browser_name}")

        bc3_method = getattr(browser_cookie3, browser_name)

        if bc3_method:
            try:   
                cookie_jar = bc3_method(domain_name='www.linkedin.com')
                # print(cookie_jar)
                cookies_dict = {}
                for cookie in cookie_jar:
                    cookies_dict[cookie.name] = cookie.value
                # print(cookies_dict)
                file_path = cookie_path
                with open(file_path, 'w') as json_file:
                    json.dump(cookies_dict, json_file)
                    file_rel_path = os.path.relpath(file_path, os.getcwd())
                    log(f"Cookie jar saved to {file_rel_path}.")
                self.human.getBrowser().reloadCookies()

                content = self.human.browse(linkedin_learning_url, 'linkedin_learning_homepage')
                
                if self.human.guessPage('authenticated_page',content):
                    log(lang("you_are_loged_in"),'info')
                    self.already_loged_in=True
            except Exception as e:
                errors("Could not load browser cookies", e)
                errors(f"You select : {browser_name}, if you using another browser, please fix in Account Settings -> Import Browser Cookies-> Change Browser Name")

        else:
            errors(f"Unknown browser name : {browser_name}, please fix in Account Settings -> Import Browser Cookies-> Change Browser Name")
        return self.already_loged_in
def login(human, json_config):
    li = LoginBrowserCookie(human, json_config)
    li.start()
    return li.alreadyLogedIn()   
