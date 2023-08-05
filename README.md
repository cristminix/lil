# lil
lil stand for Linkedin Learning CLI, linkedin learning course assets downloader by using command line interface.

# Requirements
- `python3` currently `python3.11`

# Tested and ready for
- `Mac Osx intel 10.13.6 +`

For another platform you can try to adopting by using python3 use conventions.

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
## 1. Login to linkedin learning website via cli
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
## 1.1 Configure Account Setting
For the first time you will select the option 5
```
Please Select Login type:
1: Individual Account
2: Library Account
3: Import Browser Cookies
0: Back
```
**Description**
1. Individual Account
    - You need to provide `email` and valid `password` 
        ```
        Please Select Action:
        1: Change Email
        2: Change Password
        p: Print
        0: Back
        Enter your choice (1,2,0)[0]:
        ```

2. Library Account
    - You need to provide `library id`, `card number` and `pin`
        ```
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
        ```
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



## 1.2 Continue login by using your previosly configured  account setting

After configuring Account Settings you need to continue login using account by selecting option either `1`, `2` or `3` , for example I have choosing option `3`

```
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