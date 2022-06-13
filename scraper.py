import requests
from bs4 import BeautifulSoup
import string
import os
import shutil


def main():
    type_of_page, number_of_pages = user_input()
    base_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page2"
    for page in range(1, number_of_pages + 1):
        if page == 1:
            url = base_url
        else:
            url = base_url + f"&page={page}"
        main_page_soup = soup_creator(url)
        links = find_articles(main_page_soup, type_of_page)
        body_extractor(links, page)


#take user input and creates folders
def user_input():
    number_of_pages = int(input("Please type number of pages: "))
    type_of_page = input("Please enter the TYPE of articles: ")
    try:
        for i in range(1, number_of_pages + 1):
            if os.path.isdir(f"./Page_{i}"):
                shutil.rmtree(f"./Page_{i}")
            os.mkdir(f"Page_{i}")
    except FileExistsError:
        pass
    return type_of_page, number_of_pages


def soup_creator(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup


def find_articles(soup, type_of_page):
    links = []
    articles = soup.find_all("article")
    for article in articles:
        article_type = article.find("span", class_="c-meta__type").text
        if article_type == type_of_page:
            links.append(article.find("a").get("href"))
    return links


def body_extractor(links, page):
    # gets article body
    for link in links:
        article = requests.get("https://www.nature.com" + link)
        article_soup = BeautifulSoup(article.content, 'html.parser')
        body = article_soup.find('div', {'class': "c-article-body"}).text.strip("\n")
        print(body)

        # File_name
        title = article_soup.find("h1", class_="c-article-magazine-title").text.strip()
        file_name = ""
        for letter in title:
            if letter not in string.punctuation:
                file_name += letter
        file_name = file_name.replace(" ", "_") + ".txt"

        #Writing a file
        directory = f"/Users/Dmitry/PycharmProjects/Web Scraper/Web Scraper/task/Page_{page}"
        os.chdir(directory)

        file = open(file_name, 'wb')
        file.write(body.encode("utf-8"))
        file.close()
    print(f"Files for page {page} saved.")




if __name__ == "__main__":
    main()
