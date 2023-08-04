from robots import Login
from robots.fn import log,lang,errors,getQueryStringValue,matchUrl
from robots.config import linkedin_url, linkedin_learning_url
import sys
import json

class LoginLibrary(Login):
    def getLoginUrl(self):
        login_url = super().getLoginUrl()
        page_name='login_email_page'
        content=self.human.browse(login_url,page_name)
        if self.human.guessPage(page_name,content):
            current_page=self.human.getPage(page_name)
            # print(current_page.content)
            library_anchor_link=current_page.findNode("a.signin__library")
            # print(library_anchor_link)
            if len(library_anchor_link) > 0:
                library_login_url=library_anchor_link.attr("href")
                return library_login_url
            
            else:
                errors(lang('cant_get_library_anchor_link'),exit_progs=True)
        else:
            # self.human.clearCookies()
            errors(lang('cant_get_login_page'),exit_progs=True)

    def loginLibrary(self, library_login_url):        
        log(lang("login_url",library_login_url),verbose=True)
        page_name='login_library_page'
        content=self.human.browse(library_login_url,page_name)
        if self.human.guessPage(page_name,content):
            current_page=self.human.getPage(page_name)
            formNd=current_page.getFormNd()
            if formNd:
                # csrfToken: ajax:4191024661340244368
                # tenantId: trl
                # authUUID: Nd15X47vTfiX2RGOnjbYZg==
                # redirect: /learning/?upsellOrderOrigin=default_guest_learning

                form_action_validate="%s/learning-login/go/get-validate-url"%(linkedin_url)
                current_form = current_page.getForm()
                if current_form:
                    authUUID=getQueryStringValue('authUUID',library_login_url)
                    current_form.setAction(form_action_validate)
                    current_form.setPayload(current_page.getDoc())
                    current_form.setData('tenantId', self.account_setting["library_id"])
                    current_form.setData('authUUID', authUUID)
                    current_form.setData('redirect', '/learning/?upsellOrderOrigin=default_guest_learning')
                    # print(current_form.data)
                    current_form.browser.setReferer('https://www.google.com/')
                    content = current_form.post()

                    library_card_login_url=None
                    try:
                        content_json = json.loads(content) 
                        library_card_login_url = content_json["url"]
                    except Exception as e:
                        errors(lang("could_not_get_enterprise_login_url"),e,exit_progs=True)

                    if matchUrl(r"learning-login/go/no-access",library_card_login_url):
                        errors(lang('you_have_no_access_on_this_library_id',self.account_setting["library_id"]))
                        errors(lang('make_sure_you_have_valid_library_account_setting'))

                    elif library_card_login_url:
                        content = self.human.browse(library_card_login_url,'library_card_login_url')
                        page_name="login_library_card_page"
                        if self.human.guessPage(page_name,content):
                            current_page=self.human.getPage(page_name)
                            # print(current_page.content)

                            current_form=current_page.getForm()
                            formNd = current_page.getFormNd()

                            
                            if formNd:
                                form_action="%s/%s" % (linkedin_url,"learning-login/go/library-callback")
                                current_form.setAction(form_action)
                                current_form.setPayload(current_page.getDoc())
                                current_form.setData('libraryCardId',self.account_setting["card_number"])
                                current_form.setData('pin',self.account_setting["pin"])
                                # print(form_action)
                                content=current_form.post()
                                library_card_login_url=None
                                try:
                                    content_json = json.loads(content) 
                                    # library_card_login_url = content_json["url"]
                                except Exception as e:
                                    errors(lang("could_not_get_enterprise_card_login_url"),e,exit_progs=True)
                                #errorRedirectUrl
                                #redirectUrl
                                #pin
                                #account
                                #https://www.linkedin.com/checkpoint/enterprise/library/95231473/LEARNING/111224417
                                library_card_login_url="%s/checkpoint/enterprise/library/%s/LEARNING/%s" % (linkedin_url,content_json["account"],content_json["appInstance"])
                                current_form.setAction(library_card_login_url)
                                current_form.setData({
                                    "redirectUrl":content_json["redirectUrl"],
                                    "pin":content_json["pin"],
                                    "libraryCardId" : content_json["libraryCardId"]
                                })
                                content=current_form.post()
                                redirect_url=None
                                try:
                                    content_json = json.loads(content) 
                                    # library_card_login_url = content_json["url"]
                                except Exception as e:
                                    errors(lang("could_not_get_enterprise_card_login_result"),e,exit_progs=True)
                                result_key="result"
                                if result_key in content_json:
                                    results=content_json[result_key]
                                    result_key="com.linkedin.checkpoint.authentication.EnterpriseAuthenticationStatusResult"
                                    if result_key in results:
                                        redirectUri=results[result_key]["redirectUri"]  
                                        status=results[result_key]["status"]
                                        if status == "PASS":
                                            log(lang("enterprise_card_login_passed"),'info')
                                            self.already_loged_in=True

                                        else:
                                            log(lang("enterprise_card_login_not_passed"))                              

                                        content=self.human.browse(redirectUri, 'enterprise_card_login_redirect_uri')
                                        # print(content)
                                    else:
                                        errors(lang('could_not_get_enterprise_login_result_key',result_key))
                                    
                                else:
                                    errors(lang('could_not_get_enterprise_login_result_key', result_key))
                else:
                    errors(lang('page_name_doesnt_have_form_object', page_name),exit_progs=True)
            
        else:
            errors(lang('cant_login_email_page'),exit_progs=True)

    def loginLibraryCard(self, library_card_login_url):
        pass
    def start(self):
        log(lang('using_account',"library"))

        
        
        continue_next_step=False
        library_login_url=self.getLoginUrl()
        self.loginLibrary(library_login_url)


def login(human, json_config):
    li = LoginLibrary(human, json_config)
    li.start()
    return li.alreadyLogedIn()  