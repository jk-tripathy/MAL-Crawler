from tkinter import *
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import requests


sauce = requests.get('https://myanimelist.net/topanime.php')
plaintxt = sauce.text
soup = BeautifulSoup(plaintxt, 'html.parser')

for rank_list in soup.findAll('tr', {'class':'ranking-list'}):
	for rank_ac in rank_list.findAll('td', {'class':'rank ac'}):
		rank = rank_ac.find('span')
		rank = rank.getText()
		print('Rank: {}'.format(rank))

	for title_class in rank_list.findAll('td', {'class':'title al va-t word-break'}):
		id_class = title_class.find('div', {'class':'di-ib clearfix'})
		title = id_class.find('a')
		title_text = title.getText()
		print(title_text)
		title_link = title.get('href')
		print(title_link)