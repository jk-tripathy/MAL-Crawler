from tkinter import *
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import requests


genres = ['Action', 'Adventure', 'Cars', 'Comedy', 
		'Demons', 'Drama', 'Ecchi', 'Fantasy',
		'Harem', 'Hentai', 'Historical', 'Horror'
		'Kids', 'Magic', 'Martial Arts', 'Mecha',
		'Music', 'Mystery', 'Parody', 'Police',
		'Romance', 'Samurai', 'School', 'Sci-Fi', 
		'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 
		'Space', 'Sports', 'Super Power', 'Supernatural', 
		'Vampire', 'Yaoi', 'Yuri']

def parser(url, root):
	sauce = requests.get(url)
	plaintxt = sauce.text
	soup = BeautifulSoup(plaintxt, 'html.parser')
	
	score = soup.find(title="indicates a weighted score. Please note that 'Not yet aired' titles are excluded.").text
	synop = soup.find(itemprop='description').text
	
	output_frame = Frame(root)
	output_frame.pack()

	label1 = Label(output_frame, text='Score')
	label1.grid(row=1, column=1, padx=30, pady=30)

	label2 = Label(output_frame, text=score)
	label2.grid(row=1, column=2, padx=30, pady=30)

	label3 = Label(output_frame, text='Synopsis')
	label3.grid(row=2, column=1, padx=30, pady=30)

	synop_frame = Frame(output_frame)
	synop_frame.grid(row=2, column=2, padx=30, rowspan=3, columnspan=4)
	Y_S = Scrollbar(synop_frame)
	T = Text(synop_frame, height=4, width=50)
	Y_S.pack(side=RIGHT, fill=Y)
	T.pack(side=LEFT, fill=Y)
	Y_S.config(command=T.yview)
	T.config(yscrollcommand=Y_S.set)
	T.insert(END, synop)

	label4 = Label(output_frame, text='Genre')
	label4.grid(row=6, column=1, padx=30, pady=30)

	genre_frame = Frame(output_frame)
	genre_frame.grid(row=6, column=2, padx=30, rowspan=1, columnspan=4)
	Y_S = Scrollbar(genre_frame)
	T = Text(genre_frame, height=4, width=50)
	Y_S.pack(side=RIGHT, fill=Y)
	T.pack(side=LEFT, fill=Y)
	Y_S.config(command=T.yview)
	T.config(yscrollcommand=Y_S.set)

	for genre in soup.findAll(title=genres):
		anime = genre.get('title')
		T.insert(END, anime)
		T.insert(END, ' ')

	label4 = Label(output_frame, text='User Recs')
	label4.grid(row=8, column=1, padx=30, pady=30)

	recs_frame = Frame(output_frame)
	recs_frame.grid(row=8, column=2, padx=30, rowspan=4, columnspan=4)
	Y_S = Scrollbar(recs_frame)
	T = Text(recs_frame, height=4, width=50)
	Y_S.pack(side=RIGHT, fill=Y)
	T.pack(side=LEFT, fill=Y)
	Y_S.config(command=T.yview)
	T.config(yscrollcommand=Y_S.set)

	for recs in soup.findAll('li', {'class':'btn-anime'}):
		anime = recs.get('title')
		T.insert(END, anime)
		T.insert(END, '\n')

	def back():
		output_frame.destroy()
		get_link(root)


	btn = Button(output_frame, text='Back', command=back)
	btn.grid(row=1, column=5, pady=30)

def get_link(root):
	input_frame = Frame(root)
	input_frame.pack()

	label = Label(input_frame, text='Input URL:')
	label.grid(row=1, column=1, columnspan=2, padx=30, pady=30)

	link_ent = Entry(input_frame, width=50)
	link_ent.grid(row=1, column=3, padx=30, pady=30, columnspan=2)

	def link():
		global root
		link = link_ent.get()
		input_frame.destroy()
		parser(link, root)

	btn =  Button(input_frame, text='ENTER', command=link)
	btn.grid(row=2, column=3, pady=30)

root  = Tk()
root.title('MAL Crawler')
#root.geometry("640x480+100+100")
link = get_link(root)
root.mainloop()
