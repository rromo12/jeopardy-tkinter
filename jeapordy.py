import os
import sqlite3
import random
import pickle
from collections import defaultdict
import Tkinter as tk
#########TODO
# Class MAIN APPLICATION (NEW GAME, or DOWNLOAD/PARSE)
# Implement option for hidden clues with just values 
# Option for New Game 

class Jeapardy(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """Initialization"""
        self.db = "jclues.db"
        # self.db = os.path.join(sys._MEIPASS, "jclues.db")
        self.sql = sqlite3.connect(self.db)
        #Load/Create Settings
        self.showClues = True
        self.rnd = 1
        """GUI SETUP"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        #Add file menu
        menubar = tk.Menu(self.parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Game", command=lambda newGame =True:self.createBoard(newGame))
        # filemenu.add_command(label="Save Game", command=donothing)
        # filemenu.add_command(label="Load Game", command=donothing)
        filemenu.add_command(label="Close", command=self.parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        #Add View Menu
        viewmenu = tk.Menu(menubar,tearoff=0)
        viewmenu.add_checkbutton(label="Show Clues", command=self.showHideClues)
        menubar.add_cascade(label="View",menu=viewmenu)
        self.parent.config(menu=menubar)
        self.createBoard(True)


    def showHideClues(self):
      cols,rows = self.parent.grid_size()
      if(self.rnd==3):
        return
      if(self.showClues):
        #hide remaining clues
        # col = 0
        for col in range(cols):
          for row in range(1,rows):
              category = self.parent.grid_slaves(column=col,row = 0)[0].config()["text"][4]
              celltext = self.parent.grid_slaves(row,col)[0].config()["text"][4]
              clue = self.board[category][row-1]
              if(celltext == str(row*self.rnd*200)):
                        self.parent.grid_slaves(row,col)[0].config(text = clue[6])
      else:
        for col in range(cols):
          for row in range(1,rows):
              category = self.parent.grid_slaves(column=col,row = 0)[0].config()["text"][4]
              celltext = self.parent.grid_slaves(row,col)[0].config()["text"][4]
              clue = self.board[category][row-1]
              if(celltext == clue[6]):
                        self.parent.grid_slaves(row,col)[0].config(text = str(row*self.rnd*200))
        
      self.showClues = not(self.showClues)
    def createBoard(self,newGame):
        if(newGame):
          self.parent.title("JEOPARDY! Round 1")
          self.rnd = 1
          self.usedClueCnt = 0
        self.selectCategories()
        self.getClues()
        col = 0
        for category in self.categories:
          row = 0
          label = tk.Label(self.parent,text = category,relief = tk.RAISED, width = 15, height = 5,wraplength=150, bg = "blue",fg = "white")
          label.config(font=("Courier", 16))
          label.grid(column = col, row = row)
          for clue in self.board[category]:
                row +=1
                label = tk.Button(self.parent,text = str(row*200*self.rnd) if self.showClues else clue[6],relief = tk.RAISED,width = 24,height = 6, wraplength=200,bg="blue",fg="white" ,command=lambda row=row, column=col: self.buttonAction(row, column))
                label.config(font=("Courier",10))
                label.grid(column=col,row=row)
          col+=1    
    
    def selectCategories(self):
      if os.path.isfile("usable_category.lst"):
        self.usable_category_list = self.load("usable_category.lst")
      else:
       # else create it from sql query
       # and save it
       self.usable_category_list = self.sql.execute("select category from (select category,count(*) as catcnt from clues group by category) where catcnt >= 5;").fetchall()
       self.usable_category_list = [e for l in self.usable_category_list for e in l]
       self.save(self.usable_category_list,"usable_category.lst")

      self.categories = random.sample(self.usable_category_list,5)

    def getClues(self):
        """Given 5 categories return clues for those categories """
        self.clues = self.sql.execute("select  * from clues where category = ?  or category = ? or category = ? or category = ? or category = ?;", (self.categories[0],self.categories[1],self.categories[2],self.categories[3],self.categories[4], )).fetchall()
        self.board = defaultdict(list)
        for clue in self.clues:
            clue_cat = clue [4]
            self.board[clue_cat].append(clue)
        for category in self.categories:
            self.board[category] = random.sample(self.board[category],5)
          
    def save(self,Obj, Filename):
          """Given an object and a file name, write the object to the file using pickle."""

          f = open(Filename, "w")
          p = pickle.Pickler(f)
          p.dump(Obj)
          f.close()
       
    def load(self,Filename):
          """Given a file name, load and return the object stored in the file."""
          f = open(Filename, "r")
          u = pickle.Unpickler(f)
          Obj = u.load()
          f.close()
          return Obj

    def buttonAction(self,row,column):
      category = self.parent.grid_slaves(column=column,row = 0)[0].config()["text"][4]
      currentText = self.parent.grid_slaves(column=column,row = row)[0].config()["text"][4]
      clue = self.board[category][row-1]
      if currentText == str(row*200*self.rnd):
        self.parent.grid_slaves(row,column)[0].config(text = clue[6])
      else:
        self.parent.grid_slaves(row,column)[0].config(text = clue[7],state=tk.DISABLED)
        self.usedClueCnt +=1
        if(self.usedClueCnt==25):
          self.rnd = 2
          self.nextRound() 
          # Need a wait/confirm before creating new board so we can show the answer
          self.parent.title("JEOPARDY! Round 2")
        if(self.usedClueCnt==50):
          #wait 
          self.rnd = 3
          self.finalRound() 
    
    def nextRound(self):
        self.newWindow = tk.Toplevel(self.parent)
        self.app = nextRoundDialog(self)

    def finalRound(self):
        self.newWindow = tk.Toplevel(self.parent)
        self.app = finalJeopardyDialog(self)

    def finalJeopardy(self):
      self.parent.title("JEOPARDY! Final Jeapardy")
      for cell in self.parent.grid_slaves(): 
        cell.grid_forget()
      #Generate final jeopardy clue
      self.selectCategories()
      self.finalCategory = random.sample(self.categories,1)[0]
      self.finalClue = self.sql.execute("select  * from clues where category = ?",(self.finalCategory,)).fetchone()
      #Show Clue
      self.final = tk.Button(self.parent,text = self.finalCategory,relief = tk.RAISED,width = 24,height = 6, wraplength=1000,bg="blue",fg="white" ,command=self.finalJeopardyButton)
      self.final.config(font=("Courier",44))
      self.final.pack(fill=tk.BOTH,expand =1)

    def finalJeopardyButton(self):
      current = self.final.config()["text"][4]
      if(current == self.finalCategory):
        self.final.config(text = self.finalClue[6])
      else:
        self.final.config(text = self.finalClue[7])



class nextRoundDialog(tk.Frame):
    def __init__(self, master):
        self.jeopardy = master
        self.master = master.newWindow
        self.frame = tk.Frame(self.master)
        self.Button = tk.Button(self.frame, text = 'Next Round', width = 25, command = self.nextRound)
        self.Button.pack()
        self.frame.pack()
    def nextRound(self):
        self.jeopardy.createBoard(0)
        self.master.destroy()

class finalJeopardyDialog(tk.Frame):
    def __init__(self, master):
        self.jeopardy = master
        self.master = master.newWindow
        self.frame = tk.Frame(self.master)
        self.Button = tk.Button(self.frame, text = 'Next Round', width = 25, command = self.nextRound)
        self.Button.pack()
        self.frame.pack()
    def nextRound(self):
        self.jeopardy.finalJeopardy()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("JEOPARDY! Round 1")
    root.geometry("1010x680")
    root.resizable(0,0)
    Jeapardy(root)
    root.mainloop()

