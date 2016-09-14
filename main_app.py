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
                         text="New Game", fg="black",height = 2,
                         command=jeopardy.StartJeopardy)
		self.newGameButton.pack(fill=tk.X,side=tk.TOP)
		
		# self.startEditorButton = tk.Button(self.parent, 
  #                        text="Create a Board", fg="black",
  #                        command=self.parent.quit)
		# self.startEditorButton.pack(side=tk.TOP)

		self.startDownloaderButton = tk.Button(self.parent, 
                         text="Start Downloader", fg="black",height = 2,
                         command=downloader.StartDownloader)
		self.startDownloaderButton.pack(fill=tk.X , side=tk.TOP)

		self.startParserButton = tk.Button(self.parent, 
                         text="Start Parse", fg="black", height = 2,
                         command=clue_parser.StartParser)
		self.startParserButton.pack(fill=tk.X,side=tk.TOP)


		self.quitButton = tk.Button(self.parent, 
                         text="QUIT", fg="red", height=2,
                         command=self.parent.quit)
		self.quitButton.pack(fill=tk.X,side=tk.TOP)
		


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
	root.geometry("200x160")
	root.resizable(0,0)
	MainApplication(root)
	root.mainloop()