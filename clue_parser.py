#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-
from __future__ import with_statement
from bs4 import BeautifulSoup
from glob import glob
from tkinter import ttk
import os
import re
import sqlite3
import sys
import threading
import Tkinter as tk


class Parser(tk.Frame):
    """docstring for parser"""
    def __init__(self, parent, *args, **kwargs):
        self.text = tk.StringVar()
        self.dir = "j-archive"
        self.database = "jclues.db"
        self.parsed = 0
        self.total =  len(os.listdir(self.dir))
        """GUI SETUP"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.label = tk.Label(self.parent,text = "Click to Start")
        self.label.pack()
        self.parseButton = ttk.Button(self.parent,text="Parse Files", command=self.main)
        self.closeButton = ttk.Button(self.parent,text="Close", command=self.parent.quit)

        self.progress = ttk.Progressbar(self.parent, orient="horizontal",
                                   length=200, mode="determinate")
        self.parseButton.pack(side = tk.TOP) 
        self.progress["value"] = 0
        self.progress.pack(side=tk.TOP)
         
    def main(self):
        def realMain():
            self.progress.start()
            self.parse()
            print "Parsing game files"
        self.parseButton.pack_forget()
        threading.Thread(target=realMain).start()

    def start(self):
        self.maxbytes = self.total
        self.progress["maximum"] = self.total
        self.parse()
        # threading.Thread(target=realMain).start()

    def parse(self):
        """Loop thru all the games and parse them."""
        self.sql = sqlite3.connect(self.database)
        if not os.path.isdir(self.dir):
            print "j-archive folder not found"
            sys.exit(1)
        NUMBER_OF_FILES = len(os.listdir(self.dir))
        print "Parsing", NUMBER_OF_FILES, "files"
        #[game, airdate, round, category, value, clue, answer]
        if not os.path.isfile(self.database):
            self.sql.execute("""PRAGMA foreign_keys = ON;""")
            self.sql.execute("""CREATE TABLE clues(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game INTEGER,
                airdate TEXT,
                round INTEGER,
                category TEXT,
                value INTEGER,
                clue TEXT,
                answer TEXT
            );""")
        for i, file_name in enumerate(glob(os.path.join(self.dir, "*.html")), 1):
            self.parsed +=1
            self.progress["value"] = self.parsed/self.total
            self.label.config(text = "Parsing page %s" %i)

            with open(os.path.abspath(file_name)) as f:
                self.parse_game(f, i)
            if i%1000 ==0:
                print i,"committed"
                self.sql.commit()
        self.sql.commit()
        self.progress.pack_forget
        self.label.config(text = "All Done")
        self.closeButton.pack()
        print "All done"


    def parse_game(self, f, gid):
        """Parses an entire Jeopardy! game and extract individual clues."""
        bsoup = BeautifulSoup(f, "lxml")
        # The title is in the format: `J! Archive - Show #XXXX, aired 2004-09-16`,
        # where the last part is all that is required
        airdate = bsoup.title.get_text().split()[-1]
        if not self.parse_round(bsoup, 1, gid, airdate) or not self.parse_round(bsoup, 2, gid, airdate):
            # One of the rounds does not exist
            pass
        # The final Jeopardy! round
        r = bsoup.find("table", class_="final_round")
        if not r:
            # This game does not have a final clue
            return
        category = r.find("td", class_="category_name")
        if not category:
            print "err"
            return
        category = category.get_text()
        text = r.find("td", class_="clue_text").get_text()
        answer = BeautifulSoup(r.find("div", onmouseover=True).get("onmouseover"), "lxml")
        answer = answer.find("em").get_text()
        # False indicates no preset value for a clue
        self.insert([gid, airdate, 3, category, False, text, answer])


    def parse_round(self,bsoup, rnd, gid, airdate):
        """Parses and inserts the list of clues from a whole round."""
        round_id = "jeopardy_round" if rnd == 1 else "double_jeopardy_round"
        r = bsoup.find(id=round_id)
        # The game may not have all the rounds
        if not r:
            return False
        # The list of categories for this round
        categories = [c.get_text() for c in r.find_all("td", class_="category_name")]
        # The x_coord determines which category a clue is in
        # because the categories come before the clues, we will
        # have to match them up with the clues later on.
        x = 0
        for a in r.find_all("td", class_="clue"):
            is_missing = True if not a.get_text().strip() else False
            if not is_missing:
                value = a.find("td", class_=re.compile("clue_value")).get_text().lstrip("D: $")
                text = a.find("td", class_="clue_text").get_text()  
                answer = BeautifulSoup(a.find("div", onmouseover=True).get("onmouseover"), "lxml")
                answer = answer.find("em", class_="correct_response").get_text()
                self.insert([gid, airdate, rnd, categories[x], value, text, answer])
            # Always update x, even if we skip
            # a clue, as this keeps things in order. there
            # are 6 categories, so once we reach the end,
            # loop back to the beginning category.
            #
            # Using modulus is slower, e.g.:
            #
            # x += 1
            # x %= 6
            #
            x = 0 if x == 5 else x + 1
        return True


    def insert(self,clue):
        """Inserts the given clue into the database."""
        # Clue is [game, airdate, round, category, value, clue, answer]
        # Note that at this point, clue[4] is False if round is 3
        #[game, airdate, round, category, value, clue, answer]

        if "\\\'" in clue[6]:
            clue[6] = clue[6].replace("\\\'", "'")
        if "\\\"" in clue[6]:
            clue[6] = clue[6].replace("\\\"", "\"")
        if not self.sql:
            print clue
            return
        self.sql.execute("INSERT INTO clues Values(null,?, ?, ?, ?, ?, ?, ?)",(clue[0],clue[1],clue[2],clue[3],clue[4],clue[5],clue[6], ))

def StartParser():
    root = tk.Tk()
    root.title("Parser")
    root.geometry("400x100")
    root.resizable(0,0)
    Parser(root)
    root.mainloop()

if __name__ == "__main__":
    StartParser()
