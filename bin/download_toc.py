#!/usr/bin/env python3
import sys
import os
import time
sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))

from robots.fn import errors, log, lang, RED,GREEN,BLUE,RESET,BLACK,WHITE
from api.course import CourseApi, isLinkedinLearningUrl,isTimeExpired,downloadFile,getDownloadDir,downloadPipe

def download_toc(ds, api_course, toc_id, fmt, transcript_lang, transcript_only, stream_to_pipe):
    if not stream_to_pipe:
        log('Download in toc mode')
    if stream_to_pipe:
        if not stream_to_pipe:
            log("Stream to pipe mode is on")
        if transcript_only:
            if not stream_to_pipe:
                log(f"When -stp|--stream-to-pipe was on you , -to|--transcript-only, -tl|--transcript-lang was ignored")
        
        transcript_only = False
        transcript_lang = None

    toc = ds.m_toc.get(toc_id)
    if not toc:
        errors(f"Toc with id: {toc_id} not found", exit_progs=True)
    section = ds.m_section.get(toc.sectionId)
    if not section:
        if not stream_to_pipe:
            errors(f"Section with id: {section_id} not found")
    course = ds.m_course.get(section.courseId)
    if course and section:
        if not stream_to_pipe:
            print(f"Section title: {section.title} , Course : {course.title}")
    if not stream_to_pipe:
        print(f"Selected fmt: {fmt}")
        print(f"Selected transcript lang: {transcript_lang}")
    availableFmt = ds.m_course.getAvailableStreamFmt(section.courseId)
    availableFmt_str=','.join(list(availableFmt))
    if not stream_to_pipe:
        log(f"available fmt:[{availableFmt_str}]")
        log("Checking available fmt")
    if not fmt in availableFmt:
        errors(f"fmt : {fmt} is not available, valid fmt: {availableFmt_str}",exit_progs=True)
    else:
        if not stream_to_pipe:
            log(f"fmt : {fmt} is Ok")
        
    if transcript_lang:
        availableTrans = ds.m_course.getAvailableTransLang(section.courseId)
        availableTrans_str=','.join(list(availableTrans))
        if not stream_to_pipe:
            log(f"available transcript lang:[{availableTrans_str}]")
        if not transcript_lang in availableTrans:
            errors(f"transcript lang : {transcript_lang} is not available, valid transcript lang: {availableTrans_str}",exit_progs=True)
        else:
            if not stream_to_pipe:
                log(f"transcript lang : {transcript_lang} is Ok")
    
    toc_number=1
    tocs = ds.m_toc.getListBySectionId(section.id)
    download_transcripts=True
    if not transcript_lang:
        download_transcripts=False
    if download_transcripts:
        transcripts = ds.m_transcript.getByTocId(toc.id)
        if not transcripts:
            transcripts = api_course.getTranscripts(toc)
        if transcripts:
            ok=False
            wait_time=0
            retry_count=0
            max_retry_count=3
            refresh_transcripts=False
            while not ok:
                if wait_time > 0:
                    log(f"wait for {wait_time} seconds")
                    time.sleep(wait_time)
                if retry_count > 0:
                    log(f"retry count : {retry_count}")
                
                skip=False
                download_dir = getDownloadDir(course.slug)
                media_output_filename = f"{download_dir}/{toc.slug}-{fmt}.vtt"
                mo_rel_path = os.path.relpath(media_output_filename, os.path.dirname(__file__))
                if os.path.exists(media_output_filename) and retry_count == 0:
                    print(f"{mo_rel_path} already exists")
                    choice = input("overwrite ? (y,n)[n]:")
                    choice = choice.lower()
                    if choice != 'y':
                        skip=True
                        ok=True
                if not skip:
                    url=transcripts[transcript_lang].url
                    status_code = downloadFile(url,media_output_filename)
                    if status_code != 200:
                        retry_count += 1
                        wait_time += 1
                        refresh_transcripts=True
                        if retry_count > max_retry_count:
                            errors(f"Max retry count exceed max : {max_retry_count}")
                            ok=True
                    else:
                        ok=True
                else:
                    print("skiped")
    
    if not transcript_only: 
        stream_locs = ds.m_stream_location.getByTocId(toc.id)

        if not stream_locs:
            stream_locs = api_course.getStreamLocs(toc)
        if stream_locs:
            ok=False
            wait_time=0
            retry_count=0
            max_retry_count=3
            refresh_stream_locs=False
            while not ok:
                if wait_time > 0:
                    log(f"wait for {wait_time} seconds")
                    time.sleep(wait_time)
                if retry_count > 0:
                    log(f"retry count : {retry_count}")
                
                if refresh_stream_locs:
                    log(f"refershing stream locs")
                    stream_locs = api_course.getStreamLocs(toc,refresh=True)

                # print(f"{stream_locs[fmt]}")
                if not stream_to_pipe:
                    skip=False
                    download_dir = getDownloadDir(course.slug)
                    media_output_filename = f"{download_dir}/{toc.slug}-{fmt}.mp4"
                    mo_rel_path = os.path.relpath(media_output_filename, os.path.dirname(__file__))
                    if os.path.exists(media_output_filename) and retry_count == 0:
                        print(f"{mo_rel_path} already exists")
                        choice = input("overwrite ? (y,n)[n]:")
                        choice = choice.lower()
                        if choice != 'y':
                            skip=True
                            ok=True
                    if not skip:
                        url=stream_locs[fmt].url
                        status_code = downloadFile(url,media_output_filename)
                        if status_code != 200:
                            retry_count += 1
                            wait_time += 1
                            
                            if status_code == 401:
                                refresh_stream_locs=True

                            if retry_count > max_retry_count:
                                errors(f"Max retry count exceed max : {max_retry_count}")
                                ok=True
                        else:
                            ok=True
                    else:
                        print("skiped")
                else:
                    # print("Stream to pipe")
                    url=stream_locs[fmt].url
                    status_code = 200
                    try:
                        status_code=downloadPipe(url)
                    except:
                        pass
                    if status_code != 200:
                        retry_count += 1
                        wait_time += 1
                        
                        if status_code == 401:
                            refresh_stream_locs=True

                        if retry_count > max_retry_count:
                            # errors(f"Max retry count exceed max : {max_retry_count}")
                            ok=True
                    else:
                        ok=True