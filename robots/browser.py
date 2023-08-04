from robots.fn import loadCookies, saveCookies, log, lang, errors
import requests
from robots import config

class Browser:
    def __init__(self, cookie_path):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        })
        self.cookie_path= cookie_path
        self.setUserAgent(config.ua)
        loadCookies(self.session, self.cookie_path)
        self.url = ""
        self.last_resp=None
    
    def reloadCookies(self):
        log('Reload cookies')
        loadCookies(self.session, self.cookie_path)

    def getSession(self):
        return self.session
    
    def setReferer(self, referer):
        self.session.headers.update({"referer": referer})

    def setUserAgent(self,UA):
        self.session.headers.update({"User-Agent": UA})
    
    def getLastResp(self):
        return self.last_resp

    def get(self,url):
        try:
            resp = self.session.get(url)
            saveCookies(self.session, self.cookie_path)
            self.last_resp=resp

            return resp
        except Exception as e:
            errors(lang('browser_get_error'),e)
        
        return None
    
    def post(self,url, data=None, allow_redirects=True):
        try:
            resp = self.session.post(url, data=data, allow_redirects=allow_redirects)
            saveCookies(self.session, self.cookie_path)

            return resp
        except Exception as e:
            errors(lang('browser_post_error'),e)
        
        return None