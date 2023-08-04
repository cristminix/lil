from robots.page import Page
from robots.form import Form
from robots.fn import log, lang
######################################################
# ADD PAGE FOR GUESS
######################################################
class LoginPasswdPage(Page):
    def __init__(self, page_name):
        super().__init__(page_name)
        self.setForm(Form(page_name, "form.login__form"))
        self.form.setUrlNotSuccessPattern(r"checkpoint/lg/login-submit")
        self.form.setUrlCheckPointPattern(r"checkpoint/challenge")
        self.form.setUrlSuccessPattern(r"https://www\.linkedin\.com/learning/")    

    def guess(self, content):
        self.setContent(content)
        return self.form.exists()


login_passwd_page = LoginPasswdPage('login_passwd_page')