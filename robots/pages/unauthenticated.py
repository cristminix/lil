from robots.page import Page
from robots.fn import log, lang
######################################################
# ADD PAGE FOR GUESS
######################################################
class UnAuthenticatedPage(Page):
    def getSignInBtn(self):
        return self.findNode("a",startsWith='Sign in')

    def guess(self, content):
        self.setContent(content)

        valid_page = False
        if self.content:
            sign_in_btn = self.getSignInBtn()
            if len(sign_in_btn)>0:
                log(lang("sign_in_btn_found"),'nd',verbose=True)
        
                valid_page =  True

        return valid_page


unauthenticated_page = UnAuthenticatedPage('unauthenticated_page')