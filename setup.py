import sys
import os
from cx_Freeze import setup, Executable
import requests.certs

os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), "cacert.pem")

main_python_file = "./Downloader_GUI.py"
application_title = "Flickr Album One Click Download"
application_description = "Download Flickr album images for a ceratin url"

includes = []
excludes = []
packages = []
include_files = [(requests.certs.where(), 'cacert.pem')]
build_exe_options = {"includes": includes,
                     "excludes": excludes,
                     "packages": packages,
                     "include_files": include_files}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name=application_title,
    version="1.0",
    description=application_description,
    author="LeeW",
    author_email="cl87654321@gmail.com",
    url="http://lee-w.github.io/Flickr_Album_Downloader/",
    options={"build_exe":  build_exe_options},
    executables=[Executable(main_python_file, base=base)]
)
