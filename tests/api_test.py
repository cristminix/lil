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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage   : ./api_test.py <course_url>")
        print("example : ./api_test.py https://www.linkedin.com/learning/learning-next-js")
        sys.exit()
    course_url = sys.argv[1]
    if not validators.url(course_url):
        print(f"{course_url} is not a valid url")
        sys.exit()
    
    if not isLinkedinLearningUrl(course_url):
        print(f"{course_url} is not a valid linkedin learning url")
        sys.exit()
    
    ds = DataSource(db_path)
    api_course=CourseApi(ds)

    course_slug = api_course.getCourseSlugFromUrl(course_url)
    course = api_course.getCourseInfo(course_slug)

    if course:
        print(course)
        # sys.exit()
    else:
        sys.exit()
    authors = api_course.getAuthors(course_slug)
    if authors:
        print(authors)
    # sys.exit()

    sections = api_course.getCourseSections(course_slug)
    if sections:
        print(sections)
    else:
        sys.exit()
    tocs = api_course.getCourseTocs(course_slug)

    for section in sections:
        toc_list = tocs[section.slug]
        # setream_locations = api_course.getStreamLocs(toc.item_star)
        for toc in toc_list:
            stream_locations = api_course.getStreamLocs(toc)
            # print(stream_locations)
            #1627776000
            #1690895598000
            for fmt in stream_locations:
                if fmt=="640":
                    sloc=stream_locations[fmt]
                    expiresAt=sloc.expiresAt
                    expired = isTimeExpired(expiresAt)
                    if not expired:
                        download_dir = getDownloadDir(course.slug)
                        output_filename = f"{download_dir}/{toc.slug}-{fmt}.mp4"
                        url=sloc.url
                        # print(output_filename)
                        downloadFile(url,output_filename)
                        # sys.exit()


            # transcripts = api_course.getTranscripts(toc)
            # print(transcripts)