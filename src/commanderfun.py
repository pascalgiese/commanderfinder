import os
import PySimpleGUI as sg
import pyperclip
import requests
import urllib.request
from pyedhrec import EDHRec
import time
import json
from PIL import Image


url_find = 'https://api.scryfall.com/cards/search'
url_random = 'https://api.scryfall.com/cards/random'
edhrec = EDHRec()
cmdname = []

layout = [[sg.Text("Find your commander: ")], [sg.InputText("", key="cmdName"), sg.Checkbox("Red", key="Red"), sg.Checkbox("Blue", key="Blue"), sg.Checkbox("Green", key="Green"), sg.Checkbox("White", key="White"), sg.Checkbox("Black", key="Black")], [sg.Button('Find', key='-FIND-'), sg.Button("Randomize", key='-RANDOMIZE-'), sg.Button("Exit", key='-EXIT-')]]

window = sg.Window("Commander Finder", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, '-EXIT-'):
        if save_name:
            os.remove(save_name)
        break

    cmdColors = []
    cmdColorsChecks = []
    paramsPayload = []

    if values['Red']:
        cmdColors.insert(0, 'R')
    if values['Blue']:
        cmdColors.insert(0, 'U')
    if values['Green']:
        cmdColors.insert(0, 'G')
    if values['White']:
        cmdColors.insert(0, 'W')
    if values['Black']:
        cmdColors.insert(0, 'B')

    if values['cmdName']:
        cmdname.insert(0, values['cmdName'])

    if event == '-FIND-':

        if cmdColors:
            paramsPayload = {"q": cmdname[0] + ' ' + 'c:' + str(cmdColors).replace("[", "").replace("]", "").replace(",","").replace("'","").replace("'", "").replace(" ", "") + ' ' + 'is:commander'}
        elif not cmdColors:
            paramsPayload = {"q": cmdname[0] + ' ' + 'is:commander'}

        cards = requests.get(url_find, params=paramsPayload)

        if cards.status_code == 200:

            # load commander image
            image = []
            commander = json.loads(cards.text)
            clearcmdname = str(commander['data'][0]['name'])
            cardImage = str(commander['data'][0]['image_uris']['png'])
            save_name = 'commanderimage.png'
            urllib.request.urlretrieve(cardImage, save_name)

            # resize image
            image_maxwidth = 400
            image_maxheight = 600
            ratio = min(image_maxwidth / 745, image_maxheight/1040)
            resize_width = 745 * ratio
            resize_height = 1040 * ratio
            resizeImage = Image.open(save_name)
            resizeImage.thumbnail(( int(resize_width), int(resize_height)), Image.Resampling.LANCZOS)
            resizeImage.save(save_name, "PNG")
            image.append(sg.Image(save_name))

            layout = [[sg.Text("Find your commander: ")], [sg.InputText("", key="cmdName"), sg.Checkbox("Red", key="Red"), sg.Checkbox("Blue", key="Blue"), sg.Checkbox("Green", key="Green"), sg.Checkbox("White", key="White"), sg.Checkbox("Black", key="Black")], [image], [sg.Button('Find', key='-FIND-'), sg.Button('Get Deck', key='-DECK-'), sg.Button("Randomize", key='-RANDOMIZE-'), sg.Button("Exit", key='-EXIT-')]]
            window1 = sg.Window("Commander Finder", layout)
            window.close()
            window = window1

        if cards.status_code == 404:
            sg.popup("Keine Karte gefunden, die den Suchparametern entspricht.")

    time.sleep(0.1)

    if event == '-RANDOMIZE-':

        paramsPayload = {'q': 'c:' + str(cmdColors).replace("[", "").replace("]", "").replace(",", "").replace("'", "").replace("'", "").replace(" ", "") + ' ' + 'is:commander'}
        cards = requests.get(url_random, params=paramsPayload)

        if cards.status_code == 200:

            # load commander image
            image = []
            commander = json.loads(cards.text)
            clearcmdname = str(commander["name"])
            cardImage = str(commander['image_uris']['png'])
            save_name = 'commanderimage.png'
            urllib.request.urlretrieve(cardImage, save_name)

            # resize image
            image_maxwidth = 400
            image_maxheight = 600
            ratio = min(image_maxwidth / 745, image_maxheight/1040)
            resize_width = 745 * ratio
            resize_height = 1040 * ratio
            resizeImage = Image.open(save_name)
            resizeImage.thumbnail(( int(resize_width), int(resize_height)), Image.Resampling.LANCZOS)
            resizeImage.save(save_name, "PNG")
            image.append(sg.Image(save_name))

            layout = [[sg.Text("Find your commander: ")], [sg.InputText("", key="cmdName"), sg.Checkbox("Red", key="Red"), sg.Checkbox("Blue", key="Blue"), sg.Checkbox("Green", key="Green"), sg.Checkbox("White", key="White"), sg.Checkbox("Black", key="Black")], [image], [sg.Button('Find', key='-FIND-'), sg.Button('Get Deck', key='-DECK-'), sg.Button("Randomize", key='-RANDOMIZE-'), sg.Button("Exit", key='-EXIT-')]]
            window1 = sg.Window("Commander Finder", layout, finalize=True)
            window.close()
            window = window1

            if cmdColors:
                for i in cmdColors:
                    match i:
                        case 'R':
                            window["Red"].update(value=True)
                        case 'U':
                            window["Blue"].update(value=True)
                        case 'G':
                            window["Green"].update(value=True)
                        case 'W':
                            window["White"].update(value=True)
                        case 'B':
                            window["Black"].update(value=True)

        if cards.status_code == 404:
            sg.popup("Keine Karte gefunden, die den Suchparametern entspricht.")

    time.sleep(0.1)

    if event == '-DECK-':
        deck = edhrec.get_commanders_average_deck(clearcmdname)
        decklist_list = deck['decklist']
        decklist = ''
        for i in decklist_list:
            decklist += i + '\n'
        pyperclip.copy(decklist)
        time.sleep(0.1)