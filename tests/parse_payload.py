#!/usr/bin/env python3

import requests
import http.cookiejar
import sys
import re


from pyquery import PyQuery as pq

def parsePayload(doc, form_selector):
    inputs = doc.find("%s input" % (form_selector))
    print(inputs)
    payload={}
    for input in inputs:
        print(input.value)
        payload[input.name]=input.value
    return payload

file_path = 'login_stage_3_output.html'

# Open the file in read mode ('r')
with open(file_path, 'r') as file:
    # Read the entire contents of the file into a variable
    content = file.read()
    doc = pq(content)
    form_selector = "form.pin-verification-form"
    form = doc(form_selector)
    if form:
        payload=parsePayload(doc, form_selector)
        print(payload)

# Print the contents of the file
# print(file_contents)



    

