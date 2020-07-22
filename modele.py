import matplotlib.pyplot as plt
import sqlite3
import numpy as np
import pandas as pd

def dane_lista(database, marka, model, rok=None):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    if (rok == ""): rok = None
    if (model == marka or model == ""): model = None
    search = 'SELECT * FROM cars WHERE marka="' + marka + '"'
    if (model != None):
        search += ' AND model LIKE "%' + model + '%"'
    if (rok != None):
        search += ' AND rok=' + rok + " ORDER BY cena"
    else:
        search += " ORDER BY cena"
    c.execute(search)
    dane = c.fetchall()
    return dane


def Wykresik(database,marka,model, rok):
    print("tuta")
    if (model == marka):
        model = None
    if (rok == ""):
        rok = None
    conn = sqlite3.connect(database)
    c = conn.cursor()
    search = 'SELECT cena, rok FROM cars WHERE marka="' + marka + '"'
    if (model != None):
        search += ' AND model LIKE "%' + model + '%"'
    if (rok != None):
        search += ' AND rok=' + rok + " ORDER BY cena"
    else:
        search+=" ORDER BY rok"

    print(search)
    c.execute(search)
    dane = c.fetchall()

    if (rok == None):
        x = []  # wektor roczników
        y = []  # wektor cen
        for row in dane:
            x.append(row[1])
            y.append(row[0])
        roczniki = []
        for i in range(len(x)):
            if (x[i] not in roczniki):
                roczniki.append(x[i])
        tabela = [roczniki, [0] * len(roczniki), [0] * len(roczniki)]  # lata, liczba samochodów, suma cen
        for i in range(len(x)):
            for j in range(len(roczniki)):
                if (x[i] == roczniki[j]):
                    tabela[1][j] += y[i]
                    tabela[2][j] += 1
        for i in range(len(tabela[0])):
            tabela[1][i] = tabela[1][i] / tabela[2][i]
        # wykres średniej ceny pojazdu w danym roczniku
        plt.subplot(211)
        plt.plot(tabela[0], tabela[1], "o-")
        if (model != None):
            plt.title("Średnia cena " + marka + " " + model)
        else:
            plt.title("Średnia cena " + marka)
        plt.xlabel('Rok Produkcji')
        plt.ylabel('Średnia Cena')
        plt.grid(linestyle='-', linewidth=1.5)

        # wykres Liczba pojazdów w danym roczniku
        plt.subplot(212)
        plt.bar(tabela[0], tabela[2], width=0.3)
        plt.grid()
        plt.xlabel('Rok Produkcji')
        plt.ylabel('Liczba pojazdów')
        plt.title('Liczba pojazdów według rocznika')
        return plt

    else:
        print(dane)
        print(len(dane))
        if (len(dane) > 10):
            sum = 0
            for i in dane:
                sum += i[0]
            srednia = sum / len(dane)
            for i in dane:
                if (i[0] > 1.5 * srednia or i[0] < 0.5*srednia): dane.remove(i)
            print(len(dane))
        min = dane[0][0]
        max = dane[-1][0]
        print ("min = " + str(min))
        print("max = " + str(max))
        podział_na = 20
        x = [min+(i+1)*((max-min)/(podział_na)) for i in range(podział_na)]

        n = np.arange(min,max,1000)
        podział_na = len(n)
        x = n

        roznica = ((x[1]-x[0])/2)
        print(x)
        y = [0]*podział_na
        print(y)

        for i in dane:
            dodano = False
            actual = 0
            while (dodano != True and actual < podział_na):
                if (i[0] >= x[actual]-roznica and i[0] < x[actual]+roznica):
                    y[actual] += 1
                    dodano = True
                else:
                    actual += 1

        print(x)
        print(y)
        plt.bar(x,y,width=700)
        plt.xlabel("Cena samochodu")
        plt.ylabel("liczba samochodow")
        plt.title("Rozkład liczby pojazdów w podprzedziałach cenowych")
        return plt

def Marki(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    szukaj_marki = "SELECT DISTINCT marka FROM cars ORDER BY marka"
    c.execute(szukaj_marki)
    marki = c.fetchall()
    f = open("marki.txt", "w+")
    for marka in marki:
        szukaj_modelu = 'SELECT DISTINCT model FROM cars WHERE marka="' + marka[0] + '"' +  " ORDER BY model"
        c.execute(szukaj_modelu)
        aktualne_modele = c.fetchall()
        print(aktualne_modele)
        f.write(marka[0] + ",")
        for model in aktualne_modele:
            f.write(model[0] + ",")
        f.write('\n')

def Wykresik2(database,marka,model = None):
    if (model == marka):
        model = None
    conn = sqlite3.connect(database)
    c = conn.cursor()
    search = 'SELECT DISTINCT rok,cena FROM cars WHERE marka="' + marka + '"'
    if (model != None):
        search += ' AND model="' + model + '"'
    search += ' ORDER BY rok'
    print(search)
    c.execute(search)
    dane = c.fetchall()
    print(dane)
    search = 'SELECT DISTINCT rok FROM cars WHERE marka="' + marka + '"'
    if (model != None):
        search += ' AND model="' + model + '"'
    search += ' ORDER BY rok'
    c.execute(search)
    sqlout = c.fetchall()
    roczniki = [elem[0] for elem in sqlout]
    plt.plot(roczniki, roczniki)
    print(roczniki)

def Dane_Wykres(database,marka,model = None):
    if (model == marka):
        model = None
    conn = sqlite3.connect(database)
    c = conn.cursor()
    search = 'SELECT cena, rok FROM cars WHERE marka="' + marka + '"'
    if (model != None):
        search += ' AND model="' + model + '"'
    search+=" ORDER BY rok"
    print(search)
    c.execute(search)
    dane = c.fetchall()
    x = []  # wektor roczników
    y = []  # wektor cen
    for row in dane:
        x.append(row[1])
        y.append(row[0])
    roczniki = []
    for i in range(len(x)):
        if (x[i] not in roczniki):
            roczniki.append(x[i])
    tabela = [roczniki, [0] * len(roczniki), [0] * len(roczniki)]  # lata, liczba samochodów, suma cen
    for i in range(len(x)):
        for j in range(len(roczniki)):
            if (x[i] == roczniki[j]):
                tabela[1][j] += y[i]
                tabela[2][j] += 1

    for i in range(len(tabela[0])):
        tabela[1][i] = tabela[1][i] / tabela[2][i]

    return tabela

#dane = Dane_Wykres("20.03.2020.db", "Opel", "Corsa")


