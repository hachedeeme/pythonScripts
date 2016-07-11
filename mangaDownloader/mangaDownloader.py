#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import codecs
import urllib.request
import urllib.parse
from html.parser import HTMLParser

def get_int_from(aString):
  return int(re.search(r'\d+', aString).group())

def get_title(title):
  return title.split(': ')[1]

escape_range = [
  (0xA0, 0xD7FF),
  (0xE000, 0xF8FF),
  (0xF900, 0xFDCF),
  (0xFDF0, 0xFFEF),
  (0x10000, 0x1FFFD),
  (0x20000, 0x2FFFD),
  (0x30000, 0x3FFFD),
  (0x40000, 0x4FFFD),
  (0x50000, 0x5FFFD),
  (0x60000, 0x6FFFD),
  (0x70000, 0x7FFFD),
  (0x80000, 0x8FFFD),
  (0x90000, 0x9FFFD),
  (0xA0000, 0xAFFFD),
  (0xB0000, 0xBFFFD),
  (0xC0000, 0xCFFFD),
  (0xD0000, 0xDFFFD),
  (0xE1000, 0xEFFFD),
  (0xF0000, 0xFFFFD),
  (0x100000, 0x10FFFD),
]

def encode(c):
    retval = c
    i = ord(c)
    for low, high in escape_range:
        if i < low:
            break
        if i >= low and i <= high:
            retval = "".join(["%%%2X" % o for o in c.encode('utf-8')])
            break
    return retval
    
def iri2uri(uri):
    """Convert an IRI to a URI. Note that IRIs must be
    passed in a unicode strings. That is, do not utf-8 encode
    the IRI before passing it into the function."""
    if isinstance(uri ,str):
        (scheme, authority, path, query, fragment) = urllib.parse.urlsplit(uri)
        authority = authority.encode('idna').decode('utf-8')
        # For each character in 'ucschar' or 'iprivate'
        #  1. encode as utf-8
        #  2. then %-encode each octet of that utf-8
        uri = urllib.parse.urlunsplit((scheme, authority, path, query, fragment))
        uri = "".join([encode(c) for c in uri])
    return uri

class JokerFansubHTMLParser(HTMLParser):
  def __init__(self, path):
    super(JokerFansubHTMLParser, self).__init__(convert_charrefs=True)
    self.data  = {}
    self.attrs = []
    self.path  = path

  def handle_starttag(self, tag, attrs):
    if tag == 'img':
      if ('class', 'open') in attrs:
        for name, value in attrs:
          if name == 'src':
            self.data['imagePath'] = str(value)
    if tag == 'a':
      for name, value in attrs:
        if name == 'href' and self.path in value:
          self.data['nextPage'] = str(value)
          self.attrs.append(attrs)
        if name == 'onclick' and 'changePage(' in value:
          self.data['lastPage'] = get_int_from(value) + 1

  def find_chapter_name(self, vol, chapter):
    ref = ('href',self.path + str(vol) + '/' + str(chapter) + '/')
    for attr in self.attrs:
      if ref in attr:
        return get_title(attr[1][1])

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
          self.download_image(iri2uri(self.parser.data['imagePath']), dirName + '/' + imageName)
          print('generate ' + dirName + '/' + imageName)

path = 'http://reader.jokerfansub.com/read/_one_piece/es/VOL/CHAPTER/page/'

vols = { 35: [329,328], 34: [327,326,325,324,323,322,321,320,319,318,317], 33: [316,315,314,313,312,311,310,309,308,307,306], 32: [305,304,303,302,301,300,299,298,297,296], 31: [295,294,293,292,291,290,289,288,287,286], 30: [285,284,283,282,281,280,279,278,277,276], 29: [275,274,273,272,271,270,269,268,267,266,265], 28: [264,263,262,261,260,259,258,257,256], 27: [255,254,253,252,251,250,249,248,247], 26: [246,245,244,243,242,241,240,239,238,237], 25: [236,235,234,233,232,231,230,229,228,227], 24: [226,225,224,223,222,221,220,219,218,217], 23: [216,215,214,213,212,211,210,209,208,207,206], 22: [205,204,203,202,201,200,199,198,197,196], 21: [195,194,193,192,191,190,189,188,187], 20: [186,185,184,183,182,181,180,179,178,177], 19: [176,175,174,173,172,171,170,169,168,167], 18: [166,165,164,163,162,161,160,159,158,157,156], 17: [155,154,153,152,151,150,149,148,147,146], 16: [145,144,143,142,141,140,139,138,137], 15: [136,135,134,133,132,131,130,129,128,127], 14: [126,125,124,123,122,121,120,119,118], 13: [117,116,115,114,113,112,111,110,109], 12: [108,107,106,105,104,103,102,101,100], 11: [99,98,97,96,95,94,93,92,91], 10: [90,89,88,87,86,85,84,83,82], 9:  [81,80,79,78,77,76,75,74,73,72], 8:  [71,70,69,68,67,66,65,64,63], 7:  [62,61,60,59,58,57,56,55,54], 6:  [53,52,51,50,49,48,47,46,45], 5:  [44,43,42,41,40,39,38,37,36], 4:  [35,34,33,32,31,30,29,28,27], 3:  [26,25,24,23,22,21,20,19,18], 2:  [17,16,15,14,13,12,11,10,9], 1:  [8,7,6,5,4,3,2,1]}
vols = { 1: [8,7,6,5,4,3,2,1] }

parser = JokerFansubHTMLParser('http://reader.jokerfansub.com/read/_one_piece/es/')

md = MangaDownloader(vols, path, parser)
# md.download_mangas()

path = 'http://reader.jokerfansub.com/read/dragon_ball_super/es/VOL/CHAPTER/page/'
vols = { 2: [9] }
vols = { 1: [3,2,1] }
vols = { 2: [13,12,11,10,9,8,7], 1: [6,5,4,3,2,1] }

parser = JokerFansubHTMLParser('http://reader.jokerfansub.com/read/dragon_ball_super/es/')
md = MangaDownloader(vols, path, parser)
md.download_mangas()