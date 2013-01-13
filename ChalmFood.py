import sublime, sublime_plugin
import threading
import urllib
from HTMLParser import HTMLParser


class ChalmFoodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")
        thread = DataGetter(5)
        thread.start()

class DataGetter(threading.Thread):
    def __init__(self, timeout):
        self.timeout = timeout
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        parser = ChalmFoodHTMLParser()
        siteReq = urllib.urlopen("http://chalmerskonferens.se/dagens-menyer/johanneberg/")
        self.result = siteReq.read()
        parser.feed(self.result)
        print parser.data
        parser.close()
        siteReq.close()

class ChalmFoodHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'ul':
            for name, value in attrs:
                if name == 'id' and value == 'K':
                    self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'ul':
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)