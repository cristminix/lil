from robots.page import Page
from robots.form import Form
from robots.fn import log, lang
######################################################
# ADD PAGE FOR GUESS
######################################################
class LoginEmailPage(Page):
    def __init__(self, page_name):
        super().__init__(page_name)
        self.setForm(Form(page_name, "form#auth-id-form"))

        self.form.setUrlSuccessPattern(r"uas/login\?session_key=")
        self.form.setUrlCheckPointPattern(r"checkpoint/challenge")

    def guess(self, content):
        self.setContent(content)
        return self.form.exists()


login_email_page = LoginEmailPage('login_email_page')