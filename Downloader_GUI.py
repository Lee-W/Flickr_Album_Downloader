from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
# from tkinter.messagebox import askokcancel
from tkinter.filedialog import askdirectory

from Flickr_Album_Downloader import FlickrAlbumDownloader


class DownloaderGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(columnspan=2000)

        self.__create_widgets()

    def __create_widgets(self):
        self.key_label = Label(self, text="API Key")
        self.key_field = Entry(self, width=70)

        self.secret_label = Label(self, text="API Secret")
        self.secret_field = Entry(self, width=70)

        self.url_label = Label(self, text="Album URL: ")
        self.url_field = Entry(self, width=70)

        self.download_btn = Button(self, text="Download", command=self.__download_method)
        self.msg_label = Label(self)

        self.key_label.grid(row=0, column=0)
        self.key_field.grid(row=0, column=1)
        self.secret_label.grid(row=1, column=0)
        self.secret_field.grid(row=1, column=1)
        self.url_label.grid(row=2, column=0)
        self.url_field.grid(row=2, column=1)
        self.download_btn.grid(row=3, column=0)

    def __download_method(self):
        downloader = FlickrAlbumDownloader(self.key_field.get(), self.secret_field.get())
        self.msg_label.text = ""

        directory = askdirectory(parent=self.master,
                                 initialdir=".")

        if directory:
            downloader.set_export_directory(directory)
            downloader.download_album(self.url_field.get())

            # answer = askokcancel("Download Confirm",
            #                      "There are "+str(self.d.get_img_num())+" images.")
            # if answer:
            #     self.__download(directory)

        self.msg_label.text = "Successfully Downloaded"


if __name__ == '__main__':
    root = Tk()
    root.title("Flickr Album Downloader")
    app = DownloaderGUI(master=root)
    app.mainloop()
