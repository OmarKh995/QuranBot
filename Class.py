from flask import Flask,request
import requests
from urllib.request import urlopen
import json
import pyarabic.araby as araby
import codecs

Quran = json.load(open("quran.json"))
Chapters = json.load(open("en.json"))

class quran:
    def __init__(self):
        self.Quran = json.load(codecs.open("quran.json", encoding='utf-8'))
        self.Chapters = json.load(codecs.open("en.json", encoding='utf-8'))
      #HINT : do we need this variable ? 
        self.selection = {"chapter": 1, "verse": 1}
        
    def suraDetails(self, msg):
      for suraName in self.Chapters:
        #HINT: where is request variable come from? 
        #this function shouldn't depend on external variables 
        #try to add parameter to this function to solve this issue
        if msg == suraName['name']:
          #HINT: use name for i related to it's identity, ex : chapter
          if suraName['type'] == "meccan":
            sura_type = "مكية"
          else:
            sura_type = "مدنية"
          #HINT: you should have a seperated function to send messages in bot class
          text = "اسم السورة : {}\nعدد الآيات : {}\nنوع السورة : {}".format(request.json['message']['text'],suraName['total_verses'],sura_type)
      if msg != "":
        return text
      else:
        msg = ""
        return msg  
        
    def getAyaBySuraName(self, ayaDetails):
        id = None
        text = ""
      #HINT: make function parameters more clear , ex : suraNAme , ayaNumber
        for sura in self.Chapters:
            if sura['name'] == ayaDetails[0]:
                id = sura['id']      
        for suraName in self.Chapters:
          if ayaDetails[0] == suraName['name']:    
            #HINT : same comment above
            text = "اسم السورة : {}\nعدد الآيات : {}\nآية : {}\nنص الآية : {}".format(ayaDetails[0],suraName['total_verses'],Quran[str(id)][int(ayaDetails[1])-1]['verse'],Quran[str(id)][int(ayaDetails[1])-1]['text'])
          # else:
          #   text = "لا توجد آية بهذا الرقم"
            
        return text     
          
    def removeTashkeel(self, string):
      string = string.replace('۞', '').replace('ٰ', 'ا').replace('ـ', '')
      return araby.strip_diacritics(string)
  
    def searchWord(self, searchText):
      #HINT : same comment about parameters above
      searchResults = []
      final = ""
      text = self.removeTashkeel(searchText[1])
      
      for suraName, ayat in self.Quran.items():
        for aya in ayat:
          foundIndex = self.removeTashkeel(aya["text"]).find(text)
          if foundIndex != -1:
            searchResults.append({'سورة': Chapters[aya["chapter"] - 1]["name"], 'آية': aya["verse"]})
      if searchResults == [] or searchResults == {} or searchResults == ():
        msg = "لا توجد نتائج لبحثك"
        return msg
      else: 
        for results in searchResults:
          #HINT: same comment about variable names
          result = "سورة {} آية {}\n".format(results['سورة'], results['آية'])
          final+=result
          #HINT: you can type : if len(results)==0
        return final
     # wronMsg(False)  



#////////////////////////////////////Bot Class//////////////////////////////////////////////////

class bot:
  def __init__(self):
    #HINT: bot token should be a parameter for bot class constructor
    #HINT: setup webhook should be in a seperated function
    #HINT: you should make sure that old webhook is deleted before setting up new one
    # self.Webhook(token, "delete","")
    requests.post("https://api.telegram.org/bot5791068721:AAEDGrvoEDNFdMXHYoIQ--afTa47yt2L0Mg/setWebhook",json={"url":"https://final-bot.bugatti5001.repl.co"})
    print("started")

  def Webhook(self, token, status, url):
    if status == "delete" and url == "":
      requests.post("https://api.telegram.org/bot{}/deleteWebhook".format(token))
    if status == "set":
      requests.post("https://api.telegram.org/bot{}/setWebhook".format(token),json={"url":url})
  
  def default_msg(self, msg):
    #HINT: request variable should be a parameter for the function
    #HINT: this condition should not be inside this function
    if msg == "/start":
      start = "مرحبا !\nأنا بوت القرآن الكريم، يمكنني اخبارك بتفاصيل اي سورة وأي آية من القرآن ، ويمكنني أيضا البحث عن أي كلمة من القرآن\nإذا احتجت إلي أي مساعدة يمكنك إرسال كلمة (ساعدني)"
      return start
    if msg == "ساعدني":
      help = "كيف يعمل البوت : \nيمكنك ارسال اسم السورة لإخبارك بتفاصيلها ، مثلا : الفاتحة\nيمكنك ارسال اسم السورة ورقم الآية ليخبرك بتفاصيل الآية مثلا : الفاتحة:1\nأيضا يمكنك البحث عن أي كلمة عن طريق ارسال : ابحث: كلمة البحث"
      return help
       

  def sendMsg(self, msg, token):  
    requests.post("https://api.telegram.org/bot{}/sendMessage".format(token),json={"chat_id":request.json['message']['chat']['id'],"text":msg})
  

#///////////////////////////////////End Bot Class/////////////////////////////////////////////////////////////////////

