import requests
import re
import json
import os
import sys
from urllib.request import urlretrieve
from urllib.error import ContentTooShortError
from bs4 import BeautifulSoup


class FlickrAlbumDownloader:
    FLICKR_URL = "https://www.flickr.com"
    DEFAULT_PATH = "./download_img"

    def __init__(self):
        self.albums = list()

    def set_URL(self, url):
        self.album_url = url

    def parse_all_imgs(self):
        raw_html = self.__request_raw_html(self.album_url)
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
                self.other_pages_url.append(
                    FlickrAlbumDownloader.FLICKR_URL +
                    a["href"])
        except Exception:
            # exist only one page
            self.other_pages_url = list()

    def __parse_title_and_url(self, html):
        m = re.search("Y.listData = (?P<img_infos>{[\S\s]*?});", html)
        listData = json.loads(m.group("img_infos"))
        for rows in listData["rows"]:
            for row in rows["row"]:

                if 'o' in row["sizes"]:
                    image_size = 'o'
                elif 'l' in row["sizes"]:
                    image_size = 'l'
                elif 'm' in row["sizes"]:
                    image_size = 'm'
                elif 's' in row["sizes"]:
                    image_size = 's'
                else:
                    print('Error: No image file.')
                    continue

                origin_size_url = row["sizes"][image_size]["url"]
                self.albums.append(
                    {"full_name": row["full_name"], "url": origin_size_url,
                     "file_extension":
                     self.__match_file_extension(origin_size_url)})

    def __match_file_extension(self, url):
        m = re.search("\.([a-zA-Z]*)$", url)
        return m.groups()[0]

    def set_export_directory(self, path=None):
        if path:
            self.path = path
        else:
            self.path = FlickrAlbumDownloader.DEFAULT_PATH

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print("Create a directoty {}".format(self.path))

    def download_all_img(self, reporthook=None):
        if not reporthook:
            reporthook = FlickrAlbumDownloader.__reporthook

        self.is_success_download = True
        self.fail_imgs = list()
        for index, img in enumerate(self.albums):
            try:
                print("%d/%d Download %s" %
                      (index+1, len(self.albums), img["full_name"]))

                full_file_name = img["full_name"]+"."+img["file_extension"]
                full_path = self.path+"/"+full_file_name
                self.__download(img["url"], full_path, reporthook)
            except ContentTooShortError:
                self.fail_imgs.append({"name": img["full_name"], "url": img["url"]})
                self.is_success_download = False

    @staticmethod
    def __reporthook(block_num, block_size, total_size):
        current_progress = block_num * block_size

        if total_size > 0:
            try:
                percent = min((current_progress*100)/total_size, 100)
            except Exception:
                percent = 100

            s = "\r%5.1f%% %*d/%d" % (percent,
                                      len(str(total_size)),
                current_progress,
                total_size)
            sys.stderr.write(s)
            if current_progress > total_size:
                sys.stderr.write("\n")
        else:
            sys.stderr.write("Read %d\n" % (current_progress,))

    # TODO: option to overwrite duplicate file
    def __download(self, url, path, reporthook):
        if not os.path.exists(path):
            urlretrieve(url, path, reporthook=reporthook)
        else:
            print("File Exist")

    def get_albums(self):
        return self.albums

    def get_img_num(self):
        return len(self.albums)

    def get_fail_imgs(self):
        return self.fail_imgs


if __name__ == '__main__':
    album_url = input("Please input url of your flickr album: ")
    path = input("Input save path: ")

    f = FlickrAlbumDownloader()
    f.set_URL(album_url)
    f.parse_all_imgs()
    f.set_export_directory(path)
    f.download_all_img()
    print("Finish")

    if not f.is_success_download:
        print("Fail to download images below.")
        for f in f.get_fail_imgs():
            print(f["full_name"], f["url"])
