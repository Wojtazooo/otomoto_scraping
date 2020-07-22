# otomoto_web_scrapping

##### Program Otomoto scraping pozwala na pobranie danych z jednego z najpopularniejszych serwisów z aukcjami samochodowymi w Polsce otomoto.pl. 

## Główne okno

![GitHub Logo](/screenshots/MainWindow.png)

### W głównym oknie programu możemy wybrać następujące parametry
1. **Baza danych z której korzystamy**
   * Po uruchomieniu programu zostaje wybrana *przykładowa baza danych o nazwie "example_database.db"*
   * Przycisk w prawym górnym rogu **"Zmień"** pozwala na wybranie bazy danych z dowolnej lokalizacji, po zmianie bazy danych ścieżka załadowanej bazy danej zostanie zaktualizowana
   * W celu uzyskania aktualnej bazy danej należy pobrać ją patrz niżej sekcja Pobierz nową bazę danych
1. **Marka pojazdu**
   * wybór marki pojazdu aktualizuje Listę aukcji
   * Spis wszystkich marek oraz modeli zapisany jest w pliku *"marki.txt"* z tego pliku odczytywany jest do list wyboru
1. **Modele**
   * Wybór modelu możliwy jest dopiero po wybraniu marki
   * w przypadku wyboru nazwy modelu takiego samego jak marka na liście danych pojawiają się wszystkie modele
   * niektóre modele zawierają dodatkowe informacje, jak na przykład pojemność silnika, w przypadku wyboru modelu bez dodatkowych informacji brane są pod uwagę również aukcje które w nazwie posiadają bardziej sprecyzowane informacje
1. **Rok produkcji**
   * pozwala nam na przeglądanie pojazdów tylko z danego rocznika
1. **Lista aukcji**
   * Przedstawia podstawowe informacje o pojeździe
   * po dwukrotnym naciśnięciu linku nastąpi otwarcie przeglądarki i przekierowanie na stronę z aukcją, w przypadku starszej bazy danych, aukcja może być już nieaktywna
1. **Wykres**
   * Patrz niżej opis wykresu
1. **Pobierz nową bazę danych**
   * Patrz niżej sekcja Pobierz nową bazę danych
   
## Wykresy 

### Przycisk Wykres wyświetla wykresy w nowym oknie w zależności od wybranej Marki Modelu oraz Roku produkcji w  następujący sposób
 
1. **Wybrana została marka lub marka i model pojazdu**
   * Wykres górny przedstawia zależność średniej wartości pojazdu od rocznika produkcji
   * Wykres dolny przedstawia liczbę pojazdów które są brane do obliczenia średniej wartości
   * ![GitHub Logo](/screenshots/Graph1.png)
1. **Dodatkowo została wybrana marka pojazdu**
   * Wykres dzieli przedział cen na podprzedziały i przedstawia ile pojazdów znajduje się w danym podprzedziale 
   * ![GitHub Logo](/screenshots/Graph2.png)
   



