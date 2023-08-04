from robots import Login
from robots.fn import log,lang,errors
from robots.config import linkedin_url, linkedin_learning_url
import sys

class LoginIndividual(Login):
    def start(self):    
        account_setting=self.account_setting
        continue_next_step=False

        log(lang('using_account',"individual"))
        login_url=self.getLoginUrl()
        page_name='login_email_page'
        content=self.human.browse(login_url,page_name)
        if self.human.guessPage(page_name,content):
            current_page=self.human.getPage(page_name)
            formNd=current_page.getFormNd()
            if formNd:
                form_action="%s%s" % (linkedin_url,formNd.attr('action'))
                current_form = current_page.getForm()
                if current_form:
                    current_form.setAction(form_action)
                    current_form.setPayload(current_page.getDoc())
                    current_form.setData('email', account_setting["email"])
                    current_form.browser.setReferer('https://www.google.com/')
                    content = current_form.post()
                    # log(content)
                    if current_form.postValidationCheckPoint():
                        errors(lang("cant_continue_server_send_checkpoint"),exit_progs=True)
                    elif not current_form.postValidationSuccess():
                        errors(lang("cant_continue_with_provided_email",account_setting["email"]),exit_progs=True)
                    else:
                        continue_next_step=True
                else:
                    errors(lang('page_name_doesnt_have_form_object', page_name),exit_progs=True)
            
        else:
            errors(lang('cant_login_email_page'),exit_progs=True)
        
        # exit if cant continue next step
        if not continue_next_step:
            errors(lang('cant_continue_next_step_because_prev_errors'),exit_progs=True)
        
        page_name='login_passwd_page'
        
        if self.human.guessPage(page_name, content):
            current_page=self.human.getPage(page_name)
            formNd=current_page.getFormNd()
            if formNd:
                form_action="%s%s" % (linkedin_url,formNd.attr('action'))
                current_form = current_page.getForm()
                if current_form:
                    current_form.setAction(form_action)
                    current_form.setPayload(current_page.getDoc())
                    current_form.setData('session_password', account_setting["password"])
                    current_form.browser.setReferer('https://www.google.com/')
                    content = current_form.post()
                    # log(content)
                    
                    if current_form.postValidationNotSuccess():
                        errors(lang("cant_continue_with_provided_passwd",account_setting["password"]),exit_progs=True)
                    
                    else:
                        continue_next_step=True
                else:
                    errors(lang('page_name_doesnt_have_form_object', page_name),exit_progs=True)
        # exit if cant continue next step
        # sys.exit()
        if not continue_next_step:
            errors(lang('cant_continue_next_step_because_prev_errors'),exit_progs=True)
        # sys.exit()
        if current_form.postValidationCheckPoint():
            page_name='login_pin_page'
        
            if self.human.guessPage(page_name, content):
                log(lang("login_requested_challenge"))
                log(lang("please_open_device_to_get_pin_code"))
                # login_request_challenge = True
                verification_code = input(lang("enter_pin_code"))
                current_page=self.human.getPage(page_name)
                formNd=current_page.getFormNd()
                if formNd:
                    form_action="%s%s" % (linkedin_url,formNd.attr('action'))
                    current_form = current_page.getForm()
                    if current_form:
                        current_form.setAction(form_action)
                        current_form.setPayload(current_page.getDoc())
                        current_form.setData('pin', verification_code)
                        current_form.browser.setReferer('https://www.google.com/')
                        content = current_form.post()
                        # log(content)
                        
                        if current_form.postValidationPattern(r"check/add-phone"):
                            log(lang("login_requested_add_phone"))
                            log(lang("please_fix_this_problem_by_with_your_browser"))
                            log(lang("cant_continue_util_profile_setup_complete"))
                        
                    else:
                        errors(lang('page_name_doesnt_have_form_object', page_name),exit_progs=True)
            #errors(lang("cant_continue_server_send_checkpoint"),exit_progs=True)
        if current_form.postValidationSuccess():
            self.already_loged_in=True
        
        return False

            

        
def login(human, json_config):
    li = LoginIndividual(human, json_config)
    li.start()
    return li.alreadyLogedIn()   
