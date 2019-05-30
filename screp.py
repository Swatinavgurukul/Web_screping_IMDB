import requests
import bs4
import pprint
res=requests.get("https://www.imdb.com/india/top-rated-indian-movies/").text
# print res
soup = bs4.BeautifulSoup(res,'lxml')
# print soup
tbody=soup.find('tbody',{'class':'lister-list'})
trs=tbody.findAll('tr')
movie_data_list=[]
def scrape_top_list():
    for i in trs:
        movie_data={}
        name=i.find('td',{'class':'titleColumn'})
        movie_name=name.a.get_text()
        position = name.get_text().split()
        movie_position = position[0]
        movie_year=name.span.get_text()[1:5]
        link = i.find("a")
        movie_url = "https://www.imdb.com"+link['href']
        movie_rating=i.find('td',{'class':'ratingColumn imdbRating'}).get_text()
        movie_data["name"]=movie_name
        movie_data["year"]=movie_year
        movie_data["position"]=movie_position
        movie_data["url"]=movie_url
        movie_data["rating"]=movie_rating
        movie_data_list.append(movie_data)
    return movie_data_list
data=scrape_top_list()
pprint.pprint(scrape_top_list())



