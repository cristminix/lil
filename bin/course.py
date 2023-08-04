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

def course(args):
    course_id = args.id
    ds = DataSource(db_path)
    api_course=CourseApi(ds)
    course_list = ds.m_course.getList()
    # print(course_list)
    if not course_id:
        print("\nList of saved courses:\n")
        for course in course_list:
            by_authors=" by "
            for author in course.authors:
                by_authors+=f"{author.name},"
            print(f"  {course.id}. {course.title} {by_authors}")
        print("\n")
    else:
        course = ds.m_course.get(course_id)
        if not course:
            errors(f"Course with id {course_id} not found.", exit_progs=True)
        
        output_buffer = f"\n\n {course.title}"
        by_authors=[]
        for author in course.authors:
            by_authors.append(author.name)
        output_buffer += f"\n By {','.join(by_authors)}\n"

        sections = ds.m_section.getListCourseId(course_id)
        # section_number = 1
        for section in sections:
            output_buffer += f"\n\n  {section.title}\n"
            toc_number=1
            tocs = ds.m_toc.getListBySectionId(section.id)
            for toc in tocs:
                stream_loc_keys = ""
                stream_locs = ds.m_stream_location.getByTocId(toc.id)
                if not stream_locs:
                    stream_locs = api_course.getStreamLocs(toc)
                if stream_locs:
                    stream_loc_keys = list(stream_locs)
                    if len(stream_loc_keys)>0:
                        stream_loc_keys = f"[{','.join(stream_loc_keys)}]"
                    else:
                        stream_loc_keys = ""
                
                transcript_keys = ""
                transcripts = ds.m_transcript.getByTocId(toc.id)
                if not transcripts:
                    transcripts = api_course.getTranscripts(toc)
                if transcripts:
                    transcript_keys = list(transcripts)
                    if len(transcript_keys)>0:
                        transcript_keys = f"[{','.join(transcript_keys)}]"
                    else:
                        transcript_keys = ""

                output_buffer += f"\n     {toc_number}. {toc.title} {stream_loc_keys} {transcript_keys}"
                toc_number += 1
            # section_number += 1

        print(f"{output_buffer}\n")
