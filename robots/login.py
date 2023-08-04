from robots.fn import log,lang,errors
from robots.config import linkedin_url, linkedin_learning_url
import sys

class Login:
    def __init__(self, human, json_config):
        self.m_config=json_config
        self.human=human
        self.linkedin_learning_login_url =""
        self.already_loged_in=False
        self.account_setting = json_config.getData(["email","password","library_id","card_number","pin"])
        
    
    def alreadyLogedIn(self):
        return self.already_loged_in
    
    def getLoginUrl(self):
        unauth_page=self.human.getPage('unauthenticated_page')
        sign_in_btn=unauth_page.getSignInBtn()
        if sign_in_btn:
            self.linkedin_learning_login_url=sign_in_btn.attr('href')
            log(lang("login_url",self.linkedin_learning_login_url),verbose=True)
        else:
            errors(lang('could_not_find_login_url'),exit_progs=True)
        return self.linkedin_learning_login_url
    
    def start(self):
        pass