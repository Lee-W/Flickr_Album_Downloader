import os
import webbrowser
import pickle
from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
from tkinter import Checkbutton
from tkinter import IntVar
from tkinter.filedialog import askdirectory

from flickrapi.exceptions import FlickrError

from Flickr_Album_Downloader import FlickrAlbumDownloader


class DownloaderGUI(Frame):
    FLICKR_API_INFO_URL = "https://www.flickr.com/services/api/keys/"
    API_INFO_NAME = ".api.pkl"

    def __init__(self, master=None):
        self.to_remember = IntVar()

        Frame.__init__(self, master)
        self.master = master
        self.grid(columnspan=2000)

        self.msg_label = Label(self)

        self.__create_enter_api_widgets()
        self.__create_download_widgets()

        if os.path.isfile(DownloaderGUI.API_INFO_NAME):
            self.__load_api_info()
            self.__place_download_widgets()
        else:
            self.__place_enter_api_widgets()

    def __create_enter_api_widgets(self):
        self.key_label = Label(self, text="API Key")
        self.key_field = Entry(self, width=70)

        self.secret_label = Label(self, text="API Secret")
        self.secret_field = Entry(self, width=70)

        self.enter_btn = Button(self, text="Enter", command=self.__enter_method)

        self.api_link = Label(self, text="Find your API key and secret", fg="blue", cursor="hand2")
        self.api_link.bind("<Button-1>", self.__link_callback)

        self.remember_check = Checkbutton(self, text="Remember Info", variable=self.to_remember)

    def __create_download_widgets(self):
        self.url_label = Label(self, text="Album URL: ")
        self.url_field = Entry(self, width=70)

        self.download_btn = Button(self, text="Download", command=self.__download_method)
        self.reset_api_btn = Button(self, text="Reset API info", command=self.__reset_api_info_method)

    def __place_enter_api_widgets(self):
        self.key_label.grid(row=0, column=0)
        self.key_field.grid(row=0, column=1)
        self.secret_label.grid(row=1, column=0)
        self.secret_field.grid(row=1, column=1)
        self.enter_btn.grid(row=2, column=0)
        self.remember_check.grid(row=2, column=1)
        self.api_link.grid(row=3, column=1)

    def __place_download_widgets(self):
        self.url_label.grid(row=2, column=0)
        self.url_field.grid(row=2, column=1)
        self.download_btn.grid(row=3, column=0)
        self.reset_api_btn.grid(row=3, column=1)

    def __hide_enter_api_widgets(self):
        self.key_label.grid_remove()
        self.key_field.grid_remove()
        self.secret_label.grid_remove()
        self.secret_field.grid_remove()
        self.enter_btn.grid_remove()
        self.api_link.grid_remove()
        self.remember_check.grid_remove()
        self.msg_label.grid_remove()

    def __hide_download_widgets(self):
        self.url_field.grid_remove()
        self.url_label.grid_remove()
        self.download_btn.grid_remove()
        self.reset_api_btn.grid_remove()

    def __link_callback(self, event):
        webbrowser.open_new(DownloaderGUI.FLICKR_API_INFO_URL)

    def __enter_method(self):
        try:
            self.downloader = FlickrAlbumDownloader(self.key_field.get(), self.secret_field.get())
        except FlickrError:
            self.msg_label.text = "API Key Error"
            self.msg_label.grid(row=3, column=0)
        else:
            self.__hide_enter_api_widgets()
            self.__place_download_widgets()

            if self.to_remember.get():
                self.__save_api_info()

    def __save_api_info(self):
        api_info = {"key": self.key_field.get(), "secret": self.secret_field.get()}
        with open(DownloaderGUI.API_INFO_NAME, "wb") as f:
            pickle.dump(api_info, f)

    def __load_api_info(self):
        with open(DownloaderGUI.API_INFO_NAME, "rb") as f:
            api_info = pickle.load(f)
        self.downloader = FlickrAlbumDownloader(api_info['key'], api_info['secret'])

    def __remove_api_info(self):
        os.remove(DownloaderGUI.API_INFO_NAME)

    def __download_method(self):
        directory = askdirectory(parent=self.master,
                                 initialdir=".")

        if directory:
            self.downloader.set_export_directory(directory)
            album_id = FlickrAlbumDownloader.parse_id_from_url(self.url_field.get())
            self.downloader.download_album(album_id)

        self.msg_label.text = "Successfully Downloaded"
        self.msg_label.grid(row=4, column=0)

    def __reset_api_info_method(self):
        self.__remove_api_info()
        self.__hide_download_widgets()
        self.__place_enter_api_widgets()

        self.key_field.text = ""
        self.secret_field.text = ""
        self.to_remember.set(0)


if __name__ == '__main__':
    root = Tk()
    root.title("Flickr Album Downloader")
    app = DownloaderGUI(master=root)
    app.mainloop()
