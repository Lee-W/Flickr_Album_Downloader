from setuptools import setup

main_python_file = "./Downloader_GUI.py"
application_title = "Flickr Album One Click Download"
application_description = "Download Flickr ablum images for a certain url"

includes = []
excludes = []
packages = []
include_files = []
build_exe_options = {"includes": includes,
                     "excludes": excludes,
                     "packages": packages,
                     "include_files": include_files}

setup(
    app=[main_python_file],
    setup_requires=["py2app"],
    name=application_title,
    version="1.0",
    description=application_description,
    author="LeeW",
    author_email="cl87654321@gmail.com",
    url="https://github.com/Lee-W/repo",
    options={
        "build_exe":  build_exe_options,
        'py2app': {
          'packages': ['requests']
        }
    },
)
