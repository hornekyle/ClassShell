import tkinter as tk
import tkinter.ttk as ttk

from gui.page import ProblemPage

class MainWindow(tk.Tk):
	def __init__(self,problems):
		tk.Tk.__init__(self)
		
		style = ttk.Style()
		# style.theme_use('alt')
		
		self.title('Analytical-GUI')
		self.rowconfigure(0,weight=1,minsize=600)
		self.columnconfigure(0,weight=1,minsize=1000)
		
		self.book = self.build_contents(problems)
	
	def build_contents(self,problems):
		book = ttk.Notebook(self)
		book.grid(row=0,column=0,sticky='nsew')
		book.bind('<<NotebookTabChanged>>',self.change_page)
		for problem in problems:
			frame = ProblemPage(self,problem)
			book.add(frame,text=problem.get_name())
		return book
	
	def __call__(self):
		self.mainloop()
	
	def change_page(self,*args):
		name = self.book.select()
		page = self.book.nametowidget(name)
		if not page.first_update:
			page.update_figure()
