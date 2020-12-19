import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import time
from datetime import datetime

import webbrowser
import ast

import dailydata
import newssearch
import updatingdata


font_use= ("Verdana", 14)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

ticker_symbol = None

current_value = None
last_updated = None

def animate(i):
	global ticker_symbol

	if not ticker_symbol: # simple way to wait 
		return

	ticker_file = ticker_symbol + '.txt' # again, not error-checking

	with open(ticker_file, 'r') as file: # same here
		ticker_data = file.read()
	data_list = ticker_data.split('\n')

	time_list = []
	ticker_list = []

	for line in data_list:
		if len(line) > 1:
			ti, val = line.split(',') # x, y?
			time_struct = time.strptime(ti, '%Y-%m-%d %H:%M:%S')
			time_dt = datetime.fromtimestamp(time.mktime(time_struct))
			time_list.append(time_dt)
			ticker_list.append(float(val))

	a.clear()
	a.plot(time_list, ticker_list)

def update_ticker(ticker_entry):
	new_ticker = ticker_entry.get()
	global ticker_symbol
	ticker_symbol = new_ticker
	dailydata.main(new_ticker)
	print("Ticker is now " + new_ticker)

def update_news(controller):
	newssearch.main()

def start_update():
	while(1):
		quotetime, quote = updatingdata.main(ticker_symbol)
		time.sleep(3.15)
		global current_value
		current_value = quote
		global last_updated
		last_updated = quotetime


class FineAdvisorApp(tk.Tk):

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

#        tk.Tk.iconbitmap(self, default="clienticon.ico")
		tk.Tk.wm_title(self, "Fine Advisor")
#        icon = tk.Image('photo', file='currency_black_dollar.png')
#        tk.Tk.iconbitmap(self, default='icon.icns')
#        root = tk.Tk()
#        root.tk.call('wm', 'iconphoto', root._w, icon)

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (StartPage, NewsPage):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()

        
class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text="Start Page", font=font_use)
		label.pack(pady=10,padx=10)

		button = ttk.Button(self, text="News Page",
		                    command=lambda: controller.show_frame(NewsPage))
		button.pack()

		entry_label = tk.Label(self, text="Enter stock ticker symbol:")
		entry_var = tk.StringVar()
		ticker_entry = tk.Entry(self, textvariable = entry_var, font=('calibre',10,'normal'))

		entry_button = ttk.Button(self, text='Submit', command=lambda: update_ticker(ticker_entry))
		entry_label.pack()
		ticker_entry.pack()
		entry_button.pack()

		start_updating_button = ttk.Button(self, text='Update', command=lambda: start_update())
		start_updating_button.pack()

#		current_stringvar = tk.StringVar()
#		if 
#		current_label = tk.Label(self, current_stringvar)



		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class NewsPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Recent News", font=font_use)
		label.pack(pady=10,padx=10)

		button1 = ttk.Button(self, text="Back to Home",
							command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = ttk.Button(self, text="Update News",
							command=lambda: update_news(controller))
		button2.pack()

		# Load data from "cache" text file: new button to update 
		with open('articles-list.txt', 'r') as file:
			list_read = file.read()

		pair_list = ast.literal_eval(list_read) 

		titles = []
		urls = []

		for title, url in pair_list:
			words = title.split(' ')	# to split title 
			words.insert(int(len(words)/2), '\n')
			title_new = ' '.join(words)
			titles.append(title_new)
			urls.append(url)

		while len(titles) < 6:
			titles.append("No more new articles from this site.")
			urls.append('https://google.com')


		newsbuttonA = tk.Button(self, text=titles[0], height=5,width=70,
			command=lambda: webbrowser.open(urls[0], new=1))
		newsbuttonA.pack()

		newsbuttonB = tk.Button(self, text=titles[1], height=5,width=70,
			command=lambda: webbrowser.open(urls[1], new=1))
		newsbuttonB.pack()

		newsbuttonC = tk.Button(self, text=titles[2], height=5,width=70,
			command=lambda: webbrowser.open(urls[2], new=1))
		newsbuttonC.pack()

		newsbuttonD = tk.Button(self, text=titles[3], height=5,width=70,
			command=lambda: webbrowser.open(urls[3], new=1))
		newsbuttonD.pack()

		newsbuttonE = tk.Button(self, text=titles[4], height=5,width=70,
			command=lambda: webbrowser.open(urls[4], new=1))
		newsbuttonE.pack()

		newsbuttonF = tk.Button(self, text=titles[5], height=5,width=70,
			command=lambda: webbrowser.open(urls[5], new=1))
		newsbuttonF.pack()


app = FineAdvisorApp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()

