import sublime, sublime_plugin
import threading
import urllib.request
import urllib.error
import json

class ChalmFoodCommand(sublime_plugin.TextCommand):
    def run(self, edit, campus="johanneberg"):
        url ="http://vps.nandreasson.se:5000/" + campus
        thread = DataGetter(10, url)

        thread.start()
        thread.join()

        self.handle_result(edit, thread.result)

    def handle_result(self, edit, result):
        sublime.status_message('Chalm food successfully ran the request')

        new_tab = self.view.window().new_file()
        new_tab.set_name("ChalmFood")
        new_tab.set_scratch(True)

        for restaurant in result:
            title = restaurant["title"]
            new_tab.insert(edit, 0, "\n= " +  title + " =\n")

            dishes = restaurant["dishes"]
            for dish in dishes:
                new_tab.insert(edit, new_tab.size(), "\t" + dish["title"] + "\n")
                new_tab.insert(edit, new_tab.size(), "\t\t" + dish["desc"] + "\n\n")

        new_tab.set_read_only(True)



class DataGetter(threading.Thread):
    def __init__(self, timeout, url):
        self.url = url
        self.timeout = timeout
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        try:
            siteReq = urllib.request.urlopen(self.url, timeout=self.timeout)
            self.result = json.loads( siteReq.readall().decode("utf-8") )
            siteReq.close()
            return
        except urllib.error.HTTPError as e:
            err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
        except urllib.error.URLError as e:
            err = '%s: URL error %s contacting API' % (__name__, str(e.reason))
        sublime.error_message(err)
        self.result = False