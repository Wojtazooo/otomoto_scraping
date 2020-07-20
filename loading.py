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








# I think this is useless function now. It was made to compute avarage price of the cars from list in previous version of app
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







#licznik_start_programu = time.time()

#start_adress = "https://www.otomoto.pl/osobowe/"
#every_car_complex_sql(start_adress, '18.07.2020.db')

#every_car_complex_sql("https://www.otomoto.pl/osobowe/", '18.07.2020.db')

#licznik_koniec_programu = time.time()
#print(f" Czas działania całego programu: {licznik_koniec_programu-licznik_start_programu}")
#print(f"Czas pobierania aukcji {czas_pobierania_stron}")
#procentowo = (czas_pobierania_stron *100) / (licznik_koniec_programu-licznik_start_programu)
#print(f"Pobieranie aukcji to: {procentowo} %")

class Ui_Form(object):

    def setupUi(self, Form):

        Form.setObjectName("Form")
        Form.resize(520, 517)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(20, 100, 481, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(10, 140, 501, 361))
        self.listView.setObjectName("listView")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 471, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignRight)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Pobieranie nowej bazy danych"))
        self.label.setText(_translate("Form", "Pozostało:"))
        self.label_3.setText(_translate("Form", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


