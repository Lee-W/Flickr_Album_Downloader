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
        self.d = FlickrAlbumDownloader()

        self.__create_widgets()

    def __create_widgets(self):
        self.url_label = Label(self, text="Album URL: ")
        self.url_field = Entry(self, width=70)
        self.download_btn = Button(self, text="Download", command=self.__download_method)
        self.msg_label = Label(self)

        self.url_label.grid(row=0, column=0)
        self.url_field.grid(row=0, column=1)
        self.download_btn.grid(row=1, column=0)

    def __download_method(self):
        self.msg_label.grid_remove()

        directory = askdirectory(parent=self.master,
                                 initialdir=".")

        if directory:
            self.d.set_URL(self.url_field.get())
            self.d.parse_all_imgs()

            answer = askokcancel("Download Confirm",
                                 "There are "+str(self.d.get_img_num())+" images.")
            if answer:
                self.__download(directory)

    def __download(self, path):
        self.d.set_export_directory(path)
        self.d.download_all_img()

        if self.d.is_success_download:
            msg = "Success"
        else:
            msg = "The following images are not failed to download.\n"
            for fail_img in self.d.get_fail_imgs():
                msg += fail_img["name"]+"\t"+fail_img["url"]+"\n"

        self.msg_label['text'] = msg
        self.msg_label.grid(row=2, column=0)


if __name__ == '__main__':
    root = Tk()
    root.title("Flickr Album Downloader")
    app = DownloaderGUI(master=root)
    app.mainloop()
