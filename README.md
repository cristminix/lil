# lil
lil stand for Linkedin Learning CLI, linkedin learning course assets downloader by using command line interface.

# Requirements
- `python3` currently `python3.11`

# Tested and ready for
- `Mac Osx intel 10.13.6 +`

For another platform you can try to adopting by using python3 use conventions.

# How to use it
## Preparation 
```bash
$ pwd
/Users/bbd33/Desktop
$ git clone https://github.com/cristminix/lil
$ cd lil
$ python3 --version
Python 3.11.4
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirement.txt
$ chmod +x ./bin/lil.py
$ ./bin/lil.py -h
usage: lil.py [-h] {login,fetch,download,media-server,course,cache} ...

lil linkedin learning fetcher cli

options:
  -h, --help            show this help message and exit

Subcommands:
  {login,fetch,download,media-server,course,cache}
    login               Login to linkedin learning to create cookies
    fetch               Fetch course metadata
    download            Download course items
    media-server        Start local media server
    course              List saved course
    cache               Cache
```
## 1. Login to linkedin learning website via cli
First thing first you need to decide which login method you want to use to create a valid cookies for accessing API interface.
```bash
$ ./bin/lil.py login
Last run 1.646 hours ago
Please Select Action:
1: Continue using Individual Account
2: Continue using Library Account
3: Continue Using Browser Cookies
4: Clear Cookies (Logout)
5: Account Settings
0: exit
Enter your choice (1,2,3,4,5,0)[2]:5
```
## 1.1. Configure Account Setting
For the first time you will select the option 5
```bash
Please Select Login type:
1: Individual Account
2: Library Account
3: Import Browser Cookies
0: Back
```
**Description**
1. Individual Account
    - You need to provide `email` and valid `password` 
        ```bash
        Please Select Action:
        1: Change Email
        2: Change Password
        p: Print
        0: Back
        Enter your choice (1,2,0)[0]:
        ```

2. Library Account
    - You need to provide `library id`, `card number` and `pin`
        ```bash
        Please Select Action:
        1: Change Library ID
        2: Change Card Number
        3: Change PIN
        p: Print
        0: Back
        Enter your choice (1,2,3,0)[0]:
        ```
    
3. Import Browser Cookies
    - You need to define the browser name you are currently loged in the linkedin learning website 
        ```bash
        Please Select Action:
        1: Change browser name
        p: Print
        0: Back
        Enter your choice (1,2,3,0)[0]:1

        Please select browser
        1:chrome
        2:firefox
        3:edge
        4:safari
        5:chromium
        6:opera
        7:opera_gx
        8:brave
        9:vivaldi
        10:librewolf
        00: Back
        Enter your choice (1-10):1
        ```



## 1.2. Continue login by using your previosly configured  account setting

After configuring Account Settings you need to continue login using account by selecting option either `1`, `2` or `3` , for example I have choosing option `3`

```bash
Please Select Action:
1: Continue using Individual Account
2: Continue using Library Account
3: Continue Using Browser Cookies
4: Clear Cookies (Logout)
5: Account Settings
0: exit
Enter your choice (1,2,3,4,5,0)[2]:3
[LOG]Human start browsing this url:https://www.linkedin.com/learning
[LOG]Resp Code 200
[LOG]Write file storage/browser_cache/linkedin_learning_homepage-1.html success
[INFO]You are loged in
[LOG]ALREADY LOGED IN
```
On successful login you will see `ALREADY LOGED IN` output text, neither you will got `CANT LOGIN WITH THAT ACCOUNT OPTION` red errors text.

## 2. Fetch the Course Page
For fetching the course page you need a valid course url, by copyng the course url from linkedin learning website

```bash
$ ./bin/lil.py fetch -h
usage: lil.py fetch [-h] url

positional arguments:
  url         Course url

options:
  -h, --help  show this help message and exit

$ ./bin/lil.py fetch https://www.linkedin.com/learning/learning-next-js
...
[LOG]Human start browsing this url:https://www.linkedin.com/learning/learning-next-js/what-to-learn-next
[LOG]wait for 1 seconds
[LOG]retry count : 1
[LOG]Human start browsing this url:https://www.linkedin.com/learning/learning-next-js/what-to-learn-next
[LOG]Resp Code 200
getVideoMetaNd time elapsed:0.084532 seconds

ApiCourse.getStreamLocs time elapsed:3.701450 seconds

Fetch stream locations [360,720,540]
getVideoMetaNd time elapsed:0.087000 seconds

ApiCourse.getTranscripts time elapsed:0.485192 seconds

Fetch transcripts [us,ae,id,cn,tw,cz,dk,nl,fr,de,in,it,jp,kr,my,no,pl,br,ro,es,se,ph,th,tr,ua]
```
After fetching course page complete the course metadata will be stored in local database for further use.


## 3. Displaying Saved Course
After fetching course page complete you can now try to displaying saved course

```bash
$ ./bin/lil.py course

List of saved courses:

  1. DevOps Foundations: Lean and Agile  By Ernest Mueller,Karthik Gaekwad
  2. Rust for JavaScript Developers  By Eve Porcello
  3. Test Automation with Python: 1 Introduction to Automated Testing  By Headspin University
  4. Learning GitHub Pages  By Ray Villalobos
  5. Learning Vim  By Miki Tebeka
  6. Learning Static Site Building with Jekyll  By Nate Barbettini
  7. Python Essential Training  By Ryan Mitchell
  8. Python Essential Libraries  By Joe Marini
  9. Learning Next.js  By Sandy Ludosky
```

### 3.1. Displaying course detail
For displaying course detail you need to specify `-i <course_id>` or `--id <course_id>` , and you can show the duration of the video toc items by adding `-sd` or `--show-duration`

```bash
$ ./bin/lil.py course --id 9 --show-duration
$ ./bin/lil.py course -i 9 -sd


 Learning Next.js
 By Sandy Ludosky

 The Next.js web development framework gives you all the benefits of a server-side rendering tool with the speed and ease of a single-page app. 
...

  Introduction

     1. Speeding up your workflow with Next.js (57 seconds)
...    

  Conclusion

     1. What to learn next? (26 seconds)
```

## 4. Dowloading Course Assets
Course assets contains media course data either video or audio, transcripts or subtitle file WEB VTT , Exercise File, and Playlist M3U file.
```bash
$ ./bin/lil.py download
```
Default options display all saved course with available media formats and transcript languages, with information [i:course_id]

```bash
$ ./bin/lil.py download --id 9
$ ./bin/lil.py download -i 9
```
With suplied course_id options will display course details which includes course sections and toc available media formats and transcript languages, with information  [i:course_id] [si:section_id] [ti:section_id]

### 4.1. Downloading all assets in selected course
Downloading all assets means download all media streams transcripts or subtitles and playlist for all toc in current course sections. To achive this you need to specify required options : `-i <course_id>` or `--id <course_id>`, `-f <media_format>` or `--fmt <media_format>`, `-tl <country_id>` or `--transcript-lang <country_id>` , `-w a` or `-w all` or `--what a` or `--what all` then the last option is `-run` or `--run` to run the cli download manager

To enable numbering on download output filename you can add option `-en` or `--enable-numbering`

```bash
# this commands are all equivalents
$ ./bin/lil.py download -i 9 -f 720 -tl us -w a -run
$ ./bin/lil.py download -i 9 -f 720 -tl us -w all -run
$ ./bin/lil.py download --id 9 --fmt 720 --transcript-lang us --what a --run
$ ./bin/lil.py download --id 9 --fmt 720 --transcript-lang us --what all --run
# enable numbering
$ ./bin/lil.py download -i 9 -f 720 -tl us -w all -en -run
$ ./bin/lil.py download -i 9 -f 720 -tl us -w all --enable-numbering -run

```

### 4.2. Download playlist only
To download course Playlist M3U file, you just need to specify required options : `-i <course_id>` or `--id <course_id>`, `-f <media_format>` or `--fmt <media_format>`, `-w pl` or `-w playlist` or `--what pl` or `--what playlist` then the last option is `-run` or `--run` to run the cli download manager

```bash
# this commands are all equivalents
$ ./bin/lil.py download -i 9 -f 720 -w pl -run
$ ./bin/lil.py download -i 9 -f 720 -w playlist -run
$ ./bin/lil.py download --id 9 --fmt 720 --what pl --run
$ ./bin/lil.py download --id 9 --fmt 720 --what playlist --run
Download manager is running
playlist
Selected fmt: 720
Selected transcript lang: None
[LOG]available fmt:[360,540,720]
[LOG]Checking available fmt
[LOG]fmt : 720 is Ok
Download playlist
[LOG]Write file storage/downloads/learning-next-js/learning-next-js-720.m3u success
File saved to : ../storage/downloads/learning-next-js/learning-next-js-720.m3u
```

### 4.3. Download transcripts or subtitles only
To download course transcript or subtitle WEB VTT file, you just need to specify required options : `-i <course_id>` or `--id <course_id>`, `-f <media_format>` or `--fmt <media_format>`, `-tl <country_id>` or `--transcript-lang <country_id>` ,`-w t` or `-w transcript` or `--what t` or `--what transcript` then the last option is `-run` or `--run` to run the cli download manager

```bash
# this commands are all equivalents
$ ./bin/lil.py download -i 9 -f 720 -tl us -w t -run
$ ./bin/lil.py download -i 9 -f 720 -tl us -w transcript -run
$ ./bin/lil.py download --id 9 --fmt 720 --transcript-lang us --what t --run
$ ./bin/lil.py download --id 9 --fmt 720 --transcript-lang us --what transcript --run
Download manager is running
transcript
Selected fmt: 720
Selected transcript lang: us
[LOG]available fmt:[360,540,720]
[LOG]Checking available fmt
[LOG]fmt : 720 is Ok
Download transcript
[LOG]available transcript lang:[ae,br,cn,cz,de,dk,es,fr,id,in,it,jp,kr,my,nl,no,ph,pl,ro,se,th,tr,tw,ua,us]
[LOG]transcript lang : us is Ok
Downloading:lil/storage/downloads/learning-next-js/speeding-up-your-workflow-with-next-js-720.vtt
```

### 4.4. Download media only
To download course media file, you just need to specify required options : `-i <course_id>` or `--id <course_id>`, `-f <media_format>` or `--fmt <media_format>`,`-w m` or `-w media` or `--what m` or `--what media` then the last option is `-run` or `--run` to run the cli download manager

```bash
# this commands are all equivalents
$ ./bin/lil.py download -i 9 -f 720 -tl us -w m --run
$ ./bin/lil.py download --id 9 --fmt 720 --transcript-lang us --what media --run
Download manager is running
media
Selected fmt: 720
Selected transcript lang: us
[LOG]available fmt:[360,540,720]
[LOG]Checking available fmt
[LOG]fmt : 720 is Ok
Download media
Downloading:lil/storage/downloads/learning-next-js/speeding-up-your-workflow-with-next-js-720.mp4
url:https://www.linkedin.com/dms/prv/vid/C4E0DAQEy1ZQPqq-arw/learning-original-video-vbr-720/0/1660679415193?ea=95231473&ua=153712024&e=1691310545&v=beta&t=PzPCximO_GvzOqmY-iGd7MYvWSbI9oDs-tQHoM-LDn0
```

### 4.4. Download exercise file only
To download exercise file, you just need to specify required options : `-i <course_id>` or `--id <course_id>`, `-w ex` or `-w exercise` or `--what ex` or `--what exercise` then the last option is `-run` or `--run` to run the cli download manager

```bash
# this commands are all equivalents
$ ./bin/lil.py download --id 9 -w ex --run
$ ./bin/lil.py download --id 9 --what exercise --run
Download manager is running
Download exercise_file
Downloading:lil/storage/downloads/learning-next-js/Ex_Files_Learning_Nextjs.zip
url:https://www.linkedin.com/ambry/?x-li-ambry-ep=AQLna5qRecM7PgAAAYnE0F85wx_MKeyggHMSEVF2qzO_qUEYgVP2syEPuYPC_BxHORA56CGQfR29uZ8oJzdE--_PgIKjxMA82zE52idVlGM5huSRqxYmv4ne2izAzRlpdhaXJcUqOG_UUfzqL3FFd0ZkMo_jKJ2Gvpp4vmDSMD5gagFhZK9DuwE0X54_lkjA_F-qHWFgdsRBOJ5W3ggs_Iu031nnkFCzZB_xu_sQK5zzaSa3c1pa191IUjYtKQZ_mF1ikCCEP4wofP5H8YxrO1mGBcpRao_uq4SN4f7XxUewHhkNtZL3yJDDrddmhX1YX3UKMfen-arC_OFwg2dkvPOnZnWp9J1wp3gnWJWhKI5InEfOq3-3vpROCUzNtbhNqzlpJk5v9O79LARsst3sS1AZNsUsGMq5VlFz79Vym1CQBTy7huwEFt-ZjpnH0waaKm94NP8ak9nYpUMR1gRYtCtmMq5KvT3kFf0FghCjYz5kdwTwJhPLaZv9picDho-RMpj7YHZF2GWQzPy6NOfTCJw8zeNEimABisJnWZM_XPqdu6cGeVHHlwZrvy40nWvXbaFWpwFpLXtcm5RNKBEF
downloading 7.20 MB
....
```

## 5. Downloading assets only on all item in selected course section 
To download media and transcripts required options : `-si <section_id>` or `--section-id <section_id>`,  `-f <media_format>` or `--fmt <media_format>` , `-tl <country_id>` or `--transcript-lang <country_id>` then the last option is `-run` or `--run` to run the cli download manager


### 5.1. Download all media and transcript in all item in selected course section 
To download media and transcripts only on all item in selected course section just specify full option as above
```bash
# this commands are all equivalents
$ ./bin/lil.py download --section-id 63 --fmt 360 --transcript-lang id -run
$ ./bin/lil.py download -si 63 -f 360 -tl id -run

```

### 5.2. Download all media only in all item in selected course section 
Just remove `-tl` or `--transcript-lang` options
```bash
# this commands are all equivalents
$ ./bin/lil.py download --section-id 63 --fmt 360 -run
$ ./bin/lil.py download -si 63 -f 360  -run

```

### 5.2. Download all transcript only in all item in selected course section 
Just add `-to` or `--transcript-only` options

```bash
# this commands are all equivalents
$ ./bin/lil.py download --section-id 63 --fmt 360 --transcript-lang id --transcript-only -run
$ ./bin/lil.py download -si 63 -f 360 -to -run

```

## 6. Download media and transctipt only on selected course toc
To download media and transcripts required options : `-ti <toc_id>` or `--toc-id <toc_id>`,  `-f <media_format>` or `--fmt <media_format>` , `-tl <country_id>` or `--transcript-lang <country_id>` then the last option is `-run` or `--run` to run the cli download manager
```bash
# media and transcript
$ ./bin/lil.py download --toc-id 343 --fmt 360 --transcript-lang id -run
$ ./bin/lil.py download -ti 343 -f 360 -tl id -run

# transcript only
$ ./bin/lil.py download --toc-id 343 --fmt 360 --transcript-lang id --transcript-only -run
$ ./bin/lil.py download -ti 343 -f 360 -tl id -to -run
```

## 6.1 Stream current media on selected course toc via pipe with ffplay

You can play media on selected course toc via pipe by adding `-stp` or `--stream-to-pipe`. Remember you have already installed ffplay and add it on your system PATH

```bash
$ ./bin/lil.py download --toc-id 23 --fmt 640 
$ --stream-to-pipe -run|ffplay -i pipe:
./bin/lil.py download -ti 23 -f 640 -stp -run|ffplay -i pipe:

```

# 7. Troubleshooting

Sometimes you will got download errors `401` , and this indicate the current download url has expired, so you need to refresh all the download links by using this command `./bin/lil.py download -i <course_id> -rsl` or `./bin/lil.py download --id <course_id> --refresh-stream-location`

```bash
$ ./bin/liy.py download -i 1 -rsl
$ ./bin/lil.py download --id 1 --refresh-stream-location
```

# LICENSE
MIT LICENSE