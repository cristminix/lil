from robots.fn import log,lang,parseFormPayload,writeResp,matchUrl
class Form:
    def __init__(self,name, selector=None,filter=None):
        self.name = name
        self.data={}
        self.selector = selector
        self.selector_filter=filter
        self.action = ""
        self.browser=None
        self.human=None
        self.page=None
        self.last_resp=None
        self.url_success_pattern=None
        self.url_not_success_pattern=None
        self.url_checkpoint_pattern=None
    
    def setUrlCheckPointPattern(self, pattern):
        self.url_checkpoint_pattern = pattern

    def setUrlSuccessPattern(self, pattern):
        self.url_success_pattern = pattern

    def setUrlNotSuccessPattern(self, pattern):
        self.url_not_success_pattern = pattern
    
    def postValidationSuccess(self):
        print(self.url_success_pattern)
        print(self.last_resp.url)
        if self.url_success_pattern:
            return matchUrl(self.url_success_pattern, self.last_resp.url)
        return False
    
    def postValidationNotSuccess(self):
        
        if self.url_not_success_pattern:
            return matchUrl(self.url_not_success_pattern, self.last_resp.url)
        return False
    def postValidationPattern(self,pattern):
        return matchUrl(pattern, self.last_resp.url)

    def postValidationCheckPoint(self):
        if self.url_checkpoint_pattern:
            return matchUrl(self.url_checkpoint_pattern, self.last_resp.url)
        return False
    
    def getLastResp(self):
        return self.last_resp
    
    def setPage(self, page):
        self.page=page
        self.human=page.getHuman()
    def getName(self):
        return self.name
    
    def setBrowser(self, browser):
        self.browser = browser
    
    def setHuman(self, human):
        if human:
            self.human = human
            self.browser = self.human.getBrowser()
    
    def setAction(self, action):
        self.action = action
    
    def setData(self, key_or_data, value=None):
        if type(key_or_data) is str:
            if value:
                self.data[key_or_data]=value
        else:        
            self.data = key_or_data
    
    def exists(self, doc=None):
        return len(self.getNd(doc)) > 0
    
    def getNd(self, doc=None):
        if not doc:
            doc = self.page.getDoc()
        if doc:    
            return doc(self.selector)
        return []
    #set data based on current form input nodes
    def setPayload(self, doc):
        self.data= parseFormPayload(doc, self.selector) 

    # def existsInContent(self, content):
    #     pass
    
    def post(self):
        log(lang('form_start_post',self.action),verbose=True)
        log(lang('form_post_payload',self.data),verbose=True)

        resp = self.browser.post(self.action, data=self.data,allow_redirects=True)
        self.last_resp=resp

        log(lang('form_post_resp_code',resp.status_code),verbose=True)
        
        writeResp(resp, "%s_form" % (self.name), 1)
        return resp.text