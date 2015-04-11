from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
from tkinter.messagebox import askokcancel
from tkinter.filedialog import askdirectory

from Flickr_Album_Downloader import FlickrAlbumDownloader


class DownloaderGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(columnspan=2000)

        self.__create_widgets()

    def __create_widgets(self):
        self.url_label = Label(self, text="Album URL: ")
        self.url_field = Entry(self, width=70)
        self.download_btn = Button(self, text="Download", command=self.__download_method)

        self.url_label.grid(row=0, column=0)
        self.url_field.grid(row=0, column=1)
        self.download_btn.grid(row=1, column=0)

    def __download_method(self):
        directory = askdirectory(parent=self.master,
                                 initialdir=".")

        if directory:
            d = FlickrAlbumDownloader()
            d.set_URL(self.url_field.get())
            d.parse_all_imgs()

            answer = askokcancel("Download Confirm",
                                 "There are "+str(d.get_img_num())+" images.")
            if answer:
                d.set_export_directory(directory)
                d.download_all_img()


if __name__ == '__main__':
    root = Tk()
    root.title("Flickr Album Downloader")
    app = DownloaderGUI(master=root)
    app.mainloop()
