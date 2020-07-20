from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import os
import sqlite3
from sqlite3 import Error
import re
import time

class Models():
    marka = 'Brak'
    modele = []


all_scraped = 0
czas_pobierania_stron = 0
class Car():
    cena = None
    rok = None
    przebieg = None
    silnik = None
    typ_paliwa = None
    link = None
    marka = None
    model = None
    def opisz(self):
        print(f"{self.marka} {self.model} Cena: {self.cena} Rok: {self.rok} Przebieg: {self.przebieg} Silnik: {self.silnik} Typ paliwa: {self.typ_paliwa}")

def entersite(adress):
    req = Request(adress, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"})
    try:
        uClient = urlopen(req)
    except:
        try:
            uClient = urlopen(req)
        except:
            print("Couldn't connect to page")
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, 'html.parser')
    #print(f'Poprawnie odczytaem dane ze strony: {adress}')
    return page_soup

def data_implement(auction):
    ret = Car()
    link = auction.find('a', class_="offer-title__link")
    dane = auction.find_all(class_="ds-param")

    #brand
    marka = auction['data-param-make'].capitalize()
    ret.marka = marka

    #model
    marka += " "
    model = re.compile(re.escape(marka), re.IGNORECASE)
    model = model.sub("", link['title'])
    ret.model = model

    #link
    ret.link = link['href']

    #price
    cena = auction.find('span', class_="offer-price__number ds-price-number")
    cena = cena.span.text
    if ("," in cena):
        cena = cena[:-3]
    try: ret.cena = int(cena.replace(" ", ""))
    except: ret.cena = None
    if (ret.cena > 10000000):
        ret.cena = 'error'

    #year
    try: ret.rok = int(dane[0].span.text)
    except: ret.rok = None

    #mileage
    try: ret.przebieg = int((dane[1].span.text).replace(" ", "").replace("km", ""))
    except: ret.przebieg = None

    #engine
    try: ret.silnik = dane[2].span.text
    except: ret.silnik = None

    #type of fuel
    try: ret.typ_paliwa = dane[3].span.text
    except: ret.typ_paliwa = 'nie podano'
    return ret

def take_auctions(page):
    global counter,range_text,all_scraped
    # list of auctions
    list = []
    # First auction on actual page
    auction = page.find('article')
    # Auctions to the end of acutal page
    all_auctions_in_range = page.find('span', class_="counter").text[1:-1]

    while auction != None:
        new = data_implement(auction)
        list.append(new)
        counter = counter + 1
        all = all + 1
        auction = auction.find_next('article')
    print(f"Przedział: {range_text} | pobrano {counter} z {all_auctions_in_range} | łącznie pobrano: {all}")
    return list

def average(list):
    sum = 5000
    max = min = lista[0]
    for i in range(len(lista)):
        if (lista[i].cena > max.cena):
            max = lista[i]
        if (lista[i].cena < min.cena):
            min = lista[i]
        try:
            sum += float(lista[i].cena)
        except:
            sum +=0
        srednia = sum / (i + 1)
        #print(f"akutalnie suma: {sum} Srednia {srednia}")
    print(f"Srednia cena to: {srednia}\n Najtansza fura: {min.link}\n ")
    min.opisz()
    print(f"Najdrozsza fura: {max.link}\n")
    max.opisz()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print("Połączono do bazy danych" + db_file)
    except Error as e:
        print(e)
    return conn

def sql_cars(db_file,lista):
    sql_create_cars = """CREATE TABLE IF NOT EXISTS cars (
                                    marka text,
                                    model text,
                                    cena integer,
                                    rok integer,
                                    przebieg integer,
                                    silnik text,
                                    typ_paliwa text,
                                    link text);
                                    """
    conn = create_connection(db_file)
    if conn:
        c = conn.cursor()
        c.execute(sql_create_cars)
        insert = f"""INSERT INTO cars(marka,model,cena,rok, przebieg, silnik, typ_paliwa, link) 
        VALUES(?,?,?,?,?,?,?,?)"""
        for i in range(len(lista)):
            c.execute(insert, [lista[i].marka, lista[i].model, lista[i].cena, lista[i].rok, lista[i].przebieg,  lista[i].silnik, lista[i].typ_paliwa, lista[i].link])
        conn.commit()
    else:
        print("NIe udało mi się stworzyć tabeli")

def every_car_complex_sql(base_adress, db_file):
    # at otomoto.pl if you don't set any searching settings you get "only" 500 pages with cars which equals to about 16000 cars. There are more auctions at the whole page otomoto.pl but they aren't shown. To get access to them we will be searching cars in given range.

    start_price = 0
    price_range = 500
    for i in range(2000):
        global counter, range_text, all_scraped, czas_pobierania_stron
        counter = 0
        settings = "?search%5Bfilter_float_price%3Afrom%5D=" + str((start_price + price_range * i) + 1) + "&search%5Bfilter_float_price%3Ato%5D=" + str(start_price + price_range * (i + 1)) + "&search%5Bfilter_enum_damaged%5D=0&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D="
        range_text = "<" + str(
            (start_price + price_range * i) + 1) + " zł, " + str(
            start_price + price_range* (i+1)) + " zł>"
        start_aukcja = time.time()
        actualpage = entersite(base_adress+settings)
        koniec_aukcja = time.time()
        print(f"CZAS: {koniec_aukcja - start_aukcja}")
        czas_pobierania_stron += (koniec_aukcja - start_aukcja)
        sql_cars(db_file, take_auctions(actualpage))
        nextpageURL = actualpage.find('li', class_="next abs")
        while nextpageURL != None:
            next_adress = nextpageURL.a['href']
            start_aukcja = time.time()
            actualpage = entersite(next_adress)
            koniec_aukcja = time.time()
            print(f"CZAS: {koniec_aukcja - start_aukcja}")
            czas_pobierania_stron += (koniec_aukcja - start_aukcja)
            sql_cars(db_file, take_auctions(actualpage))
            nextpageURL = actualpage.find('li', class_="next abs")

#licznik_start_programu = time.time()

#start_adress = "https://www.otomoto.pl/osobowe/"
#every_car_complex_sql(start_adress, '18.07.2020.db')

#licznik_koniec_programu = time.time()
#print(f" Czas działania całego programu: {licznik_koniec_programu-licznik_start_programu}")
#print(f"Czas pobierania aukcji {czas_pobierania_stron}")
#procentowo = (czas_pobierania_stron *100) / (licznik_koniec_programu-licznik_start_programu)
#print(f"Pobieranie aukcji to: {procentowo} %")