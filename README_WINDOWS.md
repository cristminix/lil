# How to use it
## Preparation 

- install python 3.10+

- install git-scm

- install windows termininal

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
$ ln -ns .venv/Scripts/python .venv/Scripts/python3
$ source .venv/Scripts/activate
$ pip3 install -r requirement.txt
$ chmod +x ./bin/lil.py
$ ./bin/lil.py -h