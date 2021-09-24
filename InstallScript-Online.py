"""
InstallScript-Online.py
Author: Gabriel Herrera
Email: gherrera@managedservicesit.com
Date: 9/23/21

This file pulls data from the github repo depending on what the user wants to install.
Like the offline mode InstallScript, InstallScript-Online will do both the "full monty"
and the "a-la-carte" by pulling necessary dependencies from the github repo rather than locally storing them.
"""

"""
requests module handles interacting with URLs via http/https to get, push, post and whatever else from the servers themselves.
In this case, we supply it a token I generated from the private repo which has limited permissions and
use the headers recommended by the github API to access the URL properly.
"""
import requests
import os
from requests.exceptions import RequestException

"""
url holds the URL of the file in question.
workingdir holds the ideal location the program should work out of and create directories in.
"""

url = r"https://raw.githubusercontent.com/BoomEarth/InstallScript-Online/main/Payloads/Winget/Microsoft.VCLibs.x64.14.00.Desktop.appx"
token = "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"
headers = {'accept': 'application/vnd.github.v3+json'}
workingdir = "C:\\UTIL\\test\\"

if not os.path.isdir(workingdir):

    os.mkdir(workingdir)

"""
We create a session as "session" and then authorize it with BoomEarth and the token. This session persists through the duration of the script 
so any subsequent calls to github are already pre-authorized by use of the token as this script acts as a client.
by calling session.get we're using the "get" command to pull information from a URL that would otherwise not be visible to us. We'd receive a 404 / 403 error (forbidden or not found)
but since we supplied a username and a token, the client is considered logged in and the script has permission to browse the repo and download what it needs to.
"""

with requests.Session() as session:
    session.auth = ('BoomEarth', token)

os.chdir(workingdir)

"""
Here we pull all relevant information from the URL and place it in "file_download".
We wrap it in a try catch to make sure if there's an exception to print the error and close.
"""

try:

    file_download = session.get(url, headers=headers)

except RequestException as e:

    print(e)

"""
If the status code of the url is 200 (meaning a success regarding authorization and file path)
then we continue with the script. We parse the filename from the URL, which for github is always consistent, as
there's no content disposition marker with the name of the file to scrape otherwise.
We then create f(ile) by using open() which allows python to write to disk at the workingdir directory ending in the name of the file we want (we're creating a file with that name)
and we write to it from the content in file_download (which is the file we want).

If the status code isn't 200, we print it and attempt to debug
"""

if file_download.status_code == 200:

    fname = url.split("/")[-1]
    with open(workingdir + fname, 'wb') as f:
    
        f.write(file_download.content)

else:

    print(file_download.status_code)

