import requests
import pandas as pd

url_film_series = 'https://en.wikipedia.org/wiki/Film_series'
response = requests.get(url_film_series)


film_series = pd.read_html(response.text)[0]
#print(film_series.columns)

# for franchise in film_series['Franchise']:
#   print(franchise)

franchises = film_series[['Franchise']]
franchises.columns = ['nome']

franchises.to_csv('data/Franquia.csv', index=False, encoding='utf-8')