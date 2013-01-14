import sublime, sublime_plugin
import threading
import urllib2
from HTMLParser import HTMLParser as parser


class ChalmFoodHTMLParser(parser):
    def __init__(self):
        parser.__init__(self)
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == "ul":
            for name, value in attrs:
                if name == "id" and value == "K":
                    self.recording = 1

    def handle_endtag(self, tag):
        if tag == "ul":
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)


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
        pt = ChalmFoodHTMLParser()
        siteReq = urllib2.urlopen("http://chalmerskonferens.se/dagens-menyer/johanneberg/")
        self.result = siteReq.read()
        self.result = self.result.decode("utf-8")
        print self.result
        pt.feed(self.result)
        print pt.data
        pt.close()
        siteReq.close()
