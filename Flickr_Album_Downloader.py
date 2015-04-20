import requests
import re
import json
import os
import wget
from bs4 import BeautifulSoup


class FlickrAlbumDownloader:
    FLICKR_URL = "https://www.flickr.com"
    DEFAULT_PATH = "./download_img"

    def __init__(self):
        self.albums = list()

    def set_URL(self, url):
        self.url = url

    def parse_all_imgs(self):
        raw_html = self.__request_raw_html(self.url)
        self.__parse_title_and_url(raw_html)

        self.__parse_other_pages_url(raw_html)
        for url in self.other_pages_url:
            raw_html = self.__request_raw_html(url)
            self.__parse_title_and_url(raw_html)

    def __request_raw_html(self, url):
        req = requests.get(url)
        return req.text

    def __parse_other_pages_url(self, html):
        self.other_pages_url = list()

        try:
            soup = BeautifulSoup(html)
            for a in soup.find('span', {'class': 'pages'}).find_all('a', href=True):
                self.other_pages_url.append(FlickrAlbumDownloader.FLICKR_URL+a["href"])
        except Exception:
            # exist only one page
            self.other_pages_url = list()

    # TODO: refactor
    def __parse_title_and_url(self, html):
        m = re.findall("Y.listData = {[\S\s]*try", html)
        listData = json.loads(m[0][13:-8])
        for rows in listData["rows"]:
            for row in rows["row"]:
                origin_size_url = row["sizes"]["o"]["url"]
                self.albums.append({"full_name": row["full_name"],
                                    "url": origin_size_url,
                                    "file_extension": self.__match_file_extension(origin_size_url)})

    def __match_file_extension(self, url):
        m = re.search("\.([a-zA-Z]*)$", url)
        return m.groups()[0]

    def set_export_directory(self, path):
        if not path:
            self.path = FlickrAlbumDownloader.DEFAULT_PATH

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print("Create a directoty {}".format(self.path))

    def download_all_img(self, path=None):
        self.set_export_directory(path)

        for index, img in enumerate(self.albums):
            print("%d/%d Download %s" % (index+1, len(self.albums), img["full_name"]))
            full_file_name = img["full_name"]+"."+img["file_extension"]
            self.__download(img["url"], self.path+"/"+full_file_name)

    def __download(self, url, path):
        wget.download(url, path)
        print()

    def get_albums(self):
        return self.albums

    def get_img_num(self):
        return len(self.albums)


if __name__ == '__main__':
    url = input("Please input url of your flickr album: ")
    path = input("Input save path")
    f = FlickrAlbumDownloader()
    f.set_URL(url)
    f.set_export_directory(path)
    f.parse_all_imgs()
    f.download_all_img()
    print("Finish")
