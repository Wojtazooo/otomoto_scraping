import matplotlib.pyplot as plt
import sqlite3
import numpy as np
import pandas as pd

def dane_lista(database, marka, model, rok=None):
    # connecting to database and creating cursor
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # if a year of production is not specified we are taking data of all models
    if (rok == ""): rok = None
    # if the model is the same as the brand name we are taking a data of all cars of the brand
    if (model == marka or model == ""): model = None
    search = 'SELECT * FROM cars WHERE marka="' + marka + '"'
    # in some cases model have also information about type of engine or capacity. To omit this we use model LIKE instead of model = ...
    if (model != None):
        search += ' AND model LIKE "%' + model + '%"'
    if (rok != None):
        search += ' AND rok=' + rok
    c.execute(search)
    dane = c.fetchall()
    return dane


def Wykresik(database,marka,model, rok):
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


    # There are 2 posibilities of plot we want to achieve
    # 1. Year of production is not specified
    #   Plot of average price depending on the year of production and how many cars are taken to compute this average
    # 2. Year of production is specified
    #   We are graphing how many cars are in price intervals

    # First option
    if (rok == None):
        # x is vector of years
        # y is vector of prices
        x = []
        y = []
        # inserting data
        for row in dane:
            x.append(row[1])
            y.append(row[0])
        # roczniki is vector of unique years of production
        roczniki = []
        # adding unique years to roczniki
        for i in range(len(x)):
            if (x[i] not in roczniki):
                roczniki.append(x[i])
        # We are creating table for graph
        # [ years, how many cars , sum of prices ]
        tabela = [roczniki, [0] * len(roczniki), [0] * len(roczniki)]
        # inputing data
        for i in range(len(x)):
            for j in range(len(roczniki)):
                if (x[i] == roczniki[j]):
                    tabela[1][j] += y[i]
                    tabela[2][j] += 1
        for i in range(len(tabela[0])):
            tabela[1][i] = tabela[1][i] / tabela[2][i]

        # dividing plot
        plt.subplot(211)
        # ploting average price depending on the year of production
        plt.plot(tabela[0], tabela[1], "o-")
        # adding titles and labels to plots
        if (model != None):
            plt.title("Średnia cena " + marka + " " + model)
        else:
            plt.title("Średnia cena " + marka)
        plt.xlabel('Rok Produkcji')
        plt.ylabel('Średnia Cena')
        plt.grid(linestyle='-', linewidth=1.5)

        # second plot of how many cars are in specified price interval
        plt.subplot(212)
        plt.bar(tabela[0], tabela[2], width=0.3)
        # second plot settings
        plt.grid()
        plt.xlabel('Rok Produkcji')
        plt.ylabel('Liczba pojazdów')
        plt.title('Liczba pojazdów według rocznika')

        return plt

    else:
        if (len(dane) > 10):
            sum = 0
            for i in dane:
                sum += i[0]
            srednia = sum / len(dane)
            for i in dane:
                # removing auctions with too big or too less price. In some cases people create auction for 1 zloty or 123 456 789 zl only to get somebody's attention to their auction
                # we would like to remove such cases when we are counting average price
                if (i[0] > 1.5 * srednia or i[0] < 0.5*srednia): dane.remove(i)
        # interval calculations
        min = dane[0][0]
        max = dane[-1][0]
        podział_na = 20
        x = [min+(i+1)*((max-min)/(podział_na)) for i in range(podział_na)]
        n = np.arange(min,max,1000)
        podział_na = len(n)
        x = n
        roznica = ((x[1]-x[0])/2)
        print(x)
        y = [0]*podział_na
        print(y)

        # setting intervals
        for i in dane:
            dodano = False
            actual = 0
            while (dodano != True and actual < podział_na):
                if (i[0] >= x[actual]-roznica and i[0] < x[actual]+roznica):
                    y[actual] += 1
                    dodano = True
                else:
                    actual += 1

        # plot settings
        plt.bar(x,y,width=700)
        plt.xlabel("Cena samochodu")
        plt.ylabel("liczba samochodow")
        plt.title("Rozkład liczby pojazdów w podprzedziałach cenowych")
        return plt

def Marki(database): # function create .txt file with names of brands and their models
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # finding distinct, unique brand in database
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




