#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))

from robots.fn import errors, log, lang,  pq, dict2htmTable, formatBytes,RED,GREEN,BLUE,RESET,BLACK,WHITE
from robots.datasource import DataSource
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir,download_dir
from api.course import CourseApi, isLinkedinLearningUrl,isTimeExpired,downloadFile,getDownloadDir
import validators
import re
import time

# import math
def cache(args):
    clear=args.clear
    ds = DataSource(db_path)
    if clear:
        ds.m_prx.clear()
        print(f"Cache cleared")
    else:
        cache_sz=formatBytes(ds.m_prx.getSize())
        print(f"Cache size: {cache_sz}")

    # print(args)
    pass