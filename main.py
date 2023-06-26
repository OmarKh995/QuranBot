from flask import Flask,request
import requests
from urllib.request import urlopen
import json
import pyarabic.araby as araby
import codecs
from Class import *
#setup the webhook here with the url of the window on the right
# will be like https://<project_name>.<user_name>.repl.co

app = Flask(__name__)

token = "5791068721:AAEDGrvoEDNFdMXHYoIQ--afTa47yt2L0Mg"
quran = quran()
Bot = bot()
#Quran = json.load(open("quran.json"))
#Chapters = json.load(open("en.json"))

    
@app.route('/',methods=['POST','GET'])
def index():
  if request.json:
    sura = ""
    req = request.json['message']['text']
  #HINT : message conditions should be here
    if req == "/start" or req == "ساعدني":
      default = Bot.default_msg(req)
      Bot.sendMsg(default, token)
      
    for suraName in Chapters:
      if req == suraName['name'] and ":" not in req:
        print("in sura details condition")
        sura = quran.suraDetails(req)
        Bot.sendMsg(sura, token)

    
    if ":" in req:
      print("in condition : ")
      searchKey = req.split(":")
      if "ابحث" not in searchKey:
        ayaDetails = quran.getAyaBySuraName(searchKey)
        Bot.sendMsg(ayaDetails, token)
      else:
        print("hi")
        msg = quran.searchWord(searchKey)
        Bot.sendMsg(msg,token)
    # if err == "":
    #   print("sui")
    if sura == "" and ":" not in req:
      #b.wronMsg(True) 
      Bot.sendMsg("رسالة خطأ", token)
      print("hello")

  return ('',200) #keep the return empty, webhook dont return

app.run(host='0.0.0.0', port=81)