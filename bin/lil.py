#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.realpath('%s/..' % os.path.dirname(__file__)))
from login import login
from course import course
from fetch import fetch
from download import download
from cache import cache
import argparse



def main():
    parser = argparse.ArgumentParser(description="lil linkedin learning fetcher cli")
    subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")

    # Build subcommand
    login_parser = subparsers.add_parser("login", help="Login to linkedin learning to create cookies")

    # Watch subcommand
    fetch_parser = subparsers.add_parser("fetch", help="Fetch course metadata")
    fetch_parser.add_argument("url", help="Course url")

     # Watch subcommand
    download_parser = subparsers.add_parser("download", help="Download course items")
    download_parser.add_argument("-i","--id", help="Course id")
    download_parser.add_argument("-w","--what", help="What to download [m:media,t:transcript,ex:exercise_file,pl:playlist,a:all]")

    download_parser.add_argument("-si","--section-id", help="Section id , download only in section id")
    download_parser.add_argument("-ti","--toc-id", help="Toc id , download only toc id")
    download_parser.add_argument("-tl","--transcript-lang", help="Transcript lang , specify transcript lang")
    download_parser.add_argument("-f","--fmt", help="Media output size/format , specify output video size/media format")
    download_parser.add_argument("-pl","--play-list",action='store_true', help="Download playlist")
    download_parser.add_argument("-to","--transcript-only",action='store_true', help="Only download transcript")
    download_parser.add_argument("-rsl","--refresh-stream-location",action='store_true', help="Refresh stream location")
    download_parser.add_argument("-stp","--stream-to-pipe",action='store_true', help="Stream the video output to pipe")
    download_parser.add_argument("-run","--run", action='store_true',help="Run download manager")

    
    media_server_parser = subparsers.add_parser("media-server", help="Start local media server")
    media_server_parser.add_argument("-p","--port", help="Specify port")
    
    course_parser = subparsers.add_parser("course", help="List saved course")
    course_parser.add_argument("-i","--id", help="Course id")

    cache_parser = subparsers.add_parser("cache", help="Cache")
    cache_parser.add_argument("-c","--clear", action='store_true', help="Clear cache")

    # account_parser = subparsers.add_parser("account", help="Check for a valid tickets")
    # Serve subcommand
    args = parser.parse_args()

    if args.subcommand == "login":
        login()
    elif args.subcommand == "fetch":
        fetch(args)
    elif args.subcommand == "course":
        course(args)
    elif args.subcommand == "download":
        download(args)
    elif args.subcommand == "cache":
        cache(args)
    else:
        print("Error: Invalid subcommand. Use --help for usage.")

if __name__ == "__main__":
    main()
