import tkinter as tk
import tkinter.ttk as ttk
import threading
import queue

import matplotlib.pyplot as pl
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.render import render_latex

matplotlib.use('Agg')


class ProblemPage(ttk.Frame):
	def __init__(self,parent,problem):
		ttk.Frame.__init__(self,parent)
		self.problem = problem
		
		self.refernce_preservation = {}
		self.string_vars = {}
		self.first_update = False
		
		self.rowconfigure(0,weight=1)
		self.columnconfigure(0,weight=1)
		self.build_contents()
	
	def build_contents(self):
		paned_window = ttk.Panedwindow(self,orient=tk.HORIZONTAL)
		paned_window.grid(row=0,column=0,sticky='nsew')
		
		settings_pane = ttk.Frame(paned_window,padding=3)
		self.build_settings(settings_pane)
		paned_window.add(settings_pane)
		
		self.figure = pl.figure(layout='tight')
		self.canvas = FigureCanvasTkAgg(self.figure,master=paned_window)
		figure_pane = self.canvas.get_tk_widget()
		paned_window.add(figure_pane)
	
	def build_settings(self,settings_pane):
		settings_pane.columnconfigure(0,weight=1)
		settings_pane.columnconfigure(0,weight=1)
		
		self.update_button = ttk.Button(settings_pane,
			text='Update Plot',command=self.update_figure)
		self.update_button.grid(row=0,column=0,sticky='sew')
		self.update_button.state(['disabled'])
		
		self.progress_bar = ttk.Progressbar(settings_pane,orient=tk.HORIZONTAL)
		self.progress_bar.grid(row=1,column=0,sticky='nsew')
		
		frame = ttk.Labelframe(settings_pane,text='Settings',padding=(5,3))
		frame.grid(row=2,column=0,sticky='ew')
		self.build_table(frame)
	
	def build_table(self,frame):
		desc = self.problem.get_descriptors()
		defaults = self.problem.get_params()
		
		frame.columnconfigure(0,weight=1)
		frame.columnconfigure(0,weight=1)
		for k in range(1,4):
			frame.columnconfigure(k,weight=0)
		
		for (k,text) in enumerate(['Quantity','Symbol','Units','Value']):
			label = ttk.Label(frame,text=text,font='TkHeadingFont')
			label.grid(row=0,column=k,sticky='' if k in (1,2) else 'w')
		
		sep = ttk.Separator(frame,orient=tk.HORIZONTAL)
		sep.grid(row=1,column=0,columnspan=4,sticky='ew',pady=3)
		
		for (i,(key,fields)) in enumerate(desc.items()):
			text,symbol,units,low,high,step = fields
			row = i+2
			
			label = ttk.Label(frame,text=text)
			label.grid(row=row,column=0,sticky='ew')
			
			image = tk.PhotoImage(data=render_latex(symbol),format='png')
			self.refernce_preservation[(key,'symbol')] = image
			label = ttk.Label(frame,image=image)
			label.grid(row=row,column=1)
			
			image = tk.PhotoImage(data=render_latex(units),format='png')
			self.refernce_preservation[(key,'units')] = image
			label = ttk.Label(frame,image=image)
			label.grid(row=row,column=2)
			
			self.string_vars[key] = tk.StringVar(value=defaults[key])
			self.string_vars[key].trace_add('write',self.invalidate)
			spin = ttk.Spinbox(frame,textvariable=self.string_vars[key],
				from_=low,to=high,increment=step,width=10)
			spin.grid(row=row,column=3)
	
	def invalidate(self,*args):
		self.update_button.state(['!disabled'])
	
	def update_figure(self):
		if not self.first_update:
			self.first_update = True
		
		params = {key:float(val.get()) for (key,val) in self.string_vars.items()}
		self.problem.set_params(params)
		
		self.connection = queue.Queue()
		thread = threading.Thread(target=self.problem.plot,
			args=(self.figure,self.connection))
		thread.start()
		self.update_button.state(['disabled'])
		self.after(10,self.update_progress)
	
	def update_progress(self):
		if not self.connection.empty():
			item = self.connection.get_nowait()
			
			if item=='done':
				self.progress_bar['value'] = 100
				self.canvas.draw()
				return
			elif type(item)==float:
				self.progress_bar['value'] = 100*item
			
		self.after(10,self.update_progress)
