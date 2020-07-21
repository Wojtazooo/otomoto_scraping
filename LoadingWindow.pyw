# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading_screen.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import os
import sqlite3
from sqlite3 import Error
import re
import time
import threading
import sys




class Models():
    marka = 'Brak'
    modele = []





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
        print(
            f"{self.marka} {self.model} Cena: {self.cena} Rok: {self.rok} Przebieg: {self.przebieg} Silnik: {self.silnik} Typ paliwa: {self.typ_paliwa}")


class Ui_Form(object):


    def entersite(self, adress):
        req = Request(adress, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.130 Safari/537.36"})
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
        # print(f'Poprawnie odczytaem dane ze strony: {adress}')
        return page_soup

    def data_implement(self, auction):
        ret = Car()
        link = auction.find('a', class_="offer-title__link")
        dane = auction.find_all(class_="ds-param")

        # brand
        marka = auction['data-param-make'].capitalize()
        ret.marka = marka

        # model
        marka += " "
        model = re.compile(re.escape(marka), re.IGNORECASE)
        model = model.sub("", link['title'])
        ret.model = model

        # link
        ret.link = link['href']

        # price
        cena = auction.find('span', class_="offer-price__number ds-price-number")
        cena = cena.span.text
        if ("," in cena):
            cena = cena[:-3]
        try:
            ret.cena = int(cena.replace(" ", ""))
        except:
            ret.cena = None
        if (ret.cena > 10000000):
            ret.cena = 'error'

        # year
        try:
            ret.rok = int(dane[0].span.text)
        except:
            ret.rok = None

        # mileage
        try:
            ret.przebieg = int((dane[1].span.text).replace(" ", "").replace("km", ""))
        except:
            ret.przebieg = None

        # engine
        try:
            ret.silnik = dane[2].span.text
        except:
            ret.silnik = None

        # type of fuel
        try:
            ret.typ_paliwa = dane[3].span.text
        except:
            ret.typ_paliwa = 'nie podano'
        return ret

    def take_auctions(self, page):

        # list of auctions
        list = []
        # First auction on actual page
        auction = page.find('article')
        # Auctions to the end of acutal page
        all_auctions_in_range = page.find('span', class_="counter").text[1:-1]

        # taking data from all auctions on actual page
        while auction != None:
            new = self.data_implement(auction)
            list.append(new)
            self.counter = self.counter + 1
            self.all_scraped = self.all_scraped + 1
            auction = auction.find_next('article')

        # status info
        print(f"Przedział: {self.range_text} | pobrano {self.counter} z {all_auctions_in_range} | łącznie pobrano: {self.all_scraped}")
        self.textBrowser.append(f"Przedział: {self.range_text} | w tym przedziale pobrano {self.counter} z {all_auctions_in_range} | łącznie pobrano: {self.all_scraped} z {self.all_cars}")


        # providing info about time left of downlaoding data
        if (self.all_scraped != 0 and self.all_cars!=0):
            seconds_left = int(((1 - (self.all_scraped/self.all_cars))*self.czas_pobierania_stron)/(self.all_scraped/self.all_cars))
            hours_left = seconds_left//3600
            seconds_left = seconds_left % 3600
            minutes_left = seconds_left//60
            seconds_left = seconds_left % 60
            self.label_3.setText(f"{hours_left} h : {minutes_left} m : {seconds_left} s")

        # setting scrollbar to the end of output
        scrollbar = self.textBrowser.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


        return list

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            # print("Połączono do bazy danych" + db_file)
        except Error as e:
            print(e)
        return conn

    def sql_cars(self, db_file, lista):
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
        conn = self.create_connection(db_file)
        if conn:
            c = conn.cursor()
            c.execute(sql_create_cars)
            insert = f"""INSERT INTO cars(marka,model,cena,rok, przebieg, silnik, typ_paliwa, link) 
            VALUES(?,?,?,?,?,?,?,?)"""
            for i in range(len(lista)):
                c.execute(insert, [lista[i].marka, lista[i].model, lista[i].cena, lista[i].rok, lista[i].przebieg,
                                   lista[i].silnik, lista[i].typ_paliwa, lista[i].link])
            conn.commit()
        else:
            print("NIe udało mi się stworzyć tabeli")

    def every_car_complex_sql(self, base_adress, db_file):
        # at otomoto.pl if you don't set any searching settings you get "only" 500 pages with cars which equals to about 16000 cars. There are more auctions at the whole page otomoto.pl but they aren't shown. To get access to them we will be searching cars in given range.

        start_price = 0
        price_range = 500
        self.scrapped_sites = 0
        for i in range(20000):
            self.counter = 0
            start_aukcja = time.time()
            settings = "?search%5Bfilter_float_price%3Afrom%5D=" + str(
                (start_price + price_range * i) + 1) + "&search%5Bfilter_float_price%3Ato%5D=" + str(
                start_price + price_range * (
                        i + 1)) + "&search%5Bfilter_enum_damaged%5D=0&search%5Border%5D=created_at%.3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D="
            self.range_text = "<" + str(
                (start_price + price_range * i) + 1) + " zł, " + str(
                start_price + price_range * (i + 1)) + " zł>"
            actualpage = self.entersite(base_adress + settings)

            self.scrapped_sites+=1


            self.sql_cars(db_file, self.take_auctions(actualpage))
            nextpageURL = actualpage.find('li', class_="next abs")
            koniec_aukcja = time.time()
            self.czas_pobierania_stron += (koniec_aukcja - start_aukcja)
            print(f"CZAS: {koniec_aukcja - start_aukcja}")
            while nextpageURL != None:
                start_aukcja = time.time()
                next_adress = nextpageURL.a['href']
                actualpage = self.entersite(next_adress)
                self.sql_cars(db_file, self.take_auctions(actualpage))
                nextpageURL = actualpage.find('li', class_="next abs")
                koniec_aukcja = time.time()
                print(f"CZAS: {koniec_aukcja - start_aukcja}")
                self.scrapped_sites += 1
                self.czas_pobierania_stron += (koniec_aukcja - start_aukcja)

    def loading_info(self, base_adress):
        self.all_cars = int(self.entersite(base_adress).find('div', id="tabs-container").find('span',
                                                                                                         class_="counter").text.replace(
        " ", "").replace(")", "").replace("(", ""))
        self.scrapped_sites = 0
        self.all_scraped = 0
        self.czas_pobierania_stron = 0

    def funkcja(self,i):
        self.progressBar.setValue(i)

    def startscrapping(self):
        start_adress = "https://www.otomoto.pl/osobowe/"
        self.loading_info(start_adress)

        save_path = QtWidgets.QFileDialog.getSaveFileName()
        save_path = save_path[0]
        print(save_path)

        if (".db" != save_path[-3:]):
            save_path = save_path + ".db"
        if (save_path != ".db"):
            self.thread1 = threading.Thread(target=self.every_car_complex_sql, args=(start_adress, str(save_path)))
            self.thread1.daemon = True
            self.thread1.start()




    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(623, 343)
        Form.setMinimumSize(QtCore.QSize(623, 343))
        Form.setMaximumSize(QtCore.QSize(623, 343))
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(9, 57, 601, 231))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(200, 10, 216, 42))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(263, 301, 96, 31))
        self.pushButton.setMaximumSize(QtCore.QSize(216, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


        # ADDED
        self.pushButton.clicked.connect(self.startscrapping)
        print("SET UP")


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Aktualizacja bazy danych"))
        self.label_2.setText(_translate("Form", "Pobieranie nowej bazy danych"))
        self.label.setText(_translate("Form", "Pozostało:"))
        self.label_3.setText(_translate("Form", ""))
        self.pushButton.setText(_translate("Form", "Rozpocznij"))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


