#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-
from tkinter import ttk
import clue_parser
import itertools
import os
import urllib2
import time
import concurrent.futures as futures  # In Python 3 we can use "import concurrent.futures as futures"
import threading
import Tkinter as tk




class Downloader(tk.Frame):
    """Downloader"""

    def __init__(self, parent,*args,**kwargs):
        self.text = tk.StringVar()
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        self.current_working_directory = application_path
        self.archive_folder = os.path.join(self.current_working_directory, "j-archive")
        self.SECONDS_BETWEEN_REQUESTS = 5
        self.ERROR_MSG = "ERROR: No game"
        self.NUM_THREADS = 2  # Be conservative
        try:
            import multiprocessing
            # Since it's a lot of IO let's double # of actual cores
            self.NUM_THREADS = multiprocessing.cpu_count() * 2
            self.text.set('Using {} threads'.format(self.NUM_THREADS))
            print 'Using {} threads'.format(self.NUM_THREADS)
        except (ImportError, NotImplementedError):
            pass
        """GUI SETUP"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.label = tk.Label(self.parent,text = self.text.get())
        self.label.pack()
        self.startButton = ttk.Button(self.parent,text="start downloading", command=self.main)
        self.closeButton = ttk.Button(self.parent,text="Close Button", command=self.quit)
        self.progress = ttk.Progressbar(self.parent, orient="horizontal",
                                   length=200, mode="indeterminate")
        self.startButton.pack(side = tk.TOP)        
        

    def main(self):
        def realMain():
            self.progress.start()
            self.create_archive_dir()
            self.text.set("Downloading game files")
            print "Downloading game files"
            self.download_pages()
        self.startButton.pack_forget()
        self.progress.pack(side=tk.TOP)

        threading.Thread(target=realMain).start()
    
    def onFinishedDownloads(self):
        self.closeButton.pack()
        self.progress.stop()

    def create_archive_dir(self):
        if not os.path.isdir(self.archive_folder):
            self.text.set("Making %s" % self.archive_folder)
            print "Making %s" % self.archive_folder
            os.mkdir(self.archive_folder)


    def download_pages(self):
        page = 1
        with futures.ThreadPoolExecutor(max_workers=self.NUM_THREADS) as executor:
            # We submit NUM_THREADS tasks at a time since we don't know how many
            # pages we will need to download in advance
            while True:
                l = []
                for i in range(self.NUM_THREADS):
                    f = executor.submit(self.download_and_save_page, page)
                    l.append(f)
                    page += 1
                # Block and stop if we're done downloading the page
                if not all(f.result() for f in l):
                    break


    def download_and_save_page(self,page):
        if(page%5==0):
            print page
            self.label.config(text = "Downloading page %s" %page)

        new_file_name = "%s.html" % page
        destination_file_path = os.path.join(self.archive_folder, new_file_name)
        if not os.path.exists(destination_file_path):
            html = self.download_page(page)
            if self.ERROR_MSG in html:
                # Now we stop
                self.label.config(text = "Finished downloading. Now parse.")
                print "Finished downloading. Now parse."
                self.onFinishedDownloads()

                return False
            elif html:
                self.save_file(html, destination_file_path)
                time.sleep(self.SECONDS_BETWEEN_REQUESTS)# Remember to be kind to the server
        else:
            print "Already downloaded %s" % destination_file_path
        return True


    def download_page(self,page):
        url = 'http://j-archive.com/showgame.php?game_id=%s' % page
        html = None
        try:
            response = urllib2.urlopen(url)
            if response.code == 200:
                self.text.set("Downloading %s" % url)
                print "Downloading %s" % url
                html = response.read()
            else:
                self.text.set("Invalid URL: %s" % url)
                print "Invalid URL: %s" % url
        except urllib2.HTTPError:
            self.text.set("Failed to open %s" % url)
            print "Failed to open %s" % url
        return html


    def save_file(self,html, filename):
        try:
            with open(filename, 'w') as f:
                f.write(html)
        except IOError:
            self.text.set("Couldn't write to file %s" % filename)
            print "Couldn't write to file %s" % filename

def StartDownloader():
    root = tk.Tk()
    root.title("Downloader")
    root.geometry("400x100")
    root.resizable(0,0)
    Downloader(root)
    root.mainloop()


if __name__ == "__main__":
    StartDownloader()