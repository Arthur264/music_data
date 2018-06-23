import requests
from database.db_connect import db
from bs4 import BeautifulSoup
import json
import requests
import urllib2
import sys  
from sms.client import client
reload(sys)  
sys.setdefaultencoding('utf-8')

base_url = 'http://zk.fm'
prefix = 'all'

def text_encode(text):
    try:
       result = text.encode('utf-8').decode('latin-1')
    except:
       result = text 
    return text

def create_table():
    query_data = """CREATE TABLE dataset_{0}(
               id INT NOT NULL AUTO_INCREMENT,
               artist NVARCHAR(100) NOT NULL,
               time NVARCHAR(10) NOT NULL,
               name NVARCHAR(70) NOT NULL,
               link NVARCHAR(200) NOT NULL,
               PRIMARY KEY ( id ),
               UNIQUE KEY `artist` (`artist`,`name`)
            ); """.format(prefix)
    db.query(query_data)
    query_artist = """CREATE TABLE dataset_{0}_artist(
               id INT NOT NULL,
               artist NVARCHAR(100) NOT NULL UNIQUE,
               img NVARCHAR(200) ,
               PRIMARY KEY ( id )
            ); """.format(prefix)
    db.query(query_artist)
    
def insert_data(artist, song_time, song_name, song_link):
    query_data = u"INSERT INTO dataset_{p}(artist,time,name,link)"\
                "VALUES(N'{a}', N'{t}', N'{n}',N'{l}')".format(p=prefix, a=artist, t=song_time, n=song_name, l=song_link)
    db.insert(query_data)
    
def insert_artist(id, artist):
    img = get_image_google(artist)
    query_data = u"INSERT INTO dataset_{p}_artist(id,artist, img)"\
                "VALUES(N'{i}', N'{a}', N'{m}')".format(p=prefix, a=artist, i=id, m=img)
    if db.insert(query_data):
        return True
    return False
    
def get_image_google(text):
    header= "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    res = requests.get("https://www.google.co.in/search", 
              params={'q': text + 'group', 'source': 'lnms', 'tbm': 'isch'}, 
              headers={'User-Agent': header})
    soup = BeautifulSoup(res.content)
    a = soup.find("div",{"class":"rg_meta"})
    try:
        link =json.loads(a.text)["ou"]
    except:
        link = None
    return link
    
def parse(data, n):
    for item in data:
        song_time = item.find("span", {"class": "song-time"}).get_text()
        song_name = text_encode(item.find("div", {"class": "song-name"}).a.span.string)
        song_link = base_url +  item.find("span", {"class": "song-download"})['data-url']
        insert_data(n, song_time, song_name, song_link)



# db.remove_table('dataset_{0}'.format(prefix))    
# db.remove_table('dataset_{0}_artist'.format(prefix))    
# create_table()

def sendSMS(n):
    message = client.messages.create(
    to="+380988977842", 
    from_="+15162605176",
    body="Hello from Python!" + str(n))
    print(message.sid)

def all():
    for n in range(44544, 100000):
        if n%1000 == 0:
            sendSMS(n)
        res1 = requests.get(base_url + '/artist/' + str(n))
        soup1 = BeautifulSoup(res1.text)
        try:
            h1 = text_encode(soup1.find("title").string)
            h1 = h1.split(":")[0]
        except:
            continue
        if insert_artist(n, h1):
            for m in range(1, 1000):
                print(n, m)
                res = requests.get(base_url + '/artist/' + str(n) + '/?page=' + str(m))
                soup = BeautifulSoup(res.text)
                try:
                    next = soup.find("a", {"class": "next-btn"}).get("class")
                except:
                    break
                
                if "disabled" in next:
                    break
                else:
                    dataset = soup.find("section", {"id": "container"}).findAll("div", { "class": "song" })
                    parse(dataset, n)

all()



