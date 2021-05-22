import os
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://www.imdb.com/chart/top'

SAVE_FOLDER = 'images'

def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())
    movietags = soup.select('td.titleColumn')
    inner_movietags = soup.select('td.titleColumn a')
    ratingtags = soup.select('td.posterColumn span[name=ir]')
    imagelinks = soup.select('td.posterColumn img')
    
    
    def get_year(movie_tag):
        moviesplit = movie_tag.text.split()
        year = moviesplit[-1]
        return year
        
    years = [get_year(tag) for tag in movietags]
    actors_list = [tag['title'] for tag in inner_movietags]
    titles = [tag.text for tag in inner_movietags]
    ratings = [float(tag['data-value']) for tag in ratingtags]
    images = [tag['src'] for tag in imagelinks]
    
    
    n_movies = len(titles)
    
    df = pd.DataFrame(columns = ['Title', 'Actors', 'Year', 'Rating', 'Image'])
    df.Title = titles
    df.Actors = actors_list
    df.Year = years
    df.Rating = ratings
    
    df.to_csv('movie.csv')
    
    for i, imagelink in enumerate(images):
        response = requests.get(imagelink)
        imagename = SAVE_FOLDER + '/' + titles[i] + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)
    
    
    
if __name__ == '__main__':
    main()