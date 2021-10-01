import codecs
import urllib.parse
import falcon
import threading
import frida
from werkzeug.serving import run_simple

script = None


# Обработка get-запросов и вызов метода frida-rpc
class SignClass:
    def on_get(self, req, resp):
        data = urllib.parse.unquote_plus(req.query_string)
        resp.body = urllib.parse.unquote(script.exports.getsecsign(data))


# Запуск http-сервера
def startServer():
    api = falcon.API()
    api.add_route('/getSign', SignClass())
    run_simple("0.0.0.0", 1234, api, threaded=True)


# Обработка сообщений из Frida
def on_message(message, data):
    if message["type"] == "send":
        msg = str(message["payload"])
        # Сообщение о готовности к запуску сервера
        if str(msg).__contains__("script loaded"):
            onScriptLoaded()
        print(msg)
    else:
        print(message)


def onScriptLoaded():
    threading.Thread(target=onScriptLoadedAsync,
                     args=()).start()


# Асинхронный запуск сервера
def onScriptLoadedAsync():
    startServer()


# Запуск приложения и внедрение скрипта testBox.js
device = frida.get_device_manager().get_usb_device()
pidmore = device.spawn(["ru.ryazantsev.blacktestbox"])
session = device.attach(pidmore)
with codecs.open("testBox.js", 'r', 'utf-8') as f:
    source = f.read()
script = session.create_script(source)
script.on('message', on_message)
script.load()
device.resume(pidmore)
input()
