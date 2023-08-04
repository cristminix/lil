from robots.browser import Browser
from robots.fn import log,lang,writeResp, clearCookies
import sys
import time
class Human:
    def __init__(self, cookie_path, browser_cache_dir):
        self.browser = Browser(cookie_path)
        self.pages = {} 
        self.forms = {} 
        self.browse_counts = {}
        self.browser_cache_dir=browser_cache_dir
        self.save_resp = True
    
    def getBrowser(self):
        return self.browser
    def setSaveResp(self, flag):
        self.save_resp = flag    
    def addPage(self, page):
        self.pages[page.getName()] = page
        page.setHuman(self)
        return self


    def addForm(self, form):
        self.form[form.getName()] = form
        form.setHuman(self)
        return self

    def getBrowseCount(self, page_name):
        if not page_name in self.browse_counts:
            self.browse_counts[page_name] = 0
        
        self.browse_counts[page_name] += 1

        return self.browse_counts[page_name]    
    def getPage(self,page_name):
        if not page_name in self.pages:
            log(lang('human_doesnt_have_page',page_name),'ERR')
            print(self.pages)
            sys.exit()
        
        return self.pages[page_name]

    def guessPage(self, page_name, content):
        return self.getPage(page_name).guess(content)
    
    def browse(self, url, page_name):
        # time.sleep(1)
        ok=False
        wait_time=0
        retry_count=0
        max_retry_count=3
        resp=None
        while not ok:
            if wait_time > 0:
                log(f"wait for {wait_time} seconds")
                time.sleep(wait_time)
            if retry_count > 0:
                log(f"retry count : {retry_count}")
            
            log(lang('human_start_browsing',url),verbose=True)
            resp= self.browser.get(url)

            if resp.status_code != 200:
                retry_count += 1
                wait_time += 1
                
                # if status_code == 401:
                #     refresh_stream_locs=True

                if retry_count > max_retry_count:
                    errors(f"Max retry count exceed max : {max_retry_count}")
                    ok=True
            else:
                ok=True
        
        
        log(lang('human_browsing_resp_code',resp.status_code),verbose=True)
        if resp.status_code == 200 and self.save_resp:
            writeResp(resp, page_name, self.getBrowseCount(page_name), self.browser_cache_dir)
        return resp.text
        
        return None

    def getBrowser(self):
        return self.browser
        
    def fillForm(self,form_name, key, value):
        self.forms[form_name].setDataItem(key, value)

    def clearCookies(self):
        log(lang('human_clear_cookies'),verbose=True)
        clearCookies(self.browser.cookie_path)
        self.getBrowser().reloadCookies()

    
    
    
               