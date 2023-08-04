#!/usr/bin/env python3

from robots import Human
from robots.pages import unauthenticated_page,authenticated_page,login_email_page, login_passwd_page, login_pin_page, login_library_page, login_library_card_page
from robots.fn import errors,log, lang, waitForCaptcha, inputAction
from robots.config import linkedin_learning_url
from robots.datasource import DataSource
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir
import login_individual
import login_library
import login_browser_cookie
import sys

# print(cookie_path)
# sys.exit()

def login():
    waitForCaptcha(cli_config)
    #######################################################
    # Database settings
    ######################################################
    ds = DataSource(db_path)
    db_config = ds.m_config
    # sys.exit()
    ######################################################
    # MIMIC HUMAN
    ######################################################
    human = Human(cookie_path,browser_cache_dir)
    human.addPage(login_library_page).addPage(login_library_card_page).addPage(authenticated_page)
    human.addPage(unauthenticated_page).addPage(login_email_page).addPage(login_passwd_page).addPage(login_pin_page)
    ######################################################
    already_loged_in=False
    # login_type="individual"
    # login_type="library"
    login_type = inputAction("library", human, db_config)
    ######################################################
    # STEP 1 BROWSE THE LINKEDIN LEARNING WEBSITE
    ######################################################
    # human try to browse linkedin learning website
    content = human.browse(linkedin_learning_url, 'linkedin_learning_homepage')

    # human try to guess page by name
    if human.guessPage('unauthenticated_page',content):
        log(lang("you_are_not_login"),'info')

        if login_type == "individual":
            already_loged_in = login_individual.login(human, db_config)
        elif login_type == "library":
            already_loged_in = login_library.login(human, db_config)
        elif login_type == "browser_cookie":
            already_loged_in = login_browser_cookie.login(human, db_config)
        else:
            errors(f"Invalid login type", exit_progs=True)

    elif human.guessPage('authenticated_page',content):
        log(lang("you_are_loged_in"),'info')
        already_loged_in=True

    # entry point after login process
    if already_loged_in:
        log(lang('already_loged_in'))
    else:
        errors("CANT LOGIN WITH THAT ACCOUNT OPTION")
        human.clearCookies()
        # continue_next_step=True


