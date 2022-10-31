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
def randomUA():
    UA = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48',
        'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/88.0.4324.182 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0',
        'Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        'Mozilla/5.0 (iPad; CPU OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 EdgiOS/44.5.2 Mobile/15E148 Safari/605.1.15'
    ]
    return(UA[random.randrange(len(UA) - 1)])
#End of functions

URL = 'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=207%7C954%7C910%7C544%7C795%7C916%7C622%7C926%7C990%7C233%7C202%7C930%7C938%7C57%7C932%7C200%7C245%7C617%7C927%7C203%7C615%7C62%7C237%7C977%7C956%7C931%7C631%7C942%7C965%7C943%7C937%7C985&postalCode=L7A&skus=15078017'
URLAlt = 'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=207%7C954%7C910%7C544%7C795%7C916%7C622%7C926%7C990%7C233%7C202%7C930%7C938%7C57%7C932%7C200%7C245%7C617%7C927%7C203%7C615%7C62%7C237%7C977%7C956%7C931%7C631%7C942%7C965%7C943%7C937%7C985&postalCode=L7A&skus=15166285'

headers = {
    'authority': 'www.bestbuy.ca',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': randomUA(),
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3080-ti-12gb-gddr6x-video-card/15530045',
    'accept-language': 'zh-CN,zh;q=0.9'
}

headersAlt = {
    'authority': 'www.bestbuy.ca',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': randomUA(),
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3060-ti-8gb-gddr6-video-card/15166285',
    'accept-language': 'zh-CN,zh;q=0.9'
}

def chk3070(quantity, attempts):
    f = open("stockLog.txt", "a")
    response = requests.get(URL, headers = headers)
    response_formatted = json.loads(response.content.decode('utf-8-sig').encode('utf-8'))
    quantity = response_formatted['availabilities'][0]['shipping']['quantityRemaining']
    if(quantity < 1):
        #out of stock
        attempts += 1
        f.write("RTX 3070    - " + str(datetime.now()) + ": Out of stock. Curremt attempt: " + str(attempts) + "\n")
        f.close()
    else:
        #here
        time.sleep(0.5)
        attempts = chk3070(quantity, attempts)
    return attempts
#end of function

def chk3060(quantity, attempts):
    response = requests.get(URLAlt, headers = headersAlt)
    response_formatted = json.loads(response.content.decode('utf-8-sig').encode('utf-8'))
    quantity = response_formatted['availabilities'][0]['shipping']['quantityRemaining']
    if(quantity < 1):
        print("1")
        #sentMsg('No Stock')
        #out of stock
    else:
        time.sleep(0.5)
        #attempts = chk3060(quantity, attempts)
    return attempts
#end of function

def main():
    quantity = 0
    attempts = 0
    while(True):
        #attempts = chk3070(quantity, attempts)
        #attempts = chk3060(quantity, attempts)
        nextDelay = random.randrange(3, 10)
        print("next check in " + str(nextDelay))
        time.sleep(nextDelay)
        headers['user-agent'] = randomUA()
#end of funtion

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('hello')
        channelID = message.channel.id
        main()

async def c3060():
    await client.wait_until_ready()
    channel = client.get_channel('some discord channel id')
    nextDelay = random.randrange(3, 10)
    print("next check in " + str(nextDelay))
    headersAlt['user-agent'] = randomUA()
    while True:
        response = requests.get(URLAlt, headers = headersAlt)
        response_formatted = json.loads(response.content.decode('utf-8-sig').encode('utf-8'))
        quantity = response_formatted['availabilities'][0]['shipping']['quantityRemaining']
        if(quantity < 1):
            #await channel.send('no stock')
            print('no stock')
            await asyncio.sleep(nextDelay)
            #sentMsg('No Stock')
            #out of stock
        else:
            await channel.send('in stock')
            await asyncio.sleep(0.5)
            #attempts = chk3060(quantity, attempts)
        
client.loop.create_task(c3060())
client.run('some discord bot key')
