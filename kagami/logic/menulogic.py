'''Function that will be binded to menu entry'''

from webbrowser import open as w_open

# File menu logic
def browse_file():
    print("Browsing file now")


def save_file():
    print("Saving file now")


# About menu logic
def open_twitter():
    url = 'http://twitter.com/CreamNeapolitan'
    w_open(url, new=2, autoraise=True)


def open_github():
    url = 'http://github.com/cream-neapolitan/kagami'
    w_open(url, new=2, autoraise=True)
