#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))

from robots.fn import errors, log, lang,  pq, dict2htmTable, RED,GREEN,BLUE,RESET,BLACK,WHITE
from robots.datasource import DataSource
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir,download_dir
from api.course import CourseApi, isLinkedinLearningUrl,isTimeExpired,downloadFile,getDownloadDir
import validators
import re
import time
# from tabulate import tabulate


def fetch(args):
    course_url = args.url
    # if len(sys.argv) < 2:
    #     print("usage   : ./api_test.py <course_url>")
    #     print("example : ./api_test.py https://www.linkedin.com/learning/learning-next-js")
    #     sys.exit()
    # course_url = sys.argv[1]
    if not validators.url(course_url):
        errors(f"{course_url} is not a valid url", exit_progs=True)
        sys.exit()
    
    if not isLinkedinLearningUrl(course_url):
        errors(f"{course_url} is not a valid linkedin learning url", exit_progs=True)
    
    ds = DataSource(db_path)
    api_course=CourseApi(ds)

    course_slug = api_course.getCourseSlugFromUrl(course_url)
    course = api_course.getCourseInfo(course_slug)

    if course:
        print(f"Fetch course ok")
        # sys.exit()
    else:
        errors(f"Failed to fetch course url : {course_url}", exit_progs=True)

    authors = api_course.getAuthors(course_slug)
    if authors:
        print(f"Fetch course authors ok")
    else:
        errors(f"Failed to fetch course authors")

    sections = api_course.getCourseSections(course_slug)
    if sections:
        print(f"Fetch course sections ok {len(sections)}")
    else:
        errors(f"Failed to fetch course sections course : {course.title}", exit_progs=True)

    tocs = api_course.getCourseTocs(course_slug)
    if not tocs:
        errors(f"Failed to fetch course tocs course : {course.title}", exit_progs=True)

    for section in sections:
        toc_list = tocs[section.slug]
        # setream_locations = api_course.getStreamLocs(toc.item_star)
        for toc in toc_list:
            stream_locations = api_course.getStreamLocs(toc)
            if not stream_locations:
                errors(f"Failed to fetch stream locations toc : {toc.title}")
            else:
                print(f"Fetch stream locations [{','.join(list(stream_locations))}]")
            transcripts = api_course.getTranscripts(toc)
            if not transcripts:
                errors(f"Failed to fetch transcripts toc : {toc.title}")
            else:
                print(f"Fetch transcripts [{','.join(list(transcripts))}]")

            