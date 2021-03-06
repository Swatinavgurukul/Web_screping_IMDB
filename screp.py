import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import os
import random
import time

URL = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"

# TASK-1

def scrap_to_tist():

    sample = requests.get(URL)
    soup = BeautifulSoup(sample.text, "html.parser")

    tbody = soup.find('tbody', class_="lister-list")
    # print tbody
    trs = tbody.findAll('tr')
    whole_data = []
    j = 0
    for i in trs:
        movies_data = {}
        position = j = j+1

        name = i.find('td', class_="titleColumn").a.get_text()
        # print name
        year = i.find('td', class_="titleColumn").span.get_text()
        # print year
        reng = i.find('td', class_="ratingColumn").get_text()
        # print reng
        link = i.find("a")
        # print link
        movie_link = "https://www.imdb.com/"+link["href"]
        # print movie_link
        movies_data["position"] = position
        movies_data["name"] = name
        movies_data["year"] = int(year[1:5])
        movies_data["reting"] = float(reng)
        movies_data["url"] = movie_link

        whole_data.append(movies_data)
    return whole_data


scrept = scrap_to_tist()
# pprint (scrept)

# Task - 2


def group_by_year(movies):

    years = []
    for i in movies:
        year = i["year"]
        if year not in years:
            years.append(year)

    movie_dict = {i: []for i in years}

    for i in movies:
        year = i["year"]
        for x in movie_dict:
            if str(x) == str(year):
                movie_dict[x].append(i)
    return movie_dict


year_wais = group_by_year(scrept)
pprint (year_wais)

# # TASK-3


def group_by_decade(movies):
    moviedec = {}
    list1 = []
    for index in movies:
        mod = index % 10
        # print mode
        decade = index-mod
        # print decade
        if decade not in list1:
            list1.append(decade)

    for i in list1:
        moviedec[i] = []
    for i in moviedec:
        drc10 = i+9
        for x in movies:
            if x <= drc10 and x >= i:
                for v in movies[x]:
                    moviedec[i].append(v)
    return (moviedec)


decade_movies = group_by_decade(year_wais)
# pprint (decade_movies)


# Task - 4
def scrape_top_list(movie_url):
    # print movie_url
    Id = movie_url.split("/")
    file_name_id = Id[5]
    # print file_name_id
    # Task - 8

    if os.path.exists("/home/pooja/web-screping-IMDB/IMDB-DATA/" + file_name_id + ".json"):
        file1 = open("/home/pooja/web-screping-IMDB/IMDB-DATA/" + file_name_id + ".json", "r")
        top_movies_read = file1.read()
        movies_lode = json.loads(top_movies_read)
        print ("file exists")
        return movies_lode

    else:
        print ("file not exsits")
        movies_data_scrape = {}
        sample = requests.get(movie_url)
        soup = BeautifulSoup(sample.text, "html.parser")

        movie_name = soup.find('h1', class_="").get_text().split("(")
        # return movie_name[0]

        movie_Directors = soup.find('div', class_="credit_summary_item")
        director_list = movie_Directors.findAll("a")
        director_name = []
        for i in director_list:
            director_name.append(i.get_text())
        # return director_name
        # return movie_Directors[0]

        movie_poster_link = soup.find("div", class_="poster").a["href"]
        movie_poster = "https://www.imdb.com"+movie_poster_link
        # return movie_poster

        movies_bio = soup.find("div", class_="summary_text").get_text().strip()
        # return movies_bio
        movie_genres1 = soup.find("div", class_="subtext")
        gener = movie_genres1.findAll("a")
        gener.pop()
        movie_gener = []
        for i in gener:
            movie_gener.append(i.get_text())
        # return movie_gener
        extra_details = soup.find(
            "div", attrs={"class": "article", "id": "titleDetails"})
        list_of_div = extra_details.find_all("div")
        for div in list_of_div:
            tag_h4 = div.find_all("h4")
            for text in tag_h4:
                if "Language:" in text:
                    tag_anchor = div.find_all("a")
                    movie_language = [language.get_text()
                                      for language in tag_anchor]
                elif "Country:" in text:
                    tag_anchor = div.find_all("a")
                    movie_country = "".join(
                        [country.get_text() for country in tag_anchor])
        # return movie_language
        # return movie_country

        movie_time = soup.find("div", class_="subtext")
        run_time = movie_time.find("time").get_text().strip()
        run_time_hours = int(run_time[0])*60
        run_minuts = 0
        if 'min' in run_time:
            run_minuts = int(run_time[3:].strip("min"))
            movie_runtime = run_time_hours + run_minuts
        else:
            movie_runtime = run_time_hours
        # # return movie_runtime

        movies_data_scrape["name"] = movie_name[0]
        movies_data_scrape["director"] = director_name
        movies_data_scrape["country"] = movie_country
        movies_data_scrape["language"] = movie_language
        movies_data_scrape["poster_image_url"] = movie_poster
        movies_data_scrape["bio"] = (movies_bio)
        movies_data_scrape["runtime"] = movie_runtime
        movies_data_scrape["genre"] = movie_gener

        with open("/home/pooja/web-screping-IMDB/IMDB-DATA/" + file_name_id + ".json", "w") as file1:
            file1.write(json.dumps(movies_data_scrape, file1))

        return movies_data_scrape


# url = scrept[0]['url']
# print url
# movie_top_list=scrape_top_list(url)
# print movie_top_list

# Task-5
def get_movie_list_details(movies_list):
    movie_10_list = []
    random_sleep=random.randint(1,3)
    # print random_sleep
    time.sleep(random_sleep)
    for i in scrept[:250]:
        url = i['url']
        movieDetails = scrape_top_list(url)
        # print movieDetails
        movie_10_list.append(movieDetails)
    return movie_10_list


storage = get_movie_list_details(scrept)
pprint(storage)

# task-6


def analyse_movies_language(movies_language_list):
    movie_language_details = {}

    for movie_name in movies_language_list:

        if movie_name not in movie_language_details:

            movie_language_details[movie_name] = 1
        else:
            movie_language_details[movie_name] += 1

    return movie_language_details


movie_languages = []
for storage_language in storage:
    languages = storage_language["language"]
    # print languages
    movie_languages.extend(languages)
# print movie_languages
movies_language_count = analyse_movies_language(movie_languages)
# print movies_language_count

# #Task 7


def analyse_movies_director(movies_director_list):
    movie_director_details = {}

    for movie_director in movies_director_list:

        if movie_director not in movie_director_details:

            movie_director_details[movie_director] = 1
        else:
            movie_director_details[movie_director] += 1

    return movie_director_details


movie_director = []
for storage_director in storage:
    directors = storage_director["director"]
    movie_director.extend(directors)
# print movie_director
movies_director_count = analyse_movies_director(movie_director)
# print movies_director_count
