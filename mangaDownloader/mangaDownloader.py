#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib.request
import urllib.parse
import httpUtils
from htmlParsers.jokerFansubHTMLParser import JokerFansubHTMLParser

class MangaDownloader():
  def __init__(self, mangas, path, parser):
    self.mangas = mangas
    self.path   = path
    self.parser = parser
    # Essential data
    self.data = urllib.parse.urlencode({}).encode('ascii')
    self.headers = { 'User-Agent' : 'whatever' }

  def get_html(self, currentPath):
    html = ""
    try:
      request = urllib.request.Request(currentPath, self.data, self.headers)
      html    = urllib.request.urlopen(request).read().decode('utf8')
    except urllib.error.HTTPError as error:
      print(str(error))
    except urllib.error.URLError as error:
      print(str(error) + ' - Invalid URL or have not internet conection')
    except Exception as e:
      print('ERROR GROSO: Se econtró un error de esta clase: ' + str(type(e)))
    finally:
      return html

  def download_image(self, imagePath, imageName):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'whatever')
    filename, headers = opener.retrieve(imagePath, imageName)

  def get_file_name(self, vol, chapter, page):
    return 'Vol' + self.get_vol_name(vol) + '-Ch' + self.get_chapter_name(chapter) + '-' + ('0' + str(page) if page < 10 else str(page)) + '.jpg'

  def get_vol_name(self, volNumber):
    if volNumber < 10:
      return '00' + str(volNumber)
    elif volNumber < 100:
      return '0' + str(volNumber)
    else:
      return str(volNumber)

  def get_chapter_name(self, chapterNumber):
    if chapterNumber < 10:
      return '000' + str(chapterNumber)
    elif chapterNumber < 100:
      return '00' + str(chapterNumber)
    elif chapterNumber < 1000:
      return '0' + str(chapterNumber)
    else:
      return str(chapterNumber)

  def make_directory(self, dirName):
    os.makedirs(dirName)

  def parse_html(self, path):
    timelimit = 1
    ok = False
    html = ""
    while not ok and timelimit < 10:
      print('try get first time from: ' + path)
      html = self.get_html(path)
      if not (html == ""):
        print("It's okey")
        ok = True
      else:
        print('Try number ' + str(timelimit))
        timelimit += 1
    self.parser.feed(html)

  def download_mangas(self):
    for vol in self.mangas.keys():
      currentPath = self.path
      currentPath = currentPath.replace('VOL', str(vol))

      for chapter in self.mangas[vol]:
        path = currentPath
        path = path.replace('CHAPTER', str(chapter))

        # Try to get html from path
        self.parse_html(path + '1')
        
        dirName = 'Vol ' + self.get_vol_name(vol) + '/Capitulo ' +  self.get_chapter_name(chapter) + ' - ' + self.parser.find_chapter_name(vol, chapter)
        
        self.make_directory(dirName)
        lastPage = self.parser.data['lastPage'] + 1

        for page in range(1, lastPage):
          self.parse_html(path + str(page))

          imageName = self.get_file_name(vol, chapter, page)
          print(self.parser.data['imagePath'])
          self.download_image(httpUtils.iri2uri(self.parser.data['imagePath']), dirName + '/' + imageName)
          print('generate ' + dirName + '/' + imageName)

#############################
### Descarga de One Piece ###
#############################
path  = 'http://reader.jokerfansub.com/read/_one_piece/es/VOL/CHAPTER/page/'
color = { 36: [337], 35: [336,335,334,333,332,331,330,329,328], 34: [327,326,325,324,323,322,321,320,319,318,317], 33: [316,315,314,313,312,311,310,309,308,307,306], 32: [305,304,303,302,301,300,299,298,297,296], 31: [295,294,293,292,291,290,289,288,287,286], 30: [285,284,283,282,281,280,279,278,277,276], 29: [275,274,273,272,271,270,269,268,267,266,265], 28: [264,263,262,261,260,259,258,257,256], 27: [255,254,253,252,251,250,249,248,247], 26: [246,245,244,243,242,241,240,239,238,237], 25: [236,235,234,233,232,231,230,229,228,227], 24: [226,225,224,223,222,221,220,219,218,217], 23: [216,215,214,213,212,211,210,209,208,207,206], 22: [205,204,203,202,201,200,199,198,197,196], 21: [195,194,193,192,191,190,189,188,187], 20: [186,185,184,183,182,181,180,179,178,177], 19: [176,175,174,173,172,171,170,169,168,167], 18: [166,165,164,163,162,161,160,159,158,157,156], 17: [155,154,153,152,151,150,149,148,147,146], 16: [145,144,143,142,141,140,139,138,137], 15: [136,135,134,133,132,131,130,129,128,127], 14: [126,125,124,123,122,121,120,119,118], 13: [117,116,115,114,113,112,111,110,109], 12: [108,107,106,105,104,103,102,101,100], 11: [99,98,97,96,95,94,93,92,91], 10: [90,89,88,87,86,85,84,83,82], 9:  [81,80,79,78,77,76,75,74,73,72], 8:  [71,70,69,68,67,66,65,64,63], 7:  [62,61,60,59,58,57,56,55,54], 6:  [53,52,51,50,49,48,47,46,45], 5:  [44,43,42,41,40,39,38,37,36], 4:  [35,34,33,32,31,30,29,28,27], 3:  [26,25,24,23,22,21,20,19,18], 2:  [17,16,15,14,13,12,11,10,9], 1:  [8,7,6,5,4,3,2,1]}
news  = { 92: [846,845,844,843,842,841,840,839,838,837,836], 91: [835,834,833,832,831,830,829,828,827,826], 90: [825,824,823,822,821,820,819,818,817,816,815,814], 80: [813,812,811,810,809,808,807,806,805,804,803,802,801,800,799,798,797,796], 79: [795,794,793,792,791,790,789,788,787,786], 78: [785,784,783,782,781,780,779] }
news  = { 92: [846] }
vols  = news

parser = JokerFansubHTMLParser('http://reader.jokerfansub.com/read/_one_piece/es/')
md = MangaDownloader(vols, path, parser)
md.download_mangas()

#####################################
### Descarga de Dragon Ball Super ###
#####################################
path = 'http://reader.jokerfansub.com/read/dragon_ball_super/es/VOL/CHAPTER/page/'
vols = { 3:[17], 2: [16,15,14,13,12,11,10,9,8,7], 1: [6,5,4,3,2,1] }
vols = { 1:[4] }

parser = JokerFansubHTMLParser('http://reader.jokerfansub.com/read/dragon_ball_super/es/')
md = MangaDownloader(vols, path, parser)
# md.download_mangas()