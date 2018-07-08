from tkinter import *
from bs4 import BeautifulSoup
import requests
import pickle
from anime_class import anime_details


completion_count = 1

genres = ['Action', 'Adventure', 'Cars', 'Comedy', 
		'Demons', 'Drama', 'Ecchi', 'Fantasy',
		'Harem', 'Hentai', 'Historical', 'Horror'
		'Kids', 'Magic', 'Martial Arts', 'Mecha',
		'Music', 'Mystery', 'Parody', 'Police',
		'Romance', 'Samurai', 'School', 'Sci-Fi', 
		'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 
		'Space', 'Sports', 'Super Power', 'Supernatural', 
		'Vampire', 'Yaoi', 'Yuri']

class links:
	def __init__(self, anime_link):
		self.anime_link = anime_link

def  link_grabber(all_links, page_start, page_end):
	count = page_start-1
	while count < page_end:
		sauce = requests.get('https://myanimelist.net/topanime.php?limit={}'.format((count)*50))
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
				l = links(title_link.encode('utf-8'))
				all_links.append(l)
		print('page {} links grabbed'.format(count+1))
		count +=1
	
		
def parser(url, animes, total):
	global count
	global completion_count
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
	print("{}/{} parsed". format(completion_count, total))
	completion_count += 1
	try:
		anime = anime_details(title, score, synop, anime_genre, user_recs, anime_rank)
		animes.append(anime)
	except UnboundLocalError:
		print("{} is skipped due to missing data". format(title.decode('utf-8')))
	
	

def run():
	animes = []
	try:
		with open('DB.file', 'rb') as f:
			animes = pickle.load(f)
			length = len(animes)
			print('there are curently {} anime in DB'.format(length))
	except FileNotFoundError:
		print('DB not yet created')

	start, end = map(int,input('Start page, End Page: ').split())
	print('Starting link grabber...')
	with open('Links_file.txt', 'ab+') as f:
		all_links = []
		link_grabber(all_links, start, end)
		print('You have grabbed {} links'.format(len(all_links)))
		for link in all_links:
			f.write(link.anime_link)
			f.write('\n'.encode('utf-8'))

	tot = len(all_links)
	for link in all_links:
		parser(link.anime_link, animes, tot)
	
	print("completed parsing")
	
	with open("DB.file", "wb") as f:
		pickle.dump(animes, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
	run()