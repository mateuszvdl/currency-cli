import requests
import json
import sqlite3
import csv

def pobierz_i_zapisz_kursy():
    url = 'https://api.nbp.pl/api/exchangerates/tables/A'
    response = requests.get(url)
    data = response.json()

    conn = sqlite3.connect('kursy_walut.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS kursy (
                        data TEXT,
                        waluta TEXT,
                        kurs REAL
                    )''')

    for item in data[0]['rates']:
        waluta = item['currency']
        kurs = item['mid']

        cursor.execute("INSERT INTO kursy (data, waluta, kurs) VALUES (DATE('now'), ?, ?)", (waluta, kurs))

    conn.commit()
    conn.close()

def przeszukaj_archiwum():
    conn = sqlite3.connect('kursy_walut.db')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT waluta FROM kursy ORDER BY waluta")
    waluty = cursor.fetchall()

    if len(waluty) == 0:
        print("Brak danych w archiwum.")
        return

    print("Dostępne waluty w archiwum:")
    for idx, waluta in enumerate(waluty, start=1):
        print(f"{idx}. {waluta[0]}")

    waluta_index = input("Podaj numer waluty, którą chcesz przeszukać: ")

    try:
        waluta_index = int(waluta_index)
        if waluta_index < 1 or waluta_index > len(waluty):
            raise ValueError
    except ValueError:
        print("Nieprawidłowy numer waluty.")
        return

    wybrana_waluta = waluty[waluta_index - 1][0]

    cursor.execute("SELECT data, kurs FROM kursy WHERE waluta = ? ORDER BY data", (wybrana_waluta,))
    wyniki = cursor.fetchall()

    if len(wyniki) == 0:
        print(f"Brak danych dla waluty {wybrana_waluta}.")
    else:
        print(f"Archiwum kursów dla waluty {wybrana_waluta}:")
        for wynik in wyniki:
            data, kurs = wynik
            print(f"{data}: {kurs}")

    conn.close()

def kalkulator_walutowy(kwota, waluta_docelowa):
    url = f'https://api.nbp.pl/api/exchangerates/rates/A/{waluta_docelowa}/'
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        print("Nieprawidłowa waluta docelowa.")
        return None

    kurs = data['rates'][0]['mid']

    kwota_docelowa = kwota / kurs

    return kwota_docelowa

def eksportuj_do_csv():
    conn = sqlite3.connect('kursy_walut.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM kursy ORDER BY data")
    wyniki = cursor.fetchall()

    with open('archiwum_kursow.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Data', 'Waluta', 'Kurs'])
        writer.writerows(wyniki)

    conn.close()

def menu():
    print("=== System pobierania kursów walut ===")
    print("1. Pobierz i zapisz aktualne kursy")
    print("2. Przeszukaj archiwum kursów walut")
    print("3. Kalkulator walutowy")
    print("4. Eksportuj dane do pliku CSV")
    print("5. Wyjście")
    print("=====================================")

def main():
    while True:
        menu()
        wybor = input("Wybierz opcję: ")

        if wybor == '1':
            pobierz_i_zapisz_kursy()
            print("Pobrano i zapisano aktualne kursy.")
        elif wybor == '2':
            przeszukaj_archiwum()
        elif wybor == '3':
            kwota_pln = float(input("Podaj kwotę w PLN: "))
            waluta_docelowa = input("Podaj kod waluty docelowej: ")
            kwota_docelowa = kalkulator_walutowy(kwota_pln, waluta_docelowa)
            if kwota_docelowa:
                print(f"{kwota_pln} PLN = {kwota_docelowa} {waluta_docelowa}")
        elif wybor == '4':
            eksportuj_do_csv()
            print("Dane zostały wyeksportowane do pliku CSV.")
        elif wybor == '5':
            break
        else:
            print("Nieprawidłowa opcja. Wybierz ponownie.")

if __name__ == "__main__":
    main()
