#!/usr/bin/env python2.7
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from selenium import webdriver
import SimpleHTTPServer
import SocketServer
import threading
import time
import sys


def upHttpServer(port):
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        '.webapp': 'application/x-web-app-manifest+json',
    })
    return SocketServer.TCPServer(("", int(port)), Handler)


def getBrowserDrive():
    return webdriver.Firefox()


class Watch(FileSystemEventHandler):
    def on_modified(self, event):
        browser.refresh()


def startMonitor(path, recursive=False):
    event_handler = Watch()
    observer = Observer()
    observer.schedule(event_handler, path, False)
    observer.start()


def keepAlive():
    while True:
        time.sleep(0.5)

domain = sys.argv[1]
port = sys.argv[2]
uri = sys.argv[3]
path = sys.argv[4]
url = domain + ":" + port + uri

browser = getBrowserDrive()
webserver = upHttpServer(port)
threading.Thread(target=webserver.serve_forever).start()
browser.get(url)
startMonitor('.')
threading.Thread(target=keepAlive).start()
