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


from download_section import download_section
from download_toc import download_toc
from download_what import download_what

def getAttr(obj,key):
    try:
        return getattr(obj,key)
    except Exception as e:
        print(e)
    return None

def download(args):
    # print(args)
    course_id = getAttr(args,'id')
    run = getAttr(args,'run')
    section_id = getAttr(args,'section_id')
    toc_id = getAttr(args,'toc_id')
    transcript_lang = getAttr(args,'transcript_lang')
    transcript_only=getAttr(args,'transcript_only')
    fmt=getAttr(args,'fmt')
    stream_to_pipe=getAttr(args,'stream_to_pipe')
    refresh_stream_location=getAttr(args,'refresh_stream_location')
    what=getAttr(args,'what')

    ds = DataSource(db_path)
    api_course=CourseApi(ds)
    course_list = ds.m_course.getList()
    download_mode="course_mode"
    download_transcript=False
    
    if run:
        # if course_id:
        #     print(f"course id : {course_id}")
        
        if toc_id:
            # print(f"toc id : {toc_id}")
            download_mode="toc_mode"
            if section_id or course_id:
                if not stream_to_pipe:
                    log('Option ignored -i|--id or -si|--section-id, if you have specify -ti|--toc-id')
        elif section_id:
            download_mode="section_mode"
            if course_id:
             log('Option ignored -i|--id , if you have specify -si|--section-id')
        # if transcript_lang:
        #     print(f"transcript lang : {transcript_lang}")

        if not stream_to_pipe:
            print("Download manager is running")
        if transcript_only:
            if not transcript_lang:
                errors("If -to|--transcript-only flag was on, you must specify -tl|--transcript-lang, example -tl en", exit_progs=True)
            if not stream_to_pipe:
                print("Download transcripts only.")
        if not fmt:
            errors("You must specify -f|--fmt, example -f 720", exit_progs=True)
        if not what:
            if download_mode == "course_mode":
                pass
            if download_mode == "section_mode":
                download_section(ds, api_course, section_id, fmt, transcript_lang, transcript_only)
            if download_mode == "toc_mode":
                download_toc(ds, api_course, toc_id, fmt, transcript_lang, transcript_only,stream_to_pipe)
            if download_mode == "course_mode":
                pass
        else:
            print(f"{what}")
            if not course_id:
                errors(f"you must specify course id -i|--id",exit_progs=True)
            if not fmt:
                errors("You must specify -f|--fmt, example -f 720", exit_progs=True)
            # if what == "pl" or what == 'playlist':

            download_what(ds, api_course, course_id, fmt, transcript_lang, what)
            # pass
        # if download_mode == "transcript_mode":
        #     log('Download in transcript mode')
        #     pass
        sys.exit()
    # print(course_list)
    if not course_id:
        print("\nList of saved courses:\n")
        for course in course_list:
            by_authors=[]
            for author in course.authors:
                by_authors.append(author.name)
            sloc_fmt = ds.m_course.getAvailableStreamFmt(course.id)
            # print(sloc_fmt)   
            trans_lang = ds.m_course.getAvailableTransLang(course.id)
            # print(trans_lang)    
            print(f"  [{GREEN}i{RESET}:{RED}{course.id}{RESET}]. {course.title} By {','.join(by_authors)}")
            print(f"     Available fmt [{GREEN}f{RESET}:{RED}{','.join(sloc_fmt)}{RESET}]")
            print(f"     Available transcript lang [{GREEN}tl{RESET}:{RED}{','.join(trans_lang)}{RESET}]\n")
        # print("\n")
        print("  description:\n")
        print(f"    {GREEN}i{RESET}  : {RED}Course id{RESET}")
        print(f"    {GREEN}f{RESET}  : {RED}Media format{RESET}")
        print(f"    {GREEN}tl{RESET} : {RED}Transcript lang{RESET}\n")
    else:
        
        course = ds.m_course.get(course_id)
        if not course:
            errors(f"Course with id {course_id} not found.", exit_progs=True)
        if refresh_stream_location:
            print(f"Course : {course.title}")
            choice = input("Are you sure wanna refresh stream location for this course?(y/n)[n]:")
            choice=choice.lower()

            if choice != 'y':
                refresh_stream_location=False

        output_buffer = f"\n\n {course.title}"
        by_authors=[]
        for author in course.authors:
            by_authors.append(author.name)
        output_buffer += f"\n By {','.join(by_authors)}\n"

        sections = ds.m_section.getListCourseId(course_id)
        # section_number = 1
        for section in sections:
            output_buffer += f"\n\n  [{GREEN}si{RESET}:{section.id}] {section.title}\n"
            toc_number=1
            tocs = ds.m_toc.getListBySectionId(section.id)
            for toc in tocs:
                stream_locs=None
                stream_loc_keys = ""

                if not refresh_stream_location:
                    stream_locs = ds.m_stream_location.getByTocId(toc.id)
                if not stream_locs:
                    stream_locs = api_course.getStreamLocs(toc,refresh=refresh_stream_location)
                if stream_locs:
                    stream_loc_keys = list(stream_locs)
                    if len(stream_loc_keys)>0:
                        stream_loc_keys = f"[{GREEN}f{RESET}:{RED}{','.join(stream_loc_keys)}{RESET}]"
                    else:
                        stream_loc_keys = ""
                
                transcript_keys = ""
                transcripts = ds.m_transcript.getByTocId(toc.id)
                if not transcripts:
                    transcripts = api_course.getTranscripts(toc)
                if transcripts:
                    transcript_keys = list(transcripts)
                    if len(transcript_keys)>0:
                        transcript_keys = f"[{GREEN}tl{RESET}:{RED}{','.join(transcript_keys)}{RESET}]"
                    else:
                        transcript_keys = ""
                # toc_id = "ti:%d" % toc.id
                output_buffer += f"\n    [{GREEN}ti{RESET}:{toc.id}] {toc_number}. {toc.title} {stream_loc_keys} {transcript_keys}"
                toc_number += 1
            # section_number += 1

        print(f"{output_buffer}\n")
        print("\n  description:\n")
        print(f"    {GREEN}si{RESET} : Section id")
        print(f"    {GREEN}ti{RESET} : Toc id\n")
        print("\n  example:\n")
        print("  To download all transcript only on section id 13:\n")
        print("  ./lil.py download --section-id 13 --fmt 400  --transcript-only --transcript-lang id --run")
        print("  ./lil.py download -si 13 -f 400  -to -tl id -run")
        print("\n  To stream toc id 23 on a pipe and play with ffplay: \n")
        print("  ./lil.py download --toc-id 23 --fmt 640 --stream-to-pipe -run|ffplay -i pipe:")
        print("  ./lil.py download -ti 23 -f 640 -stp -run|ffplay -i pipe:")
        print("\n")
