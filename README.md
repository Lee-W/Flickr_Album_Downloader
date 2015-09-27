# Flickr Album Downloader
Download all the image in flickr albums of a given url
***It could only download a limited number of pictures***

# Requirements
requests
```sh
pip3 install -r requirements.txt
```

# USAGE
```sh
python3 Flickr_Album_Downloader.py
```
Input url as prompt ask.

# Build
These script are on branch GUI.

## Windows
```
python3 setup.py build
```

or

```
python3 setup.py bdist_msi
```

# Mac OSX
```
virtualenv --no-site-package env
sh fix_env_py2app.sh
source env/bin/activate
python3 setup-py2app.py py2app
```


# AUTHORS
[Lee-W](https://github.com/Lee-W/)

# LICENSE
MIT

