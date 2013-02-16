import sublime, sublime_plugin
import threading
import urllib2
import json

class ChalmFoodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # self.view.insert(edit, 0, "Hello, World!")
        thread = DataGetter(5)
        thread.start()
        self.handle_threads(edit, thread)

    def handle_threads(self, edit, threads):
        if threads.is_alive():
            sublime.set_timeout(lambda: self.handle_threads(edit, threads), 100)
            return
        sublime.status_message('Chalm food successfully ran the request')
        print threads.result
        result = threads.result
        for restaurant in result:
            title = result[restaurant]["title"]
            self.view.insert(edit, 0, "= " +  title + " =\n")
            
            dishes = result[restaurant]["dishes"]
            for dish in dishes:
                self.view.insert(edit, self.view.size(), "\t" + dish["title"] + "\n")
                self.view.insert(edit, self.view.size(), "\t\t" + dish["desc"] + "\n")


class DataGetter(threading.Thread):
    def __init__(self, timeout):
        self.timeout = timeout
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        try: 
            siteReq = urllib2.urlopen("http://localhost:5000/johanneberg", timeout=self.timeout)
            self.result = json.load(siteReq)
            siteReq.close()
            return
        except (urllib2.HTTPError) as (e):  
            err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))  
        except (urllib2.URLError) as (e):  
            err = '%s: URL error %s contacting API' % (__name__, str(e.reason))  
        sublime.error_message(err)  
        self.result = False  