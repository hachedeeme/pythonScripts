import re
import os
import urllib.request
from html.parser import HTMLParser

def get_int_from(aString):
  return int(re.search(r'\d+', aString).group())

class JokerFansubHTMLParser(HTMLParser):
  def __init__(self):
    super(JokerFansubHTMLParser, self).__init__(convert_charrefs=True)
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
        if name == 'onclick' and 'changePage(' in value:
          self.data['lastPage'] = get_int_from(value) + 1


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
      html    = str(urllib.request.urlopen(request).read())
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
    while not ok and timelimit < 100:
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

      for chapter, title in self.mangas[vol]:
        path = currentPath
        path = path.replace('CHAPTER', str(chapter))
        dirName = 'Vol ' + self.get_vol_name(vol) + '/Capitulo ' +  self.get_chapter_name(chapter) + ' - ' + title

        # Try to get html from path
        self.parse_html(path + '1')

        lastPage = self.parser.data['lastPage'] + 1
        
        self.make_directory(dirName)

        for page in range(1, lastPage):
          self.parse_html(path + str(page))

          imageName = self.get_file_name(vol, chapter, page)
          self.download_image(self.parser.data['imagePath'], dirName + '/' + imageName)
          print('generate ' + dirName + '/' + imageName)

path = 'http://reader.jokerfansub.com/read/_one_piece/es/VOL/CHAPTER/page/'

vols = {
91: [(828, '1 & 2'), (827, 'Totland'), (826, '0 & 4')], 
90: [(825, 'Las Historietas De Nuestro Tiempo'), (824, 'Jueguitos De Pirata'), (823, 'Un Mundo En Movimiento'), (822, 'Descendiendo Del Elefante'), (821, 'Entendido'), (820, 'Perro Y Gato Tienen Una Historia'), (819, 'Momonosuke Heredero Del Clan Kouzumaki'), (818, 'Dentro De La Ballena'), (817, 'Raizou De La Niebla'), (816, 'Perro vs Gato'), (815, 'Llevame Contigo'), (814, 'Vamos A Ver Al Maestro Nekomamushi')], 
80: [(813, 'La Fiesta Del Te'), (812, 'La Banda Capone Bege'), (811, 'Koro'), (810, 'Los Piratas Del Sombrero Rizado Han Llegado'), (809, 'Maestro Nekomamushi'), (808, 'El Duque Inuarashi'), (807, 'Hace 10 Dias'), (806, 'La Fortaleza De La Tripa Derecha'), (805, 'La Tribu Mink'), (804, 'Una Aventura En La Espalda Del Elefante'), (803, 'Escalando El Elefante'), (802, 'Zou'), (801, 'Se Anuncia Una Nueva Era'), (800, 'Juramento De Subordinado'), (799, 'Padre E Hijos'), (798, 'Corazon'), (797, 'Rebecca'), (796, 'La decision de Soldado-San')], 
79: [(795, 'Suicida'), (794, 'La Aventura De Sabo'), (793, 'Tigre & Perro'), (792, 'De Rodillas'), (791, 'Ruinas'), (790, 'Cielo Y Tierra'), (789, 'Lucy'), (788, 'Mi Batalla'), (787, '4 minutos'), (786, 'Gatz')], 
78: [(785, 'Incluso sin mi pierna'), (784, 'Gear 4'), (783, 'Estas En Mi Camino'), (782, 'Encarnacion Del Mal'), (781, 'El Verdadero Deseo'), (780, 'La Maldicion De Corazon'), (779, 'La última pelea')], 
35: [(332, 'Luffy vs Usopp'), (331, '¡La gran pelea!'), (330, '¡Esta decidido!'), (329, 'Mi nombre es Franky'), (328, 'La crisis del secuestro del pirata')], 
34: [(327, 'Souzenjima, Astillero puerto #1'), (326, 'Iceburg-san'), (325, 'La Franky Family'), (324, 'Aventura en la ciudad del Agua'), (323, 'La capital del agua, Water Seven'), (322, 'Puffing Tom'), (321, 'Mano a Mano'), (320, 'La mayor fuerza militar'), (319, 'Almirante del Cuartel General de la Marina, Aokiji'), (318, 'Conclusión'), (317, 'K.O.')], 
33: [(316, 'Brother Soul'), (315, 'La habitacion secreta'), (314, 'Combat!!!'), (313, 'Main event'), (312, 'Goal!!'), (311, 'Rough Game'), (310, 'Groggy Ring!!'), (309, 'Groggy Monsters'), (308, 'El magnifico plan de interferencia'), (307, 'Ready, Donut!!'), (306, 'Donut Race!!')], 
32: [(305, 'Foxy, el zorro plateado'), (304, 'Aventura en Long Island'), (303, 'Piratas muy ricos'), (302, 'Final'), (301, 'Estuvimos aqui'), (300, 'Sinfonia'), (299, 'Fantasia'), (298, 'La cancion de la isla'), (297, 'Rezar por la tierra'), (296, 'Situacion de alto vuelo')], 
31: [(295, 'El tallo gigante'), (294, 'La llegada del trueno'), (293, 'Trance'), (292, 'Encontrar la luna rota a traves de las nubes'), (291, '¡Estaremos aqui!'), (290, 'El fuego de Shandia'), (289, 'Luna llena'), (288, 'Maldición'), (287, 'Asesino de Dios'), (286, 'El monstruo de Shandia')], 
30: [(285, 'Capricho'), (284, 'Chicos malos'), (283, 'La primera linea del amor'), (282, 'Deseo'), (281, 'Despiea'), (280, 'Emergencia'), (279, 'Luffy vs Dios Enel'), (278, 'Conis'), (277, 'Maxim'), (276, 'Shandia Rhythm')], 
29: [(275, 'Divina comedia'), (274, 'Oratorio'), (273, 'Quinteto'), (272, 'Play'), (271, 'Zoro vs Ohm'), (270, 'Serenade'), (269, 'Concerto'), (268, 'Suite'), (267, 'March'), (266, 'Chopper vs Aum'), (265, 'Robin vs Yama')], 
28: [(264, 'Guerrero Kamakiri vs dios Enel'), (263, 'Nami y el caballero del cielo vs guardianes divinos Hotori y Kotori'), (262, 'Chopper vs el sacerdote Gedatsu'), (261, 'El guerrero Genbou vs Yama el líder de la guardia divina'), (260, 'Luffy vs Wiper'), (259, 'Zoro vs Braham'), (258, 'Todos al sur'), (257, 'Batalla Dial'), (256, 'Wiper "El demonio de la guerra"')], 
27: [(255, 'La serpiente y el equipo de la búsqueda'), (254, 'Aubade'), (253, 'Verse'), (252, 'Junction'), (251, 'Overture'), (250, 'Dragón de esferas'), (249, 'La villa oculta en las nubes'), (248, 'Ex-Dios vs. sacerdote'), (247, 'Prueba de las Esferas')], 
26: [(246, 'Satori, sacerdote del Bosque Maya'), (245, 'Aventura en la isla de Dios'), (244, 'SOS'), (243, 'Pruebas'), (242, 'Criminales de segunda clase'), (241, 'El juicio del cielo'), (240, 'Dial Energy'), (239, 'Angel Beach'), (238, 'Puerta del Paraíso'), (237, 'En el cielo')], 
25: [(236, 'El barco va hacia el cielo'), (235, 'Knock-Up Stream'), (234, 'Por favor no olvides recordarlo'), (233, 'La mayor autoridad en el mundo'), (232, 'El hombre de los cien millones'), (231, 'Bellamy la Hiena'), (230, '¡¡Tras el South Bird!!'), (229, '¡A comer!'), (228, '"Líder supremo de la Alianza Saruyama", Montblanc Cricket'), (227, 'Noland, el mentiroso')], 
24: [(226, 'Shoujou, rey de búsquedas bajo el mar'), (225, 'El sueño de un hombre'), (224, 'Sin sueños'), (223, 'Prometo no pelear en este pueblo'), (222, 'Grandes novatos'), (221, 'Monstruos '), (220, 'Paseando en el fondo marino'), (219, 'Masira, el rey de salvamento'), (218, 'El motivo por el que "Log Pose" es Esferico'), (217, 'Polizón ')], 
23: [(216, 'La Aventura de Vivi '), (215, 'El último vals'), (214, 'Plan para Escapar del Reino de Arena'), (213, 'VIP'), (212, 'Un poco de justicia'), (211, 'Rey'), (210, '0'), (209, 'Superarte'), (208, 'Espíritu guardián'), (207, 'Pesadilla'), (206, 'Ignición')], 
22: [(205, 'La base secreta del clan Suna Suna'), (204, 'RED'), (203, 'Crocish'), (202, 'La tumba real'), (201, 'Nico Robin'), (200, 'Luffy de agua'), (199, '¡¡Esperanza!!'), (198, '4:15 PM'), (197, 'Los líderes'), (196, '1')], 
21: [(195, 'Mr. Bushido'), (194, 'Cortando el acero'), (193, 'Utopía'), (192, 'Se avecina un tornado'), (191, 'La mujer que controla el clima'), (190, 'Clima Tact'), (189, '2'), (188, 'Kenpo Okama'), (187, 'Igualdad')], 
20: [(186, '4'), (185, 'Genial'), (184, 'Calle Montetopo número 4'), (183, 'Capitán Carue'), (182, 'Rugido'), (181, 'Concurso del superpato mandado'), (180, 'Arabasta reino animal'), (179, 'Batalla decisiva en Alubarna '), (178, 'Nivel G.L.'), (177, '30 Millones vs. 81 Millones')], 
19: [(176, '!!!Rush!!!'), (175, 'Liberación'), (174, 'Mr.Prince'), (173, 'Bananawani'), (172, 'Rebelión'), (171, 'Kohza, líder de los rebeldes'), (170, 'Empezando'), (169, 'El guerrero más fuerte del reino'), (168, 'Rainbase, La ciudad de los sueños'), (167, 'El frente de batalla')], 
18: [(166, 'Luffy vs Vivi'), (165, 'Plan, Utopía'), (164, 'Amo este Pais'), (163, 'Yuba, la base de los rebeldes'), (162, 'Aventura en el reino de arena'), (161, 'La ciudad verde, Erumalu'), (160, 'Café Araña, ¡¡8 en punto!!'), (159, 'Ven'), (158, 'Desembarco en Arabasta'), (157, 'Introducción de Ace'), (156, 'Tiempo de camaradas')], 
17: [(155, 'Sir Crocodile. el pirata'), (154, 'Hacia Arabasta'), (153, 'Los cerezos de Hiruluk'), (152, 'Luna Llena'), (151, 'El Cielo del Reyno de DRUM'), (150, 'Royal Drum Crown VII-Shot Bliking Canoon'), (149, '¡¡¡RUMBLE!!!'), (148, 'No la puedes destrozar'), (147, 'Mentira Descarada'), (146, 'Lucha para proteger el imperio')], 
16: [(145, 'Voluntad Heredada'), (144, 'Historia en un país de nieve'), (143, 'Sin ninguna habilidad'), (142, 'Calabera, Huesos Y Cerezos'), (141, 'Curandero'), (140, 'Castillo de Nieve'), (139, 'Tony Tony Chooper'), (138, 'Cima'), (137, 'Avalancha')], 
15: [(136, 'Un Hombre Llamado Dalton'), (135, 'Lapan'), (134, 'Dra. Kureha'), (133, 'Aventura en el país sin nombre'), (132, '¿Lo ves?'), (131, 'Wapol, El hombre de acero'), (130, 'Velocidad Máxima'), (129, '!!!Hacia adelante!!!'), (128, 'Orgullo'), (127, 'Den Den Mushii')], 
14: [(126, 'Instinto'), (125, 'Candle Champion'), (124, 'Un Té Jodidamente Bueno'), (123, 'Luffy vs Mr. 3'), (122, 'Un cadáver es inútil'), (121, 'Lo Sabía'), (120, 'El Ogro Rojo Lloró'), (119, 'Furtivo'), (118, 'Alguien esta aquí')], 
13: [(117, 'Dorry y Brogy'), (116, 'Enorme'), (115, 'Aventura en Little Garden'), (114, 'La ruta'), (113, '!Esta Bien!'), (112, 'Luffy vs. Zoro'), (111, 'Sindicado secreto del crimen'), (110, 'La noche no acabará'), (109, 'Problema de responsabilidad')], 
12: [(108, '100 Cazarracompensas'), (107, 'Luz de Luna y Tumbas'), (106, 'La ciudad de Bienvenida'), (105, 'Log Pose'), (104, 'La Promesa en el Cabo'), (103, 'Ballena'), (102, 'Ahora, a la Grand Line'), (101, 'Reverse Mountain'), (100, 'Comienza la leyenda')], 
11: [(99, 'Las últimas palabras de Luffy'), (98, 'Nubes Negras'), (97, 'Sandai - Kitetsu'), (96, 'Los peores del East'), (95, 'Gira, Molinillo, gira'), (94, 'La Segunda Persona'), (93, 'Hasta el fondo'), (92, 'Paraíso'), (91, 'DARTS')], 
10: [(90, 'Que puedes hacer'), (89, 'Cambio'), (88, 'Muere'), (87, 'Se Acabo'), (86, 'Caballerosidad vs. Karate Gyojin'), (85, 'antouryuu vs Rokutouryuu'), (84, 'Zombi'), (83, 'Luffy De Negro'), (82, '!Levantemonos!')], 
9: [(81, 'Lagrimas'), (80, 'Un Crimen Es Un Crimen'), (79, 'Vivir'), (78, 'Bellmere-San'), (77, 'Un Paso En Tu Sueño'), (76, 'Dormir'), (75, 'Cartas De Navegacion Y Gyojins'), (74, 'Negocios'), (73, 'El Monstruo Del Grand Line'), (72, 'De Acuerdo Con Tus Posibilidades')], 
8: [(71, 'El Rey De Las Bestias'), (70, 'La Gran Aventura Del Varonil Ussop'), (69, 'Arlong Park'), (68, 'La Cuarta Persona'), (67, 'Sopa'), (66, 'La Lanza Esta Rota'), (65, 'Preparate'), (64, 'Lanza gigante de batalla'), (63, 'No Voy A Morir')], 
7: [(62, 'MH5'), (61, 'Demonio'), (60, 'Solucion'), (59, 'Deuda'), (58, 'Viejo Asqueroso'), (57, 'Los Sueños Tienen Una Razon'), (56, 'De Ninguna Manera'), (55, 'Jungle Blood'), (54, 'Pearl-San')], 
6: [(53, 'Sabagashira #1'), (52, 'El Juramento'), (51, 'Roronoa Zoro Cae Al Mar'), (50, 'Cada Uno Tiene Su Propio Camino'), (49, 'La Tormenta'), (48, 'No vayais por alli'), (47, 'Don Krieg, El Almirante Pirata'), (46, 'Un Cliente no Invitado'), (45, 'Antes De La Tormenta')], 
5: [(44, 'Tres Cocineros'), (43, 'Introduccion de Sanji'), (42, 'Yosaku y Johnny'), (41, 'Al Mar'), (40, 'Los Piratas De Usopp'), (39, 'Por Quien Tocan Las Campanas'), (38, 'Tripulacion Pirata'), (37, 'El Pirata, Kuro En Todos Los Sentidos'), (36, 'Seguidles')], 
4: [(35, 'La Otra Cuesta'), (34, 'Kurahadol El Mayordomo'), (33, 'El Hombre Silencioso'), (32, 'Desastre'), (31, 'La verdad'), (30, '¡Genial!'), (29, 'La cuesta'), (28, 'Luna Creciente'), (27, 'El Plan')],
3: [(26, 'El Plan del Capitan Kuro'), (25, '800 Mentiras'), (24, 'Aquello de lo que no se puede mentir'), (23, 'Introduccion del Capitan Usopp'), (22, 'Eres Un Bicho Raro'), (21, 'Pueblo'), (20, 'El Camino Del Ladron'), (19, 'Akuma No Mi'), (18, 'El Pirata, Buggy El Payaso')], 
2: [(17, 'Nivel'), (16, 'VERSUS!! Los Piratas De Buggy'), (15, 'Gong'), (14, '!Imprudente!'), (13, 'El Tesoro'), (12, 'El Perro'), (11, 'La Huida'), (10, 'Incidente En El Bar'), (9, 'La Chica Con El Corazon Del Demonio')], 
1: [(8, 'Aparece Nami'), (7, 'Amigos'), (6, 'El Primer Miembro'), (5, 'El Rey De Los Piratas Y El Gran Espadachín'), (4, 'El Capitan Brazo De Hacha Morgan'), (3, 'Zoro, El Cazador De Piratas Entra En Escena'), (2, 'Luffy, EL Hombre Del Sombrero De Paja'), (1, 'Romance Dawn - El Amanecer De La Aventura')]
}
vols = { 1: [(8, 'Aparece Nami'), (7, 'Amigos'), (6, 'El Primer Miembro'), (5, 'El Rey De Los Piratas Y El Gran Espadachín'), (4, 'El Capitan Brazo De Hacha Morgan'), (3, 'Zoro, El Cazador De Piratas Entra En Escena'), (2, 'Luffy, EL Hombre Del Sombrero De Paja'), (1, 'Romance Dawn - El Amanecer De La Aventura')]}

vols = { 1: [(8, 'Aparece Nami'), (7, 'Amigos'), (6, 'El Primer Miembro'), (5, 'El Rey De Los Piratas Y El Gran Espadachín')]}
parser = JokerFansubHTMLParser()
md = MangaDownloader(vols, path, parser)
md.download_mangas()