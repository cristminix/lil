#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))

from robots.fn import errors, log, lang,fmtTime
from robots.datasource import DataSource
from config.cli_config import db_path
from api.course import CourseApi

def course(args):
    course_id = args.id
    show_duration = args.show_duration
    ds = DataSource(db_path)
    api_course=CourseApi(ds)
    course_list = ds.m_course.getList()
    # print(course_list)
    if not course_id:
        
        print("\nList of saved courses:\n")
        for course in course_list:
            by_authors=[]
            for author in course.authors:
                by_authors.append(author.name)
            print(f"  {course.id}. {course.title}  By {','.join(by_authors)}")
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
        output_buffer += f"\n {course.description}\n"

        sections = ds.m_section.getListCourseId(course_id)
        # section_number = 1
        for section in sections:
            output_buffer += f"\n\n  {section.title}\n"
            toc_number=1
            tocs = ds.m_toc.getListBySectionId(section.id)
            for toc in tocs:
                # stream_loc_keys = ""
                # stream_locs = ds.m_stream_location.getByTocId(toc.id)
                # if not stream_locs:
                #     stream_locs = api_course.getStreamLocs(toc)
                # if stream_locs:
                #     stream_loc_keys = list(stream_locs)
                #     if len(stream_loc_keys)>0:
                #         stream_loc_keys = f"[{','.join(stream_loc_keys)}]"
                #     else:
                #         stream_loc_keys = ""
                
                # transcript_keys = ""
                # transcripts = ds.m_transcript.getByTocId(toc.id)
                # if not transcripts:
                #     transcripts = api_course.getTranscripts(toc)
                # if transcripts:
                #     transcript_keys = list(transcripts)
                #     if len(transcript_keys)>0:
                #         transcript_keys = f"[{','.join(transcript_keys)}]"
                #     else:
                #         transcript_keys = ""
                dur = 0
                try:
                    dur=int(toc.duration)
                except:
                    pass
                duration=""
                if show_duration:
                    duration=f"({fmtTime(dur)})"
                output_buffer += f"\n     {toc_number}. {toc.title} {duration}"
                toc_number += 1
            # section_number += 1

        print(f"{output_buffer}\n")
