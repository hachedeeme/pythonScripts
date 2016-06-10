import urllib.request
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
  def __init__(self):
    super(MyHTMLParser, self).__init__(convert_charrefs=True)
    self.data = {}

  def handle_starttag(self, tag, attrs):
    if tag == 'img':
      if ('class', 'open') in attrs:
        for name, value in attrs:
          if name == 'src':
            self.data['imagePath'] = str(value)
    if tag == 'a':
      for name, value in attrs:
        if name == 'href' and 'http://reader.jokerfansub.com/read/_one_piece/es/' in value:
          self.data['nextPage'] = str(value)

class MangaDownloader():
  def __init__(self, mangas, path, parser):
    self.mangas = mangas
    self.path   = path
    # Essential data
    self.data = urllib.parse.urlencode({}).encode('ascii')
    self.headers = { 'User-Agent' : 'whatever' }
    self.parser  = parser

  def get_html(currentPath):
    request = urllib.request.Request(currentPath, self.data, self.headers)
    return str(urllib.request.urlopen(request).read())

  def download_image(imagePath, imageName):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'whatever')
    filename, headers = opener.retrieve(imagePath, imageName)

  def download_mangas():
    for vol in self.mangas.keys():
      currentPath = self.path
      currentPath = currentPath.replace('VOL', str(vol))
      for chapter in self.mangas[vol]:
        currentPath = currentPath.replace('CHAPTER', str(chapter))
        html = self.get_html(currentPath)
        self.parser.feed(html)



path = 'http://reader.jokerfansub.com/read/_one_piece/es/VOL/CHAPTER/page/1'
vols = { 35: [329,328], 34: [327,326,325,324,323,322,321,320,319,318,317], 33: [316,315,314,313,312,311,310,309,308,307,306], 32: [305,304,303,302,301,300,299,298,297,296], 31: [295,294,293,292,291,290,289,288,287,286], 30: [285,284,283,282,281,280,279,278,277,276], 29: [275,274,273,272,271,270,269,268,267,266,265], 28: [264,263,262,261,260,259,258,257,256], 27: [255,254,253,252,251,250,249,248,247], 26: [246,245,244,243,242,241,240,239,238,237], 25: [236,235,234,233,232,231,230,229,228,227], 24: [226,225,224,223,222,221,220,219,218,217], 23: [216,215,214,213,212,211,210,209,208,207,206], 22: [205,204,203,202,201,200,199,198,197,196], 21: [195,194,193,192,191,190,189,188,187], 20: [186,185,184,183,182,181,180,179,178,177], 19: [176,175,174,173,172,171,170,169,168,167], 18: [166,165,164,163,162,161,160,159,158,157,156], 17: [155,154,153,152,151,150,149,148,147,146], 16: [145,144,143,142,141,140,139,138,137], 15: [136,135,134,133,132,131,130,129,128,127], 14: [126,125,124,123,122,121,120,119,118], 13: [117,116,115,114,113,112,111,110,109], 12: [108,107,106,105,104,103,102,101,100], 11: [99,98,97,96,95,94,93,92,91], 10: [90,89,88,87,86,85,84,83,82], 9:  [81,80,79,78,77,76,75,74,73,72], 8:  [71,70,69,68,67,66,65,64,63], 7:  [62,61,60,59,58,57,56,55,54], 6:  [53,52,51,50,49,48,47,46,45], 5:  [44,43,42,41,40,39,38,37,36], 4:  [35,34,33,32,31,30,29,28,27], 3:  [26,25,24,23,22,21,20,19,18], 2:  [17,16,15,14,13,12,11,10,9], 1:  [8,7,6,5,4,3,2,1]}


data = urllib.parse.urlencode({})
data = data.encode('ascii')


req = urllib.request.Request('http://reader.jokerfansub.com/read/_one_piece/es/1/1/page/1',data, headers)



for vol in vols.keys():
  currentPath = path
  currentPath = currentPath.replace('VOL', str(vol))
  for chapter in vols[vol]:
    currentPath = currentPath.replace('CHAPTER', str(chapter))

    #print(currentPath)

#r = urllib.request.get(path)
#p = 'http://reader.jokerfansub.com/content/comics/_one_piece_54fbdf740682e/200_0_luffy_de_agua_563a664121045/19.1.jpg'
#p = 'http://reader.jokerfansub.com/read/_one_piece/es/1/1/page/1'
#opener = urllib.request.URLopener()
#opener.addheader('User-Agent', 'whatever')
currentName = 'Capitlo ' + nroCapitulo + " pagina " + pagina
#filename, headers = opener.retrieve(p, currentName)


headers = { 'User-Agent' : 'whatever' }
data = urllib.parse.urlencode({})
data = data.encode('ascii')
req = urllib.request.Request('http://reader.jokerfansub.com/read/_one_piece/es/1/1/page/1',data, headers)

response = urllib.request.urlopen(req)
the_page = response.read()
#print(the_page)

parser = MyHTMLParser()
parser.feed(str(the_page))
print(parser.data)

# output = open("file01.html","wb")
# output.write(the_page)
# output.close()
