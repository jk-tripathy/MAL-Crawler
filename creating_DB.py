from tkinter import *
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import requests
import pickle
from anime_class import anime_details


genres = ['Action', 'Adventure', 'Cars', 'Comedy', 
		'Demons', 'Drama', 'Ecchi', 'Fantasy',
		'Harem', 'Hentai', 'Historical', 'Horror'
		'Kids', 'Magic', 'Martial Arts', 'Mecha',
		'Music', 'Mystery', 'Parody', 'Police',
		'Romance', 'Samurai', 'School', 'Sci-Fi', 
		'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 
		'Space', 'Sports', 'Super Power', 'Supernatural', 
		'Vampire', 'Yaoi', 'Yuri']

def  link_grabber(file, pages):
	count = 1
	while count<=pages:
		sauce = requests.get('https://myanimelist.net/topanime.php?limit={}'.format((count-1)*50))
		plaintxt = sauce.text
		soup = BeautifulSoup(plaintxt, 'html.parser')

		for rank_list in soup.findAll('tr', {'class':'ranking-list'}):
			for title_class in rank_list.findAll('td', {'class':'title al va-t word-break'}):
				id_class = title_class.find('div', {'class':'di-ib clearfix'})
				title = id_class.find('a')
				title_text = title.getText()
				#print(title_text)
				title_link = title.get('href')
				#print(title_link)
				try:
					file.write(str(title_link))
					file.write('\n')
				except UnicodeEncodeError:
					print('{} cannot be formatted properly'. format(title_link))
		count +=1
		
def parser(url, animes):
	sauce = requests.get(url)
	plaintxt = sauce.text
	soup = BeautifulSoup(plaintxt, 'html.parser')
	
	for div in soup.findAll('div', {'id':'contentWrapper'}):
		title = div.find('span', {'itemprop':'name'}).text
	
	score = soup.find(title="indicates a weighted score. Please note that 'Not yet aired' titles are excluded.").text
	synop = soup.find(itemprop='description').text

	for genre in soup.findAll(title=genres):
		anime_genre = genre.get('title')
		#print(anime_genre)

	for recs in soup.findAll('li', {'class':'btn-anime'}):
		user_recs = recs.get('title')
		#print(user_recs)

	anime_rank = soup.find('span', {'class':'numbers ranked'}).text
	print("{} anime is done". format(anime_rank))
	try:
		anime = anime_details(title, score, synop, anime_genre, user_recs, anime_rank)
		animes.append(anime)
	except UnboundLocalError:
		print("{} is skipped due to missing data". format(title))
	
	

def run():
	
	links_file = open('links.txt', 'w')
	link_grabber(links_file, 5)
	links_file.close()
	
	animes = []

	links = open('links.txt', 'r')
	for url in links.readlines():
		parser(url, animes)
	links.close()
	
	print("completed parsing")

	with open("DB.file", "wb") as f:
		pickle.dump(animes, f, pickle.HIGHEST_PROTOCOL)
	

if __name__ == '__main__':
	run()