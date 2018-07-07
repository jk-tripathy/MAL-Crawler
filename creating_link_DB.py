from tkinter import *
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

class anime_details:
	def __init__(self, name, score, synopsis, genre, user_recs, rank):
		self.name = name
		self.score = score
		self.synopsis = synopsis
		self.genre = genre
		self.user_recs = user_recs
		self.rank = rank
	def disp_data(self):
		print( "disp run ")
		print (self.name.encode('utf-8'),self.score.encode('utf-8'),self.synopsis.encode('utf-8'),
			self.genre.encode('utf-8'),self.user_recs.encode('utf-8'),self.rank.encode('utf-8'))

def  link_grabber(file):
	sauce = requests.get('https://myanimelist.net/topanime.php')
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
				file.write(title_link.encode('utf-8'))
				file.write('\n')
			except UnicodeEncodeError:
				print('{} cannot be formatted properly'. format(title_link))

def parser(url, animes):
	sauce = requests.get(url)
	plaintxt = sauce.text
	soup = BeautifulSoup(plaintxt, 'html.parser')

	for div in soup.findAll('div', {'id':'contentWrapper'}):
		title = div.find('span', {'itemprop':'name'}).text.encode('utf-8')

	score = soup.find(title="indicates a weighted score. Please note that 'Not yet aired' titles are excluded.").text
	synop = soup.find(itemprop='description').text

	for genre in soup.findAll(title=genres):
		anime_genre = genre.get('title')
		#print(anime_genre)

	for recs in soup.findAll('li', {'class':'btn-anime'}):
		user_recs = recs.get('title')
		#print(user_recs)

	anime_rank = soup.find('span', {'class':'numbers ranked'}).text
	print("{} anime are done". format(anime_rank))
	anime = anime_details(title, score, synop, anime_genre, user_recs, anime_rank)
	animes.append(anime)
	test=anime_details(title, score, synop, anime_genre, user_recs, anime_rank)
	print ("Running test object ")
	test.disp_data()


def run():
	links_file = open('links.txt', 'w')
	link_grabber(links_file)
	links_file.close()

	animes = []

	links = open('links.txt', 'r')
	for url in links.readlines():
		parser(url, animes)
	links.close()
	print("completed parsing")

	for anime in animes:
		print(anime.name)


if __name__ == '__main__':
	run()
