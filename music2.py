import requests
from database.db_connect import db
from bs4 import BeautifulSoup
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

base_url = 'http://zk.fm'
prefix = 'all'

def text_encode(text):
    # try:
    #     result = text.encode('utf-8').decode('latin-1')
    # except:
    #     result = text 
    return text
    
def create_table():
    query_data = """CREATE TABLE dataset_{0}(
               id INT NOT NULL AUTO_INCREMENT,
               img NVARCHAR(200) NOT NULL,
               artist NVARCHAR(100) NOT NULL,
               time NVARCHAR(10) NOT NULL,
               name NVARCHAR(70) NOT NULL,
               link NVARCHAR(200) NOT NULL,
               PRIMARY KEY ( id ),
               UNIQUE KEY `artist` (`artist`,`name`)
            ); """.format(prefix)
    db.query(query_data)
    
def insert(img, artist, song_time, song_name, song_link):
    # print(img, artist, song_time, song_name, song_link)
    query_data = u"INSERT INTO dataset_{p}(img,artist,time,name,link)"\
                "VALUES(N'{i}', N'{a}', N'{t}', N'{n}',N'{l}')".format(p=prefix, i=img, a=artist, t=song_time, n=song_name, l=song_link)
    db.insert(query_data)
    

def parse(data):
    for item in data:
        try:
            img = base_url + item.find("div", {"class": "song-img"}).img['data-original']
        except:
            img = None
        artist = text_encode(item.find("div", {"class": "song-artist"}).a.span.string)
        song_time = item.find("span", {"class": "song-time"}).get_text()
        song_name = text_encode(item.find("div", {"class": "song-name"}).a.span.string)
        song_link = base_url +  item.find("span", {"class": "song-download"})['data-url']
        insert(img, artist, song_time, song_name, song_link)



db.remove_table('dataset_{0}'.format(prefix))        
create_table()

def main():
    for n in range(1000):
        print(n)
        res = requests.get(base_url + '/?page=' + str(n))
        soup = BeautifulSoup(res.text)
        dataset = soup.find("section", {"id": "container"}).findAll("div", { "class": "song" })
        parse(dataset)
    


def all():
    for n in range(28931):
        for m in range(1000):
            print(n, m)
            res = requests.get(base_url + '/artist/' + str(n) + '/?page=' + str(m))
            soup = BeautifulSoup(res.text)
            
            next = soup.find("a", {"class": "next-btn"}).get("class")
            print("next", next)
            if "disabled" in next:
                break
            else:
                dataset = soup.find("section", {"id": "container"}).findAll("div", { "class": "song" })
                parse(dataset)
            

