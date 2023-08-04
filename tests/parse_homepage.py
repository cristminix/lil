#!/usr/bin/env python3

import requests
import http.cookiejar
import sys
import re
import json
from robots.fn import getMeta, pq
file_path = 'html_cache/linkedin_learning_homepage-1.html'

# Open the file in read mode ('r')
meta_config={
    "learning-web/config/environment":"unquote|dict",
    "spark/hash-includes":"unescape|dict"
}
with open(file_path, 'r') as file:
    content = file.read()
    doc = pq(content)
    meta_data=getMeta("learning-web/config/environment",doc,meta_config)
    print(meta_data)



    

