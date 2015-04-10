import requests
import re
import json
import urllib
import os
from bs4 import BeautifulSoup


class FlickAlbumDownloader:
    FLICKR_URL = "https://www.flickr.com"

    def __init__(self):
        self.albums = list()

    def set_URL(self, url):
        self.url = url

    def parse_all_imgs(self):
        raw_html = self.__request_raw_html(self.url)
        self.__parse_other_pages_url(raw_html)
        self.__parse_title_and_src(raw_html)

        for url in self.other_pages_url:
            raw_html = self.__request_raw_html(url)
            self.__parse_title_and_src(raw_html)

    def __request_raw_html(self, url):
        req = requests.get(url)
        return req.text

    def __parse_other_pages_url(self, html):
        self.other_pages_url = list()

        soup = BeautifulSoup(html)
        for a in soup.find('span', {'class': 'pages'}).find_all('a', href=True):
            self.other_pages_url.append(FlickAlbumDownloader.FLICKR_URL+a["href"])

    def __parse_title_and_src(self, html):
        m = re.findall("Y.listData = {[\S\s]*try", html)
        listData = json.loads(m[0][13:-8])
        for rows in listData["rows"]:
            for row in rows["row"]:
                self.albums.append({"full_name": row["full_name"],
                                    "src": row["src"]})

    def get_albums(self):
        return self.albums

    def set_export_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print("Create a directoty {}".format(path))

    def download_all_img(self, path="./download_img"):
        self.set_export_directory(path)

        for img in self.albums:
            print("Download %s" % img["full_name"])
            self.__download(img["src"], path+"/"+img["full_name"]+".jpg")

    def __download(self, url, path):
        urllib.request.urlretrieve(url, path)


if __name__ == '__main__':
    url = input("Please input url of your flickr album: ")
    f = FlickAlbumDownloader()
    f.set_URL("url")
    f.parse_all_imgs()
    f.download_all_img()
    print("Finish")
