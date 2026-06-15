# Instrukcja użytkownika - Network Security Analyzer

## Wstęp

Network Security Analyzer to narzędzie do monitorowania bezpieczeństwa sieci. Aplikacja pomaga wykrywać potencjalne zagrożenia w ruchu sieciowym, takie jak niezaszyfrowane połączenia czy przesyłanie wrażliwych danych bez zabezpieczeń.

## Przed pierwszym uruchomieniem

### Windows:
1. Pobierz i zainstaluj **Npcap** ze strony: https://npcap.com/
2. Podczas instalacji zaznacz opcję "Install Npcap in WinPcap API-compatible Mode"
3. Uruchom CMD lub PowerShell jako **Administrator**
4. Przejdź do folderu z aplikacją
5. Zainstaluj wymagane biblioteki:
   ```
   pip install -r requirements.txt
   ```

### Linux:
1. Zainstaluj libpcap:
   ```bash
   sudo apt-get install libpcap-dev
   ```
2. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```
3. Uruchom aplikację z sudo:
   ```bash
   sudo python3 main.py
   ```

### macOS:
1. Zainstaluj wymagane biblioteki:
   ```bash
   pip3 install -r requirements.txt
   ```
2. Uruchom aplikację z sudo:
   ```bash
   sudo python3 main.py
   ```

## Uruchomienie aplikacji

### Windows:
```
python main.py
```
(Uruchom terminal jako Administrator)

### Linux/macOS:
```bash
sudo python3 main.py
```

## Interfejs aplikacji

Aplikacja składa się z kilku sekcji:

### 1. Panel kontrolny (góra)
- **Interfejs sieciowy** - wybierz kartę sieciową do monitorowania
- **Liczba pakietów** - ile pakietów przechwycić (domyślnie 100)
- **Przyciski:**
  - `Rozpocznij przechwytywanie` - start sniffingu
  - `Zatrzymaj` - przerwij przed osiągnięciem limitu
  - `Analizuj` - uruchom analizę bezpieczeństwa
  - `Generuj raport` - zapisz wyniki do plików

### 2. Panel statusu
Pokazuje aktualny stan aplikacji (gotowy, przechwytywanie, analiza)

### 3. Statystyki
- Liczba przechwyconych pakietów
- Liczba wykrytych zagrożeń

### 4. Zakładki z wynikami
- **Pakiety** - lista przechwyconych pakietów
- **Zagrożenia** - wykryte problemy bezpieczeństwa

## Typowy proces pracy

### Krok 1: Wybór interfejsu
Wybierz kartę sieciową, na której chcesz monitorować ruch:
- **Ethernet** - połączenie kablowe
- **Wi-Fi** - połączenie bezprzewodowe
- **Loopback** - ruch lokalny (127.0.0.1)

### Krok 2: Ustawienia
- Ustaw liczbę pakietów (np. 100 dla szybkiego testu, 500+ dla dokładnej analizy)
- Im więcej pakietów, tym dłuższy czas przechwytywania

### Krok 3: Przechwytywanie
1. Kliknij "Rozpocznij przechwytywanie"
2. Aplikacja będzie zbierać pakiety z sieci
3. Status pokaże "Przechwytywanie pakietów..."
4. Licznik pakietów będzie się aktualizował
5. Możesz zatrzymać wcześniej przyciskiem "Zatrzymaj"

### Krok 4: Przegląd pakietów
Po zakończeniu przechwytywania:
- Przejdź do zakładki "Pakiety"
- Zobacz listę przechwyconych połączeń
- Format: `[nr] czas | źródło:port → cel:port | protokół | rozmiar`

### Krok 5: Analiza
1. Kliknij "Analizuj"
2. Aplikacja sprawdzi pakiety pod kątem zagrożeń
3. Wyniki pojawią się w zakładce "Zagrożenia"

### Krok 6: Przegląd zagrożeń
Zakładka "Zagrożenia" pokazuje:
- **Podsumowanie**: liczba zagrożeń według poziomów
- **Szczegóły**: każde wykryte zagrożenie z opisem
- **Rekomendacje**: jak zabezpieczyć system

### Krok 7: Generowanie raportów
1. Kliknij "Generuj raport"
2. Aplikacja utworzy 3 pliki:
   - `security_report.txt` - raport tekstowy
   - `security_report.html` - raport HTML (otwórz w przeglądarce)
   - `security_report.json` - dane strukturalne

## Poziomy zagrożeń

### 🔴 KRYTYCZNE
Wrażliwe dane bez szyfrowania (hasła, tokeny, karty kredytowe)
**Działanie:** Natychmiastowe zabezpieczenie!

### 🟠 WYSOKIE
- Niezaszyfrowane protokoły (FTP, Telnet)
- Podejrzana aktywność portowa
**Działanie:** Wdrożyć szyfrowanie jak najszybciej

### 🟡 ŚREDNIE
- HTTP zamiast HTTPS
- Inne słabe protokoły
**Działanie:** Planować migrację na bezpieczne wersje

## Przykładowe scenariusze użycia

### Scenariusz 1: Sprawdzenie domowej sieci
1. Wybierz interfejs Wi-Fi
2. Ustaw 200 pakietów
3. Rozpocznij przechwytywanie
4. Korzystaj normalnie z internetu przez 1-2 minuty
5. Przeanalizuj wyniki
6. Sprawdź czy aplikacje używają HTTPS

### Scenariusz 2: Test bezpieczeństwa aplikacji
1. Uruchom swoją aplikację webową
2. Wybierz interfejs Loopback
3. Ustaw 100 pakietów
4. Wykonaj operacje w aplikacji (login, przesyłanie danych)
5. Przeanalizuj czy dane są szyfrowane

### Scenariusz 3: Audyt firmowej sieci
1. Uzyskaj zgodę administratora sieci!
2. Wybierz interfejs Ethernet
3. Ustaw 1000+ pakietów dla dokładnej analizy
4. Przechwytuj przez kilka minut
5. Przeanalizuj wyniki
6. Wygeneruj raport HTML dla managementu

## Interpretacja wyników

### "Wykryto użycie niezaszyfrowanego protokołu HTTP"
**Co to znaczy:** Aplikacja łączy się przez HTTP zamiast HTTPS  
**Ryzyko:** Dane mogą być podsłuchane  
**Rozwiązanie:** Użyj HTTPS (SSL/TLS)

### "Wykryto password przesyłane w niezabezpieczony sposób"
**Co to znaczy:** Hasło w pakiecie bez szyfrowania  
**Ryzyko:** Krytyczne! Hasło może zostać przechwycone  
**Rozwiązanie:** Natychmiast użyj HTTPS/TLS

### "Połączenie na port 3389: RDP (cel ataków brute-force)"
**Co to znaczy:** Ktoś łączy się przez Remote Desktop  
**Ryzyko:** RDP jest często atakowany  
**Rozwiązanie:** Użyj VPN, zmień port, włącz 2FA

## Najczęstsze problemy

### Problem: "Brak interfejsów w liście"
**Przyczyna:** Brak sterowników lub uprawnień  
**Rozwiązanie:**
- Windows: Zainstaluj Npcap
- Linux/Mac: Uruchom z sudo
- Sprawdź czy interfejs jest aktywny

### Problem: "Permission denied"
**Przyczyna:** Brak uprawnień administratora  
**Rozwiązanie:**
- Windows: Uruchom CMD jako Administrator
- Linux/Mac: Użyj `sudo python3 main.py`

### Problem: "Brak pakietów po przechwytywaniu"
**Przyczyna:** Brak ruchu sieciowego  
**Rozwiązanie:**
- Korzystaj z internetu podczas przechwytywania
- Wybierz aktywny interfejs (Wi-Fi jeśli używasz Wi-Fi)
- Zwiększ liczbę pakietów

### Problem: "Aplikacja zawiesza się"
**Przyczyna:** Za dużo pakietów na raz  
**Rozwiązanie:**
- Zmniejsz liczbę pakietów do 100-200
- Zamknij inne aplikacje sieciowe
- Restart aplikacji

## Bezpieczeństwo i etyka

### ⚠️ WAŻNE OSTRZEŻENIE
Przechwytywanie ruchu sieciowego może być nielegalne bez zgody!

### Dozwolone użycie:
✅ Własna sieć domowa  
✅ Sieć firmowa za zgodą administratora  
✅ Środowisko testowe / laboratoryjne  
✅ Audyt bezpieczeństwa z autoryzacją

### Zabronione użycie:
❌ Publiczne sieci Wi-Fi  
❌ Sieci bez zgody właściciela  
❌ Przechwytywanie cudzych danych  
❌ Wykorzystanie w celach nielegalnych

## Wsparcie techniczne

### Gdzie szukać pomocy:
1. Przeczytaj dokumentację techniczną (DOKUMENTACJA_TECHNICZNA.md)
2. Sprawdź FAQ w README.md
3. Zgłoś problem (jeśli to projekt open-source)

### Przydatne komendy diagnostyczne:

**Windows:**
```cmd
# Lista interfejsów
ipconfig /all

# Test Npcap
"C:\Program Files\Npcap\NPFInstall.exe" -h
```

**Linux:**
```bash
# Lista interfejsów
ip addr show

# Test libpcap
tcpdump --list-interfaces
```

## Skróty klawiaturowe

*(Jeśli zaimplementowane w GUI)*
- `Ctrl+S` - Rozpocznij przechwytywanie
- `Ctrl+T` - Zatrzymaj
- `Ctrl+A` - Analizuj
- `Ctrl+R` - Generuj raport
- `Ctrl+Q` - Zamknij aplikację

## Aktualizacje

Sprawdzaj regularnie aktualizacje:
```bash
pip install --upgrade -r requirements.txt
```

## Kontakt

**Projekt edukacyjny**  
Bezpieczeństwo Sieci Komputerowych  
Rok: 2025/2026

---

**Ostatnia aktualizacja:** 15.06.2026  
**Wersja instrukcji:** 1.0
