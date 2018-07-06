import pickle
from anime_class import anime_details

if __name__ == '__main__':
	with open("DB.file", "rb") as f:
		dump = pickle.load(f)

	for anime in dump:
		print(anime.rank)
		print(anime.name)