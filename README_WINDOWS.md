# How to use it On Windows

## Preparation On Windows Machine

- install python 3.10+
	
	Since this created python version release is 3.11 then Go to https://www.python.org/downloads/release/python-3110/ and pickup download with your current match Windows Operating System and architecture

- install git-scm 
	For download you can go to this url https://git-scm.com/downloads
- install zsh [optional]

- install oh-my-zsh [optional]

- install windows terminal[optional]

- Configure Windows terminal to using bash [optional]

- Configure Windows terminal to using zsh [optional]

# Run shell git-bash

```bash
$ which python
/c/Python311/python
$ ln -ns /c/Python311/python /c/Python311/python3
$ pwd
/x/
$ git clone https://github.com/cristminix/lil
$ cd lil
$ python3 --version
Python 3.11.4
$ python3 -m venv .venv

# repair symlink on windows
$ cd .venv/Scripts
$ ln -ns python python3
$ cd -
$ cd .venv
$ ln -ns Scripts bin
$ cd -
$ source .venv/bin/activate
$ pip3 install -r requirement.txt
$ chmod +x ./bin/lil.py
$ ./bin/lil.py -h