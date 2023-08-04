from robots.page import Page
from robots.form import Form
from robots.fn import log, lang
######################################################
# ADD PAGE FOR GUESS
######################################################
class LoginLibraryPage(Page):
    def __init__(self, page_name):
        super().__init__(page_name)
        self.setForm(Form(page_name, "form#library-tenant-form"))
        # self.form.setUrlSuccessPattern(r"https://www\.linkedin\.com/learning/")  

    def guess(self, content):
        self.setContent(content)
        return self.form.exists()


login_library_page = LoginLibraryPage('login_library_page')