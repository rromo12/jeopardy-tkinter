import jeopardy
import downloader
import clue_parser

# import editor
import Tkinter as tk
class MainApplication(tk.Frame):
	"""docstring for MainApplication"""
	def __init__(self, parent,*args,**kwargs):
		
		"""GUI SETUP"""
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		#Create Buttons
		self.newGameButton = tk.Button(self.parent, 
                         text="New Game", fg="black",
                         command=jeopardy.StartJeopardy)
		self.newGameButton.pack(side=tk.TOP)
		
		# self.startEditorButton = tk.Button(self.parent, 
  #                        text="Create a Board", fg="black",
  #                        command=self.parent.quit)
		# self.startEditorButton.pack(side=tk.TOP)

		self.startDownloaderButton = tk.Button(self.parent, 
                         text="Start Downloader", fg="black",
                         command=downloader.StartDownloader)
		self.startDownloaderButton.pack(side=tk.TOP)

		self.startParserButton = tk.Button(self.parent, 
                         text="Start Parse", fg="black",
                         command=clue_parser.StartParser)
		self.startParserButton.pack(side=tk.TOP)


		self.quitButton = tk.Button(self.parent, 
                         text="QUIT", fg="red",
                         command=self.parent.quit)
		self.quitButton.pack(side=tk.TOP)
		


	def startGame(self):
		pass

	def startEditor():
		pass

	def startDownloader(self):
		pass
	def startParser(self):
		pass





if __name__ == "__main__":
	root = tk.Tk()
	root.title("JEOPARDY!")
	root.geometry("1010x680")
	root.resizable(0,0)
	MainApplication(root)
	root.mainloop()