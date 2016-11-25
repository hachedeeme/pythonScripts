import re
from html.parser import HTMLParser

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
          self.data['lastPage'] = self.get_int_from(value) + 1

  def find_chapter_name(self, vol, chapter):
    ref = ('href',self.path + str(vol) + '/' + str(chapter) + '/')
    for attr in self.attrs:
      if ref in attr:
        return self.get_title(attr[1][1])
  
  def get_title(self, title):
    return title.split(': ')[1]

  def get_int_from(self, aString):
    return int(re.search(r'\d+', aString).group())