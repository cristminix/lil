from robots.page import Page
from robots.fn import log, lang, getMeta
######################################################
# ADD PAGE FOR GUESS
######################################################
class AuthenticatedPage(Page):
    def guess(self, content):
        self.setContent(content)
        meta_guest = getMeta('isGuest',self.doc)
        # print(meta_guest,"ND")
        return meta_guest == "false"


authenticated_page = AuthenticatedPage('authenticated_page')