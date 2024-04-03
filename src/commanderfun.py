import os
import re
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

layout = [[sg.Text("Find your commander: ")], [sg.InputText("", key="cmdName"), sg.Checkbox("Red", key="Red"), sg.Checkbox("Blue", key="Blue"), sg.Checkbox("Green", key="Green"), sg.Checkbox("White", key="White"), sg.Checkbox("Black", key="Black"), sg.Checkbox("Allow not released", key='new'), sg.Checkbox("Allow banned", key='banned')], [sg.Button('Find', key='-FIND-'), sg.Button("Randomize", key='-RANDOMIZE-'), sg.Button("Exit", key='-EXIT-')]]

window = sg.Window("Commander Finder", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, '-EXIT-'):
        os.remove(save_name)
        os.remove('bulk.json')
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

        if not values['cmdName']:
            sg.popup("Please enter a name.")

        if cmdColors:
            paramsPayload = {"q": cmdname[0] + ' ' + 'c:' + str(cmdColors).replace("[", "").replace("]", "").replace(",","").replace("'","").replace("'", "").replace(" ", "") + ' ' + 'is:commander' + ' ' + 'legal:commander' + ' ' + 'game:paper'}
            if values['new']:
                paramsPayload = {"q": cmdname[0] + ' ' + 'c:' + str(cmdColors).replace("[", "").replace("]", "").replace(",","").replace("'", "").replace("'", "").replace(" ","") + ' ' + 'is:commander' + ' ' + 'game:paper'}

        elif not cmdColors:
            paramsPayload = {"q": cmdname[0] + ' ' + 'is:commander' + ' ' + 'legal:commander' + ' ' + 'game:paper'}
            if values['new']:
                paramsPayload = {"q": cmdname[0] + ' ' + 'is:commander' + ' ' + 'game:paper'}
            if values['banned']:
                paramsPayload = {"q": cmdname[0] + ' ' + 'type:legendary' + ' ' + 'game:paper'}

        cards = requests.get(url_find, params=paramsPayload)

        if cards.status_code == 200:

            # load commander image
            image = []
            commander = json.loads(cards.text)
            clearcmdname = str(commander['data'][0]['name'])
            if clearcmdname.__contains__('//'):
                cardImage = str(commander['data'][0]['card_faces'][0]['image_uris']['png'])
            else:
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
            resizeImage.thumbnail((int(resize_width), int(resize_height)), Image.Resampling.LANCZOS)
            resizeImage.save(save_name, "PNG")
            image.append(sg.Image(save_name))

            layout = [[sg.Text("Find your commander: ")], [sg.InputText("", key="cmdName"), sg.Checkbox("Red", key="Red"), sg.Checkbox("Blue", key="Blue"), sg.Checkbox("Green", key="Green"), sg.Checkbox("White", key="White"), sg.Checkbox("Black", key="Black"), sg.Checkbox("Allow not released", key='new'), sg.Checkbox("Allow banned", key='banned')], [image], [sg.Button('Find', key='-FIND-'), sg.Button("Randomize", key='-RANDOMIZE-'), sg.Button('Get Deck', key='-DECK-'), sg.Button("Exit", key='-EXIT-')]]
            print(layout)
            window1 = sg.Window("Commander Finder", layout, finalize=True)
            window.close()
            window = window1

        if cards.status_code == 404:
            sg.popup("No card found with the specified parameters.")

    if values['new']:
        window['new'].update(value=True)
    if values['banned']:
        window['banned'].update(value=True)

    time.sleep(0.1)

    if event == '-RANDOMIZE-':

        if cmdColors:
            paramsPayload = {"q": 'c:' + str(cmdColors).replace("[", "").replace("]", "").replace(",", "").replace("'", "").replace("'", "").replace(" ", "") + ' ' + 'is:commander' + ' ' + 'legal:commander' + ' ' + 'game:paper'}
            if values['new']:
                paramsPayload = {"q": 'c:' + str(cmdColors).replace("[", "").replace("]", "").replace(",", "").replace("'", "").replace("'", "").replace(" ", "") + ' ' + 'is:commander' + ' ' + 'game:paper'}

        elif not cmdColors:
            paramsPayload = {"q": 'is:commander' + ' ' + 'legal:commander' + ' ' + 'game:paper'}
            if values['new']:
                paramsPayload = {"q": 'is:commander' + ' ' + 'game:paper'}
            if values['banned']:
                paramsPayload = {"q": 't:legendary' + ' ' + '(t:creature OR t:planeswalker)' + ' ' + 'game:paper'}

        cards = requests.get(url_random, params=paramsPayload)

        if cards.status_code == 200:

            # load commander image
            image = []
            commander = json.loads(cards.text)
            clearcmdname = str(commander["name"])
            if clearcmdname.__contains__('//'):
                cardImage = str(commander['card_faces'][0]['image_uris']['png'])
            else:
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
            resizeImage.thumbnail((int(resize_width), int(resize_height)), Image.Resampling.LANCZOS)
            resizeImage.save(save_name, "PNG")
            image.append(sg.Image(save_name))

            layout = [[sg.Text("Find your commander: ")], [sg.InputText("", key="cmdName"), sg.Checkbox("Red", key="Red"), sg.Checkbox("Blue", key="Blue"), sg.Checkbox("Green", key="Green"), sg.Checkbox("White", key="White"), sg.Checkbox("Black", key="Black"), sg.Checkbox("Allow not released", key='new'), sg.Checkbox("Allow banned", key='banned')], [image], [sg.Button('Find', key='-FIND-'), sg.Button("Randomize", key='-RANDOMIZE-'), sg.Button('Get Deck', key='-DECK-'), sg.Button("Exit", key='-EXIT-')]]
            print(layout)
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
            sg.popup("No card found with the specified parameters.")

    if values['new']:
        window['new'].update(value=True)
    if values['banned']:
        window['banned'].update(value=True)

    time.sleep(0.1)

    if event == '-DECK-':
        deck = edhrec.get_commanders_average_deck(clearcmdname)
        decklist_list = deck['decklist']
        decklist = ''
        cardstr = ''
        card = ''
        deckprice = 0.0
        cardprice = 0.0
        nopricecount = 0
        url_bulk_info = 'https://api.scryfall.com/bulk-data'
        bulk_info_json = requests.get(url_bulk_info).json()
        urllib.request.urlretrieve(bulk_info_json['data'][0]['download_uri'], 'bulk.json')
        with open('bulk.json', encoding='utf-8') as bulk:
            scryfall_bulk = json.load(bulk)
        for i in decklist_list:
            cardstr = str(i)
            card = re.sub('[1-9]', '', cardstr).strip()
            for singlecard in scryfall_bulk:
                if singlecard['name'] == card:
                    if not str(singlecard['prices']['eur']).__contains__('None'):
                        cardprice = float(singlecard['prices']['eur'])
                    else:
                        if not str(singlecard['prices']['usd']).__contains__('None'):
                            cardprice = float(singlecard['prices']['usd'])
                        else:
                            nopricecount += 1
            deckprice += cardprice
            decklist += i + '\n'
        pyperclip.copy(decklist)
        sg.popup('{} cards provided no price.'.format(nopricecount))
        time.sleep(0.1)
        image2 = []
        image2.append(sg.Image(save_name))

        layout = [[sg.Text("Find your commander: ")],
              [sg.InputText("", key="cmdName"), sg.Checkbox("Red", key="Red"), sg.Checkbox("Blue", key="Blue"),
               sg.Checkbox("Green", key="Green"), sg.Checkbox("White", key="White"), sg.Checkbox("Black", key="Black"),
               sg.Checkbox("Allow not released", key='new'), sg.Checkbox("Allow banned", key='banned')], [image2],
              [sg.Text('Budget: {} EUR'.format(round(deckprice, 2)))],
              [sg.Button('Find', key='-FIND-'), sg.Button("Randomize", key='-RANDOMIZE-'), sg.Button('Get Deck', key='-DECK-'),
               sg.Button("Exit", key='-EXIT-')]]
        print(layout)
        window1 = sg.Window("Commander Finder", layout, finalize=True)
        window.close()
        window = window1