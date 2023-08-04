import os
from pathlib import Path
import json
from robots.fn import writeFile,log,lang,errors
class JsonConfig:
    def __init__(self, path="config.json"):
        self.path=path
        self.data={}
        self.load()
    
    def load(self):
        if not os.path.exists(self.path):
            writeFile(self.path, "{}")
        try:
            self.data = json.loads(Path(self.path).read_text()) 
        except Exception as exception:
            errors(lang("could_not_load_json_file", self.path),exception) 

    def commit(self):
        try:
            Path(self.path).write_text(json.dumps(self.data))  
            return True  
        except Exception as exception:
            errors(lang("could_not_write_json_file", self.path),exception)
            return False
        
    def set(self,key,val,commit=True):
        self.data[key]=val
        if commit:
            self.commit()
    
    def get(self, key):
        if key in self.data:
            return self.data[key]
        return None
    def getData(self, props=None):
        # if props:

        return self.data