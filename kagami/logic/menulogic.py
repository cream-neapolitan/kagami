'''Function that will be binded to menu entry'''

from webbrowser import open as w_open

# About menu logic
def open_twitter():
    url = 'http://twitter.com/CreamNeapolitan'
    w_open(url, new=2, autoraise=True)


def open_github():
    url = 'http://github.com/cream-neapolitan/kagami'
    w_open(url, new=2, autoraise=True)
