import sublime, sublime_plugin
import threading
import urllib.request
import urllib.error
import json

class ChalmFoodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        thread = DataGetter(10)

        thread.start()
        thread.join()

        self.handle_result(edit, thread.result)

    def handle_result(self, edit, result):
        sublime.status_message('Chalm food successfully ran the request')

        for restaurant in result:
            title = restaurant["title"]
            self.view.insert(edit, 0, "= " +  title + " =\n")

            dishes = restaurant["dishes"]
            for dish in dishes:
                self.view.insert(edit, self.view.size(), "\t" + dish["title"] + "\n")
                self.view.insert(edit, self.view.size(), "\t\t" + dish["desc"] + "\n")
            # self.view.insert(edit, self.view.size(), "\n\n")


class DataGetter(threading.Thread):
    def __init__(self, timeout):
        self.timeout = timeout
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        try:
            siteReq = urllib.request.urlopen("http://vps.nandreasson.se:5000/johanneberg", timeout=self.timeout)
            self.result = json.loads( siteReq.readall().decode("utf-8") )
            siteReq.close()
            return
        except urllib.error.HTTPError as e:
            err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
        except urllib.error.URLError as e:
            err = '%s: URL error %s contacting API' % (__name__, str(e.reason))
        sublime.error_message(err)
        self.result = False