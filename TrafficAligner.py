from utilites import log
from Downloader import Downloader
from CommandListener import CommandListener




def download_callback(params):
    downloader = Downloader(params['url'])
    downloader.start()

listenner = CommandListener('https://pressindex.ru/alignserver')
listenner.start()
listenner.download_callback = download_callback



