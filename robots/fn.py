from pathlib import Path
from robots import config
from robots import langs
import re
import json
import requests
from pyquery import PyQuery as pquery
import sys
from datetime import datetime, timedelta
import time
import math
import html
from urllib.parse import unquote, urlunparse
from urllib.parse import urlparse, parse_qs
import unicodedata
import os
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[0m'
last_line_len=0
def formatBytes(bytes_num):
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    i = 0

    while bytes_num >= 1024 and i < len(sizes) - 1:
        bytes_num /= 1024.0
        i += 1

    return f"{bytes_num:.2f} {sizes[i]}"
def print_single_line(text):
    sys.stdout.write('\033[2K\033[1G')
    print(text, end='\r', flush=True)
def print_single_lineX(text, clear_previous=True):
    global last_line_len
    if clear_previous:
        print('\r' + ' ' * last_line_len, end='')
    last_line_len=len(text)    
    print('\r' + text, end='')

BENCHMARK_DATA = {}
def benchmark(label,command):
    global BENCHMARK_DATA
    if not label in BENCHMARK_DATA:
        BENCHMARK_DATA[label] = {}
    if command == 'start':
        BENCHMARK_DATA[label]["start_time"] = time.time()
        return BENCHMARK_DATA[label]
    elif command == 'end':
        BENCHMARK_DATA[label]["end_time"] = time.time()
        execution_time = BENCHMARK_DATA[label]["end_time"] - BENCHMARK_DATA[label]["start_time"]
        BENCHMARK_DATA[label]["execution_time"] = execution_time
        BENCHMARK_DATA[label]["elapsed_time"] = f"{execution_time:.6f} seconds"

        return BENCHMARK_DATA[label]
         
    
def deleteFile(file_path):
    rel_path = os.path.relpath(file_path, os.getcwd())

    try:
        os.remove(file_path)
        log(f"File '{rel_path}' has been deleted successfully.", verbose=True)
    except FileNotFoundError:
        errors(f"File '{rel_path}' not found.")
    except Exception as e:
        errors(f"An error occurred: {e}")

def slugify(text):
    # Normalize the text to remove diacritics and special characters
    normalized_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Convert the text to lowercase and replace spaces with dashes
    slug = re.sub(r'\s+', '-', normalized_text.lower())
    # Remove any remaining non-alphanumeric characters except for dashes
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove leading and trailing dashes
    slug = slug.strip('-')
    return slug

def timeAgo(seconds):
    current_time = datetime.now()
    time_ago = current_time - timedelta(seconds=seconds)

    if seconds < 60:
        return f"{seconds} %s" % (lang('seconds'))
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} %s" % (lang('minutes'))
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} %s" % (lang('hours'))
    else:
        days = seconds // 86400
        return f"{days} %s" % (lang('days'))
def cleanQueryString(url):
    parsed_url = urlparse(url)
    cleaned_url = urlunparse(parsed_url._replace(query=''))
    return cleaned_url

#get query string value from url
def getQueryStringValue(param_name,url):
    parsed_url = urlparse(url)
    query_string = parsed_url.query
    query_params = parse_qs(query_string)
    return query_params.get(param_name, [''])[0]

def getCookiePath(cookie_name, cookie_jar):
    for cookie in cookie_jar:
        if cookie.name == cookie_name:
            return cookie.path

    return None
def log(str, t="log",verbose=False):
    

    log_type = t.lower()
    print_log=False
    log_color=CYAN
    if config.enable_loging:
        if log_type == "err":
            print_log = config.log_errors
            log_color=RED
        elif log_type == "info":
            print_log = config.log_info
            log_color=GREEN

        elif log_type == "nd":
            print_log = config.log_nd
            log_color=YELLOW

        else:
            print_log = True
        
        if verbose:
            print_log = print_log and config.log_verbose


    if print_log: 
        
        log_message= "[%s]%s" % (t.upper(),str)
        # if log_type == "err":
        print(log_color + "[%s]%s" % (t.upper(),str) + RESET)
        # else:
        #     print_single_line(log_color + "[%s]%s" % (t.upper(),str) + RESET)

def errors(msg, exception=None, exit_progs=False,verbose=False):
    if exception:
        log(exception,'ERR',verbose=True)

    log(msg,'ERR',verbose=verbose)
    if exit_progs:
        sys.exit()

def validEmail(email):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Use the re.match function to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False

def inputAccountSettingIndividual(json_config):
    if not json_config.get("email"):
        json_config.set("email","you@gmail.com")
    if not json_config.get("password"):
        json_config.set("password","*******")
    
    print(lang("please_select_action"))

    print("1: %s" % (lang('change_email')))
    print("2: %s" % (lang('change_password')))
    print("p: %s" % (lang('prnt')))
    print("0: %s" % (lang('back')))

    user_choice = input("%s (1,2,0)[0]:" % (lang('enter_your_choice')))
    choice = user_choice.lower()

    if choice == 'p':
        print("%s : %s" % (lang('email'),json_config.get("email")))
        print("%s : %s" % (lang('password'),json_config.get("password")))
        inputAccountSettingIndividual(json_config)
    
    if choice == '1':
        email = input("%s:" % (lang('enter_email')))
        if validEmail(email):
            json_config.set("email",email)
        else:
            errors(lang('is_not_valid_email',email))
        
        inputAccountSettingIndividual(json_config)

    if choice == '2':
        password = input("%s:" % (lang('enter_password_min_4_chars')))
        if len(password)>=4:
            json_config.set("password",password)
        else:
            errors(lang('is_not_valid_password',password))
        
        inputAccountSettingIndividual(json_config)

def inputAccountSettingBrowserCookie(json_config):
    if not json_config.get("browser_cookie_browser"):
        json_config.set("browser_cookie_browser","chrome")
    print(lang("please_select_action"))

    print("1: %s" % (lang('change_browser_name')))
    print("p: %s" % (lang('prnt')))
    print("0: %s" % (lang('back')))

    user_choice = input("%s (1,2,3,0)[0]:" % (lang('enter_your_choice')))
    choice= user_choice.lower()
    if choice == 'p':
        print("%s : %s" % (lang('browser_name'),json_config.get("browser_cookie_browser")))
        inputAccountSettingBrowserCookie(json_config)
    elif choice=='1':
        ok=False
        while not ok:
            print(lang("please_select_browser"))
            browser_list=['chrome','firefox','edge','safari','chromium','opera','opera_gx','brave','vivaldi','librewolf']
            browser_index=1
            for browser_name in browser_list:
                print(f"{browser_index}:{browser_name}")
                browser_index += 1
            print("00: %s" % (lang('back')))
            user_choice = input("%s (1-10):" % (lang('enter_your_choice')))
            user_choice = user_choice.lower()
            if user_choice == '00':
                ok=True
            else:
                b_choice= 0
                try:
                    b_choice=int(user_choice)
                except:
                    pass
                
                if not b_choice:
                    b_choice=0
                
                if b_choice <1 or b_choice >10:
                    errors(f"you not choosing 0-10")
                else:
                    b_index = b_choice-1
                    try:
                        browser_name=browser_list[b_index]
                        print(browser_name)
                        json_config.set("browser_cookie_browser",browser_name)

                        ok=True
                    except:
                        pass
        
        inputAccountSettingBrowserCookie(json_config)

        


def inputAccountSettingLibrary(json_config):
    if not json_config.get("library_id"):
        json_config.set("library_id","***")
    if not json_config.get("card_number"):
        json_config.set("card_number","*****")
    if not json_config.get("pin"):
        json_config.set("pin","*****")
    
    print(lang("please_select_action"))

    print("1: %s" % (lang('change_library_id')))
    print("2: %s" % (lang('change_card_number')))
    print("3: %s" % (lang('change_pin')))
    print("p: %s" % (lang('prnt')))

    print("0: %s" % (lang('back')))

    user_choice = input("%s (1,2,3,0)[0]:" % (lang('enter_your_choice')))
    choice= user_choice.lower()
    if choice == 'p':
        print("%s : %s" % (lang('library_d'),json_config.get("library_id")))
        print("%s : %s" % (lang('card_number'),json_config.get("card_number")))
        print("%s : %s" % (lang('pin'),json_config.get("pin")))
        inputAccountSettingLibrary(json_config)
    
    
    if choice == '1':
        library_id = input("%s:" % (lang('enter_library_id_min_2_chars')))
        if len(library_id) >=2 :
            json_config.set("library_id",library_id)
        else:
            errors(lang('is_not_valid_library_id',library_id))
        
        inputAccountSettingLibrary(json_config)

    if choice == '2':
        card_number = input("%s:" %(lang('enter_card_number_min_4_chars')))
        if len(card_number)>=4:
            json_config.set("card_number",card_number)
        else:
            errors(lang('is_not_valid_card_number',card_number))
        
        inputAccountSettingLibrary(json_config)
    
    if choice == '3':
        pin = input("%s:" % lang('enter_pin_min_4_chars'))
        if len(pin)>=4:
            json_config.set("pin",pin)
        else:
            errors(lang('is_not_valid_pin',pin))
        
        inputAccountSettingLibrary(json_config)
        


def inputAccountSetting(json_config):
    print("%s:" % (lang('please_select_login_type')))

    print("1: %s" % lang('individual_account'))
    print("2: %s" % lang('library_account'))
    print("3: %s" % lang('import_browser_cookies'))
    print("0: %s" % lang('back') )
    user_choice = input("%s (1,2,0)[0]:" % (lang('enter_your_choice')))
    choice = user_choice.lower()
    # Process the user's choice
    if choice == '1':
        inputAccountSettingIndividual(json_config)
    
    elif choice == '2':
        inputAccountSettingLibrary(json_config)
    
    elif choice == '3':
        inputAccountSettingBrowserCookie(json_config)
    
    elif choice == '0':
        pass
    else:
        inputAccountSetting(json_config)



def inputAction(default_login_type,human,json_config):
    print(lang("please_select_action"))

    print("1: %s" % lang('continue_using_individual_account'))
    print("2: %s" % lang('continue_using_library_account'))
    print("3: %s" % lang('continue_using_browser_cookies'))
    print("4: %s" % lang('clear_cookies_logout'))
    print("5: %s" % lang('account_settings'))
    print("0: %s" % lang('exit'))

    login_type = default_login_type
    default_code=2
    
    user_choice = input("%s (1,2,3,4,5,0)[%i]:" % (lang('enter_your_chioce'),default_code))
    choice = user_choice.lower()
    # Process the user's choice
    if choice == '1':
        login_type="individual"
    
    elif choice == '2':
        login_type="library"

    elif choice == '3':
        login_type="browser_cookie"

    elif choice == '4':
        human.clearCookies()
        login_type=inputAction(login_type,human,json_config)

    elif choice== '5':
        inputAccountSetting(json_config)
        login_type=inputAction(login_type,human,json_config)

    elif choice== '0':
        sys.exit()

    else:
        login_type=choice

    return login_type

def parseFormPayload(doc, form_selector):
    inputs = doc.find("%s input" % (form_selector))
    # print(inputs)
    payload={}
    for input in inputs:
        # print(input.value)
        payload[input.name]=input.value
    return payload 

def lang(key, data=None):
    global langs
    global config

    config_lang  = getattr(config,"lang")
    selected_langs = getattr(langs,config_lang)
    if hasattr(selected_langs, key):
        str = getattr(selected_langs, key)
        if not data:
            return str
        else:
            return str % (data)
    return key
def writeFile(path,content,mode="w"):
    rel_path = os.path.relpath(path, os.getcwd())
    try:
        with open(path, mode) as file:
            file.write(content)
            
            
            log(lang("write_file_success",rel_path),verbose=True)

        return True
    except Exception as exception:
        errors(lang("could_not_write_file",rel_path),exception,verbose=True)
        return False    

def writeResp(resp, page_name, index,browser_cache_dir=None):
    global config
    if config.write_resp_text:
        path = "%s-%s.html" % (page_name, index)
        if not browser_cache_dir:
            browser_cache_dir = "html_cache"
        path = "%s/%s" % (browser_cache_dir,path )
        writeFile(path,resp.text.replace('</head>','<title>%s</title></head>' % (resp.url)))

def matchUrl(pattern, url):
    matches = re.findall(pattern, url)
    return len(matches) > 0

def saveCookies(session, path="cookies.json"):
    try:
        cookies = requests.utils.dict_from_cookiejar(session.cookies)  # turn cookiejar into dict
        Path(path).write_text(json.dumps(cookies))  
        return True  
    except Exception as exception:
        errors(lang("could_not_write_cookie_file", path),exception)
        return False
def clearCookies(path="cookies.json"):
    try:
        cookies = {}
        Path(path).write_text(json.dumps(cookies))  
        return True  
    except Exception as exception:
        errors(lang("could_not_clear_cookie_file", path),exception)
        return False
    
def loadCookies(session, path="cookies.json"):
    try:
        cookies = json.loads(Path(path).read_text())  # save them to file as JSON
        cookies = requests.utils.cookiejar_from_dict(cookies)  # turn dict to cookiejar
        session.cookies.update(cookies)  # load cookiejar to current session
        return True
    except Exception as exception:
       errors(lang("could_not_load_cookie_file", path),exception) 
       return False
    
def dummyFn(a=None):
    log(lang('pquery_dummy_fn_called'))
    return None
def pq(html):
    pq_obj=None
    # log(html)
    if html == None:
        log(lang('pquery_called_with_empty_html'))
    else:
        try:
            pq_obj=pquery(html)
        except Exception as exception:
            errors(lang("pquery_error", path),exception) 
            pq_obj = dummyFn
    return pq_obj

def waitForCaptcha(json_config, last_run_timeout_max=7):
    current_dt=datetime.now()
    if not json_config.get('last_run_timestamp'):
        json_config.set('last_run_timestamp', current_dt.timestamp())

    last_run_dt = datetime.fromtimestamp(json_config.get('last_run_timestamp'))
    last_run_rest = current_dt - last_run_dt
    last_run_timeout = math.ceil(last_run_rest.total_seconds())
    
    need_to_wait = last_run_timeout < last_run_timeout_max
    sleep_timeout = last_run_timeout_max - last_run_timeout

    if sleep_timeout < 0:
        sleep_timeout = 0
    
    need_to_wait_message= ""

    if need_to_wait:
        need_to_wait_message= "need to wait for %s second" % (sleep_timeout)

    print("Last run %s ago %s" %(timeAgo(last_run_timeout), need_to_wait_message))
    
    if need_to_wait:
        print("waiting for %s second " % (sleep_timeout))
        time.sleep(sleep_timeout)

    current_dt=datetime.now()
    json_config.set('last_run_timestamp',current_dt.timestamp())


# convert data to desired format
def convertData(src, c_type):
    if c_type == "unquote":
        return unquote(src)
    elif c_type == "unescape":
        return html.unescape(src)
    elif c_type == "dict" or c_type == "json.loads":
        return json.loads(src)
    return src
# get html meta data
def getMeta(name,doc,meta_config={}):
    selector="meta[name='%s']" % (name)
    metaNd=doc(selector)
    # print(metaNd)
    if len(metaNd) > 0:
        content = metaNd.attr("content")
        if name in meta_config:
            parser_type = meta_config[name]
            match_pipe=re.findall(r"\|",parser_type)
            if len(match_pipe)>0:
                parser_list = parser_type.split("|")
                for c_type in parser_list:
                    content = convertData(content, c_type)
            else:
                content=convertData(content, parser_type)
        return content    
    return None

def dict2htmTable(data_dict, root_path=""):
    style="style='border-collapse: collapse;border:solid 1px #ddd;font-family:JetBrains Mono, Consolas, monospace;padding:0 1em'"
    table_html = "<table %s>\n" % (style)
    table_html += "<tr><th %s align='right'>Key</th><th %s align='left'>Value</th></tr>\n" % (style,style)
    v=""
    full_path=""
    try:
        for key, value in data_dict.items():
            if root_path == "":
                full_path = key
            else:
                full_path = "%s.%s" % (root_path, key)
            if type(value) is dict:
                v= dict2htmTable(value, full_path)
            elif type(value) is list:
                v=""
                i=0
                for item in value:
                    full_path_i="%s[%i]" % (full_path,i)
                    v += dict2htmTable(item, full_path_i)
                    i += 1
            else:
                v=value
            table_html += f"<tr><td valign='top' align='right' %s><span style='color:brown'>{key}<br/>{full_path}</span></td><td %s>{v}</td></tr>\n" % (style,style)
    except Exception as e:
        errors('',e)
        return data_dict
    table_html += "</table>"
    return table_html