#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))

from robots.fn import errors, log, lang,  pq, dict2htmTable, RED,GREEN,BLUE,RESET,BLACK,WHITE
from robots.datasource import DataSource
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir,download_dir
from api.course import downloadPipe,CourseApi, isLinkedinLearningUrl,isTimeExpired,downloadFile,getDownloadDir
import validators
import re
import time
import sys
# from tabulate import tabulate
import requests
import browser_cookie3
import http.cookiejar
import json

if __name__ == '__main__':
    cookie_jar = browser_cookie3.chrome(domain_name='www.linkedin.com')
    print(cookie_jar)
    cookies_dict = {}
    for cookie in cookie_jar:
        cookies_dict[cookie.name] = cookie.value
    print(cookies_dict)
    file_path = cookie_path
    with open(file_path, 'w') as json_file:
        json.dump(cookies_dict, json_file)
        print(f"Cookie jar saved to {file_path}.")

    sys.exit()
    get_title = lambda html: re.findall(r'<title>(.*?)</title>', html, flags=re.DOTALL)[0].strip()
    url = 'https://www.linkedin.com/learning/'
    resp = requests.get(url,cookies=cj)
    title=get_title(resp.text)
    print(title)
    # url="https://www.linkedin.com/dms/C560DAQEg_8BvPk7EcQ/learning-original-video-iphone-360/0/1603989082995?ea=95231473&ua=153712024&e=1691057763&v=beta&t=Y7t2fHZ49F_WmDYuXRf_mMXeGuFCTWODJg6IsvCWSu8"
    # downloadPipe(url)