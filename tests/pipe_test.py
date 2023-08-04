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
# from tabulate import tabulate


if __name__ == '__main__':
    url="https://www.linkedin.com/dms/C560DAQEg_8BvPk7EcQ/learning-original-video-iphone-360/0/1603989082995?ea=95231473&ua=153712024&e=1691057763&v=beta&t=Y7t2fHZ49F_WmDYuXRf_mMXeGuFCTWODJg6IsvCWSu8"
    downloadPipe(url)