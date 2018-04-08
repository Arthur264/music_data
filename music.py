import requests
from database.db_connect import db
from bs4 import BeautifulSoup
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

base_url = 'http://zk.fm'
prefix = 'zk'

def text_encode(text):
    # try:
    #     result = text.encode('utf-8').decode('latin-1')
    # except:
    #     result = text 
    return text
    
def create_table():
    query_data = """CREATE TABLE dataset_zk(
               id INT NOT NULL AUTO_INCREMENT,
               img NVARCHAR(200) NOT NULL,
               artist NVARCHAR(100) NOT NULL,
               time NVARCHAR(10) NOT NULL,
               name NVARCHAR(70) NOT NULL,
               link NVARCHAR(200) NOT NULL,
               PRIMARY KEY ( id )
            ); """
    db.query(query_data)
    query_unique = """ALTER TABLE `dataset` ADD UNIQUE `unique_index`(`artist`, `name`);"""
    # db.query(query_unique)
    
def insert(img, artist, song_time, song_name, song_link):
    # print(img, artist, song_time, song_name, song_link)
    query_data = u"INSERT INTO dataset_zk(img,artist,time,name,link)"\
                "VALUES(N'{i}', N'{a}', N'{t}', N'{n}',N'{l}')".format(i=img, a=artist, t=song_time, n=song_name, l=song_link)
    # print(query_data)
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
        # print(img, artist, song_time, song_name.decode("utf-8"), song_link )
        insert(img, artist, song_time, song_name, song_link)



db.remove_table('dataset_zk')        
create_table()


for n in range(1000):
    print(n)
    res = requests.get(base_url + '/?page=' + str(n))
    soup = BeautifulSoup(res.text)
    dataset = soup.find("section", {"id": "container"}).findAll("div", { "class": "song" })
    parse(dataset)


        
    

