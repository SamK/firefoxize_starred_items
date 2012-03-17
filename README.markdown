# firefoxize_starred_items.py

This script permits to convert your starred items in Google Reader into bookmarks for Firefox.

This script is usable as an executable or as a Python module.

## Download

You first have to download the script:

    wget https://github.com/samyboy/firefoxize_starred_items/tarball/master

Extract the content

    tar xvzf samyboy-firefoxize_starred_items*.tar.gz
    cd samyboy-firefoxize_starred_items*.tar.gz

### Install as command line script

If used in command line, argparse is required.

Under Debian/Ubuntu:
    $ sudo apt-get install python-argparse

Set the script executable
    chmod +x samyboy-firefoxize_starred_items.py

### Command line usage:

Basic usage:

    ./samyboy-firefoxize_starred_items.py starred-items.json
The script will produce a html file which you can import in Firefox.

The available options are available with the --help switch:

$ ./firefoxize_starred_items.py --help
usage: firefoxize_starred_items.py [-h] [-v] [-q] [-V] [-s] [-o outfile.html]
                                   filename.json

Process some integers.

positional arguments:
  filename.json         The input JSON filename

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose output
  -q, --quiet           quiet output
  -V, --version         shows program version
  -s, --subfolders      Sort items into folders
  -o outfile.html, --output outfile.html
                        determine output file. default is ./The input JSON
                        filename.html


### Python module usage

Todo...
