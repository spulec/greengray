from ftplib import FTP
import os
import zipfile

import StringIO
import sys
import requests
from lxml import etree

URL = 'http://www2.sos.state.oh.us/pls/voter/f?p=111:1'

FTP_SERVER = "sosftp.sos.state.oh.us"
ftp = FTP(FTP_SERVER)
ftp.login()

def main():
    res = requests.get(URL)
    root = etree.parse(StringIO.StringIO(res.content), etree.HTMLParser()).getroot()
    data_file_urls = [url for url in root.xpath("//tr/td/a/@href") if url.startswith("ftp:")]
    for data_file_url in data_file_urls:
        data_file_url = data_file_url.split(FTP_SERVER)[1]
        output_file = "data/" + data_file_url.split("/")[-1]
        fhandle = open(output_file, 'wb')
        print 'Getting ' + data_file_url
        ftp.retrbinary('RETR ' + data_file_url, fhandle.write)
        fhandle.close()

        zfile = zipfile.ZipFile(output_file)
        zfile.extractall("data/")
        os.remove(output_file)


if __name__ == '__main__':
    main()
