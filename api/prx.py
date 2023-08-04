from robots.fn import slugify,log,lang,deleteFile
from robots.human import Human
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir

import os
class Prx:
    def __init__(self, human=None,m_prx=None):
        if not human:
            human=Human(cookie_path,browser_cache_dir)
        self.human = human
        self.page_name= ""
        self.cache_path= ""
        self.m_prx=m_prx
    
    def getHuman(self):
        return self.human
    
    def getCachePath(self):
        return self.cache_path
    
    def getPageName(self):
        return self.page_name
    
    def get(self, url, no_cache=False):
        self.human.setSaveResp(False)
        self.page_name=slugify(url.replace('/','-')).replace('https--wwwlinkedincom','ll')
        content=""
        self.cache_path = '%s/%s-1.html' % (browser_cache_dir,self.page_name)
        # print(cache_path)
        if not no_cache:
            
            if self.m_prx:
                prx_cache = self.m_prx.getByPageName(self.page_name)
                if prx_cache:
                    log(lang('prx_loading_from_cache_m_prx')+" "+self.page_name)
                    content = prx_cache.content

            elif os.path.exists(self.cache_path):
                log(lang('prx_loading_from_cache')+" "+self.page_name)
                with open(self.cache_path, 'r') as file:
                    content = file.read()
        if not content:
            content = self.human.browse(url, self.page_name)
            self.m_prx.create(self.page_name, content)
        
        self.human.setSaveResp(True)

        if os.path.exists(self.cache_path):
            deleteFile(self.cache_path)


        
        return content