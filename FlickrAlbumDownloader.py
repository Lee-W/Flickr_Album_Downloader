import json
import re
import os
import sys
from urllib.request import urlretrieve
from urllib.parse import urlparse

import flickrapi
from flickrapi.exceptions import FlickrError


class FlickrAlbumDownloader:
    DEFAULT_PATH = "./download_img"

    def __init__(self, key, secret):
        self._flickr = flickrapi.FlickrAPI(key, secret)
        self.album = list()
        self.__check_api_key()

    def __check_api_key(self):
        self._flickr.test.echo()

    def set_export_directory(self, path=None):
        if path:
            self._path = path
        else:
            self._path = FlickrAlbumDownloader.DEFAULT_PATH

        if not os.path.exists(self._path):
            os.makedirs(self._path)
            print("Create a directoty {}".format(self._path))

    def download_album(self, album_id, reporthook=None, callback=None):
        if not reporthook:
            reporthook = FlickrAlbumDownloader.__reporthook

        self.__get_album_list(album_id)
        photo_num = len(self.album)
        for index, photo in enumerate(self.album):
            photo_id = photo["id"]
            title = photo["title"]

            try:
                photo_size_info = self._flickr.photos.getSizes(
                    photo_id=photo_id, format="json"
                )
            except KeyboardInterrupt:
                print("Terminated by User")
            else:
                photo_size_info = json.loads(photo_size_info.decode("utf-8"))

                url = photo_size_info["sizes"]["size"][-1]["source"]
                file_extension = FlickrAlbumDownloader.__match_file_extension(url)
                full_path = os.path.join(self._path, title + "." + file_extension)

                try:
                    self.__download(url, full_path, reporthook)
                except FileExistsError:
                    print("%s Exist" % title)
                else:
                    print(
                        "%d/%d - %s Downloaded \n" % (index + 1, len(self.album), title)
                    )

                    if callback:
                        callback(title, index + 1, photo_num)

    @staticmethod
    def __reporthook(block_num, block_size, total_size):
        current_progress = block_num * block_size

        if total_size > 0:
            try:
                percent = min((current_progress * 100) / total_size, 100)
            except Exception:
                percent = 100

            s = "\r%5.1f%% %*d/%d" % (
                percent,
                len(str(total_size)),
                current_progress,
                total_size,
            )
            sys.stderr.write(s)
            if current_progress > total_size:
                sys.stderr.write("\n")
        else:
            sys.stderr.write("Read %d\n" % (current_progress,))

    def __get_album_list(self, album_id):
        self.album = list()
        for photo in self._flickr.walk_set(album_id):
            self.album.append(dict(photo.items()))

    @staticmethod
    def __match_file_extension(url):
        m = re.search(r"\.([a-zA-Z]*)$", url)
        return m.groups()[0]

    # TODO: option to overwrite duplicate file
    def __download(self, url, path, reporthook):
        if not os.path.exists(path):
            urlretrieve(url, path, reporthook=reporthook)
        else:
            raise FileExistsError

    @staticmethod
    def parse_id_from_url(album_url):
        return urlparse(album_url).path.split("/")[4]


def load_API_info(API_path):
    with open(API_path) as f:
        return json.load(f)


def main():
    API_path = input("Please input path to load API key and secret: ") or "API.json"
    API_info = load_API_info(API_path)

    try:
        fad = FlickrAlbumDownloader(API_info["key"], API_info["secret"])

        album_url = input("Please input album url: ")
    except FlickrError:
        print("Flickr API Key Error")
    except KeyboardInterrupt:
        print("Terminated by user")
    else:
        album_id = FlickrAlbumDownloader.parse_id_from_url(album_url)
        fad.set_export_directory()
        fad.download_album(album_id)


if __name__ == "__main__":
    main()
