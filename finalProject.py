import discord
import requests
import json
from datetime import datetime
import time
import random
import asyncio
from bs4 import BeautifulSoup

client = discord.Client()
channelID = 0
#f = open("log.txt")
urls = []

def randomUA():
    UA = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48',
        'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/88.0.4324.182 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0',
        'Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Mozilla/5.0 (iPad; CPU OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 EdgiOS/44.5.2 Mobile/15E148 Safari/605.1.15', 
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    ]
    return(UA[random.randrange(len(UA) - 1)])
#End of functions

headersAll = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': randomUA()
    }

headersBestBuy = {
    'authority': 'www.bestbuy.ca',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': randomUA(),
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': '',
    'accept-language': 'zh-CN,zh;q=0.9'
}

def Bestbuy(url):
    #print('Function called, checking BestBuy for ' + url)
    #headersBestBuy['referer'] = url
    urlPros = 'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=207%7C954%7C910%7C544%7C795%7C916%7C622%7C926%7C990%7C233%7C202%7C930%7C938%7C57%7C932%7C200%7C245%7C617%7C927%7C203%7C615%7C62%7C237%7C977%7C956%7C931%7C631%7C942%7C965%7C943%7C937%7C985&postalCode=L7A&skus=' + url[url.rindex('/') + 1:]
    response1 = requests.get(urlPros, headers = headersBestBuy)
    response_formatted = json.loads(response1.content.decode('utf-8-sig').encode('utf-8'))
    quantity = response_formatted['availabilities'][0]['shipping']['quantityRemaining']
    if(quantity < 1):
        return False
        #out of stock
    else:
        return True
        #in stock
'''
def Bestbuy(url):
    print('Function called, checking BB for ' + url)
    req = requests.get(url, headersAll)
    soup = BeautifulSoup(req.content, 'html.parser')
    retValue = str (soup.find_all(class_ = "availabilityMessage_ig-s5 container_3LC03")[0])
    print(retValue.find('Coming soon'))
    if retValue.find('Coming soon') != -1:
        return ''
    else:
        return soup.title.string
'''
def Newegg(url):
    req = requests.get(url, headersAll)
    soup = BeautifulSoup(req.content, 'html.parser')
    retValue = str (soup.find_all(class_ = "product-inventory")[0])
    if retValue.find('OUT OF STOCK') != -1:
        return ''
    else:
        return soup.title.string

def CAComp(url):
    req = requests.get(url, headersAll)
    soup = BeautifulSoup(req.content, 'html.parser')
    retValue = str (soup.find_all(class_ = "pi-prod-availability")[0])
    if retValue.find('Online In Stock') == -1 and retValue.find('Available In Stores') == -1:
        return ''
    else:
        return soup.title.string

def AA(url):
    req = requests.get(url, headersAll)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(soup)
    '''
    Amazon sux and doesnt work.
        '''

def ME(url):
    req = requests.get(url, headersAll)
    soup = BeautifulSoup(req.content, 'html.parser')
    retValue = str (soup.find_all(class_ = "c-capr-inventory__availability")[0])
    if retValue.find('Out of Stock') != -1:
        return ''
    else:
        return soup.title.string


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$start'):
        await message.channel.send('hello')
        channelID = message.channel.id
        #some method

    if message.content.startswith('$add https'):
        thismsg = message.content
        urls.append(thismsg[thismsg.find(' ') + 1:])
        print(urls)
        await message.channel.send('This URL has been added.')

    if message.content.startswith('$rem https'):
        thismsg = message.content
        curl = thismsg[thismsg.find(' ') + 1:]
        if curl in urls:
            urls.pop(urls.index(curl))
        print(urls)
        await message.channel.send('This URL has been removed.')
    
    if message.content.startswith('$get List'):
        currentList = 'Current URLs: \n'
        for strn in urls:
            currentList = currentList + strn + '\n'
        await message.channel.send(currentList)

async def check():
    await client.wait_until_ready()
    channel = client.get_channel('some discord channel id')
    while True:
        nDelay = random.randrange(3, 10)
        for st in urls:
            if(st.find('bestbuy') != -1):
                bb = Bestbuy(st)
                if bb:
                    now = datetime.now()
                    await channel.send(st + ' is currently in stock at ' + now.strftime("%m/%d/%Y, %H:%M:%S"))
            elif(st.find('newegg') != -1):
                ng = Newegg(st)
                if len(ng) != 0:
                    now = datetime.now()
                    await channel.send(ng + ' is currently in stock at ' + now.strftime("%m/%d/%Y, %H:%M:%S"))
            elif(st.find('canadacomputers') != -1):
                cc = CAComp(st)
                if len(cc) != 0:
                    now = datetime.now()
                    await channel.send(cc + ' is currently in stock at ' + now.strftime("%m/%d/%Y, %H:%M:%S"))
            elif(st.find('amazon') != -1):
                aa = AA(st)
                if len(aa) != 0:
                    now = datetime.now()
                    await channel.send(aa + ' is currently in stock at ' + now.strftime("%m/%d/%Y, %H:%M:%S"))
            elif(st.find('memoryexpress') != -1):
                me = ME(st)
                if len(me) != 0:
                    now = datetime.now()
                    await channel.send(me + ' is currently in stock at ' + now.strftime("%m/%d/%Y, %H:%M:%S"))
        print(nDelay)
        await asyncio.sleep(nDelay)

client.loop.create_task(check())
client.run('some discord bot key')
