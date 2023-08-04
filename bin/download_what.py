#!/usr/bin/env python3
import sys
import os
import time
sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))
import urllib

from robots.fn import writeFile,errors, log, lang, RED,GREEN,BLUE,RESET,BLACK,WHITE
from api.course import CourseApi, isLinkedinLearningUrl,isTimeExpired,downloadFile,getDownloadDir

def download_what(ds, api_course, course_id, fmt, transcript_lang, what):
    is_ex_mode = what == 'ex' or what == 'exercise_file' or what == 'exercise'
    if not is_ex_mode:
        print(f"Selected fmt: {fmt}")
        print(f"Selected transcript lang: {transcript_lang}")
        availableFmt = ds.m_course.getAvailableStreamFmt(course_id)
        availableFmt_str=','.join(list(availableFmt))
        log(f"available fmt:[{availableFmt_str}]")
        log("Checking available fmt")
        if not fmt in availableFmt:
            errors(f"fmt : {fmt} is not available, valid fmt: {availableFmt_str}",exit_progs=True)
        else:
            log(f"fmt : {fmt} is Ok")
    
    what_to_downloads=[]
    if what == 'pl' or what == 'playlist':
        what_to_downloads = ['playlist']
    elif what == 'm' or what == 'media':
        what_to_downloads = ['media']
    elif what == 't' or what == 'transcript':
        what_to_downloads = ['transcript']
    elif is_ex_mode:
        what_to_downloads = ['exercise_file']
    else:
        what_to_downloads=['playlist','media','transcript','exercise_file']
    print(f"Download {','.join(what_to_downloads)}")

    if 'transcript' in what_to_downloads:
        if transcript_lang:
            availableTrans = ds.m_course.getAvailableTransLang(course_id)
            availableTrans_str=','.join(list(availableTrans))
            log(f"available transcript lang:[{availableTrans_str}]")
            if not transcript_lang in availableTrans:
                errors(f"transcript lang : {transcript_lang} is not available, valid transcript lang: {availableTrans_str}",exit_progs=True)
            else:
                log(f"transcript lang : {transcript_lang} is Ok")
        else:
            errors("you must specify -tl|--transcript-lang, example -tl en", exit_progs=True)

    course = ds.m_course.get(course_id)

    if not course:
        errors(f"Course with id: {course_id} not found", exit_progs=True)
    

    if 'exercise_file' in what_to_downloads:
        exercise_file = ds.m_exercise_file.getByCourseId(course_id)
        # print(exercise_file)
        if not exercise_file:
            errors(f"Course id: {course_id} doesnt have exercise file")
        else:
            
            ok=False
            wait_time=0
            retry_count=0
            max_retry_count=3
            refresh_course=False
            while not ok:
                if wait_time > 0:
                    log(f"wait for {wait_time} seconds")
                    time.sleep(wait_time)
                if retry_count > 0:
                    log(f"retry count : {retry_count}")
                
                if refresh_course:
                    log(f"refershing course")
                    course = api_course.getCourseInfo(course.slug,refresh=True)
                    exercise_file = ds.m_exercise_file.getByCourseId(course_id)
                
                skip=False
                exercise_file_output_filename = f"{download_dir}/{exercise_file.name}"
                ex_rel_path = os.path.relpath(exercise_file_output_filename, os.path.dirname(__file__))
                
                if os.path.exists(exercise_file_output_filename):
                    print(f"{ex_rel_path} already exists")
                    choice = input("overwrite ? (y,n)[n]:")
                    choice = choice.lower()
                    if choice != 'y':
                        skip=True
                        ok=True
                if not skip:
                    status_code =downloadFile(exercise_file.url, exercise_file_output_filename)
                    if status_code != 200:
                        retry_count += 1
                        wait_time += 1
                        
                        if status_code == 401:
                            refresh_course=True

                        if retry_count > max_retry_count:
                            errors(f"Max retry count exceed max : {max_retry_count}")
                            ok=True
                    else:
                        ok=True
                else:
                    print("skiped")

        if is_ex_mode:
            sys.exit()

    sections = ds.m_section.getListCourseId(course.id)
    if not sections:
        errors(f"Course with id: {course_id} has no section", exit_progs=True)
    
    # sys.exit()
    download_transcripts= 'transcript' in what_to_downloads
    download_media = 'media' in what_to_downloads
    download_playlist = 'playlist' in what_to_downloads
    download_dir=getDownloadDir(course.slug)
    
    playlist_buffer = ""
    if download_playlist:
        playlist_buffer = "#EXTM3U\n";
    for section in sections:
        tocs = ds.m_toc.getListBySectionId(section.id)
        if not tocs:
            errors(f"Section with id: {section.id} doesnt have toc records")
            continue

        toc_number=1
        
        
        for toc in tocs:
            if download_playlist:
                media_filename = f"{toc.slug}-{fmt}.mp4"
                media_filename_encoded = urllib.parse.quote(media_filename)
                playlist_buffer += f"#EXTINF:{toc.duration},{media_filename}\n"
                playlist_buffer += media_filename_encoded + "\n"

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
                        if refresh_transcripts:
                            log(f"refershing transcripts")
                            transcripts = api_course.getTranscripts(toc,refresh=True)
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
            
            if download_media: 
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

    if download_playlist:
        # print(playlist_buffer)
        playlist_output_filename = f"{download_dir}/{course.slug}-{fmt}.m3u"
        pl_rel_path = os.path.relpath(playlist_output_filename, os.path.dirname(__file__))

        writeFile(pl_rel_path, playlist_buffer)
        print(f"File saved to : {pl_rel_path}")


    
    
    