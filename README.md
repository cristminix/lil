# lil
lil stand for Linkedin Learning CLI, linkedin learning course assets downloader by using command line interface.

# Requirements
- `python3` currently `python3.11`

# Tested and ready for
- `Mac Osx intel 10.13.6 +`

# How to use it
## Preparation 
```
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
## Login to linkedin learning website via cli
First thing first you need to decide which login method you want to use to create a valid cookies for accessing API interface.
```
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
For the first time you will select the option 5
```
Please Select Login type:
1: Individual Account
2: Library Account
3: Import Browser Cookies
0: Back
```

