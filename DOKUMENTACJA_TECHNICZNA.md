# Dokumentacja techniczna - Network Security Analyzer

## Autor
**Imię i nazwisko:** [Twoje imię]  
**Grupa:** [Twoja grupa]  
**Wariant:** 3 - Aplikacja do analizy bezpieczeństwa protokołów sieciowych

## 1. Opis projektu

Network Security Analyzer to aplikacja desktopowa napisana w Python, służąca do przechwytywania i analizy ruchu sieciowego pod kątem zagrożeń bezpieczeństwa. Aplikacja umożliwia wykrywanie niezaszyfrowanych protokołów, wrażliwych danych przesyłanych bez zabezpieczeń oraz podejrzanej aktywności portowej.

## 2. Cele projektu

- Przechwytywanie pakietów sieciowych w czasie rzeczywistym
- Analiza protokołów: HTTP, HTTPS, DNS, FTP, SMTP
- Wykrywanie zagrożeń bezpieczeństwa:
  - Niezaszyfrowane protokoły
  - Wrażliwe dane (hasła, tokeny, klucze API) przesyłane bez szyfrowania
  - Podejrzana aktywność na niebezpiecznych portach
- Generowanie raportów bezpieczeństwa (TXT, HTML, JSON)
- Przyjazny interfejs graficzny (GUI)

## 3. Wymagania systemowe

### Minimalne wymagania:
- **System operacyjny:** Windows 10/11, Linux, macOS
- **Python:** wersja 3.8 lub wyższa
- **RAM:** 2 GB
- **Uprawnienia:** Administrator (do przechwytywania pakietów)

### Wymagane oprogramowanie:
- **Windows:** Npcap lub WinPcap
- **Linux:** libpcap
- **macOS:** libpcap (wbudowane)

## 4. Architektura aplikacji

### Struktura modułów:

```
network-security-analyzer/
│
├── main.py                  # Punkt wejścia aplikacji
├── gui.py                   # Interfejs graficzny (Tkinter)
├── packet_capture.py        # Moduł przechwytywania pakietów
├── security_analyzer.py     # Moduł analizy bezpieczeństwa
├── report_generator.py      # Moduł generowania raportów
├── requirements.txt         # Zależności projektu
└── README.md               # Dokumentacja użytkownika
```

### Moduły i ich funkcje:

#### 4.1 `packet_capture.py` - PacketCapture
Odpowiedzialny za przechwytywanie pakietów sieciowych:
- Wykorzystuje bibliotekę **Scapy** do sniffingu pakietów
- Przechwytuje pakiety warstwy IP, TCP i UDP
- Identyfikuje protokoły aplikacyjne (HTTP, HTTPS, FTP, SMTP, DNS)
- Działa w osobnym wątku dla nieblokującej operacji

**Główne metody:**
- `start_capture(interface, packet_count)` - rozpoczyna przechwytywanie
- `stop_capture()` - zatrzymuje przechwytywanie
- `process_packet(packet)` - przetwarza pojedynczy pakiet
- `get_packets()` - zwraca listę przechwyconych pakietów

#### 4.2 `security_analyzer.py` - SecurityAnalyzer
Analizuje pakiety pod kątem zagrożeń bezpieczeństwa:
- Wykrywa niezaszyfrowane protokoły (HTTP, FTP, SMTP)
- Skanuje payload w poszukiwaniu wrażliwych danych (regex patterns)
- Identyfikuje podejrzaną aktywność na niebezpiecznych portach
- Klasyfikuje zagrożenia według poziomu: KRYTYCZNE, WYSOKIE, ŚREDNIE

**Główne metody:**
- `analyze_packets(packets)` - analizuje listę pakietów
- `check_unencrypted_protocol(packet)` - sprawdza protokół
- `check_sensitive_data(packet)` - wykrywa wrażliwe dane
- `check_suspicious_ports(packet)` - analizuje porty
- `generate_summary()` - generuje podsumowanie zagrożeń

**Wykrywane wzorce wrażliwych danych:**
- Hasła: `(password|passwd|pwd)[\s:=]+[\w]+`
- Klucze API: `(api[_-]?key|apikey)[\s:=]+[\w\-]+`
- Tokeny: `(token|auth)[\s:=]+[\w\-\.]+`
- Adresy email
- Numery kart kredytowych

#### 4.3 `report_generator.py` - ReportGenerator
Generuje raporty bezpieczeństwa w różnych formatach:
- **TXT** - prosty raport tekstowy
- **HTML** - interaktywny raport z CSS styling
- **JSON** - strukturalny format dla dalszego przetwarzania

**Główne metody:**
- `generate_text_report(analysis_summary, output_file)`
- `generate_html_report(analysis_summary, output_file)`
- `generate_json_report(analysis_summary, output_file)`

#### 4.4 `gui.py` - NetworkSecurityGUI
Graficzny interfejs użytkownika (Tkinter):
- Wybór interfejsu sieciowego
- Konfiguracja liczby pakietów do przechwycenia
- Kontrola procesu przechwytywania i analizy
- Wyświetlanie wyników w zakładkach (pakiety, zagrożenia)
- Generowanie raportów jednym kliknięciem

## 5. Instalacja i uruchomienie

### Krok 1: Instalacja zależności
```bash
pip install -r requirements.txt
```

### Krok 2: Instalacja sterowników (Windows)
Pobierz i zainstaluj Npcap: https://npcap.com/

### Krok 3: Uruchomienie aplikacji
```bash
# Uruchom z uprawnieniami administratora
python main.py
```

## 6. Instrukcja użytkowania

1. **Wybierz interfejs sieciowy** z listy rozwijanej
2. **Ustaw liczbę pakietów** do przechwycenia (domyślnie 100)
3. **Kliknij "Rozpocznij przechwytywanie"** - aplikacja rozpocznie sniffing
4. **Poczekaj** na zakończenie lub kliknij "Zatrzymaj"
5. **Kliknij "Analizuj"** aby uruchomić analizę bezpieczeństwa
6. **Przejrzyj wyniki** w zakładkach "Pakiety" i "Zagrożenia"
7. **Kliknij "Generuj raport"** aby zapisać wyniki

## 7. Typy wykrywanych zagrożeń

### 7.1 Niezaszyfrowane protokoły
- **HTTP** (port 80) - przesyłanie danych bez szyfrowania
- **FTP** (port 21) - transfer plików bez zabezpieczeń
- **SMTP** (port 25) - wysyłanie email bez TLS
- **Telnet** (port 23) - zdalne połączenia bez szyfrowania

**Rekomendacje:**
- HTTP → HTTPS
- FTP → SFTP/FTPS
- SMTP → SMTP z TLS (port 587/465)
- Telnet → SSH

### 7.2 Wrażliwe dane bez szyfrowania
Wykrywanie w payload pakietów:
- Hasła i dane uwierzytelniające
- Klucze API i tokeny autoryzacyjne
- Adresy email
- Numery kart kredytowych

**Poziom zagrożenia:** KRYTYCZNE

### 7.3 Podejrzana aktywność portowa
Monitorowanie połączeń na niebezpiecznych portach:
- Port 23 (Telnet) - niezaszyfrowany
- Port 69 (TFTP) - niezabezpieczony transfer
- Port 135 (MS RPC) - wykorzystywany przez malware
- Port 445 (SMB) - podatny na ataki
- Port 3389 (RDP) - cel ataków brute-force

## 8. Formaty raportów

### 8.1 Raport tekstowy (TXT)
Prosty, czytelny format zawierający:
- Podsumowanie (liczba zagrożeń według poziomów)
- Szczegółową listę każdego zagrożenia
- Rekomendacje zabezpieczeń

### 8.2 Raport HTML
Interaktywny raport z wizualizacją:
- Kolorowe oznaczenia poziomów zagrożeń
- Responsywny design
- Łatwa nawigacja
- Możliwość wydruku

### 8.3 Raport JSON
Strukturalny format dla:
- Integracji z innymi narzędziami
- Automatycznego przetwarzania
- Archiwizacji wyników

## 9. Bezpieczeństwo i ograniczenia

### Uprawnienia:
Aplikacja wymaga uprawnień administratora do przechwytywania pakietów. Używaj odpowiedzialnie i tylko w sieciach, do których masz autoryzację.

### Ograniczenia:
- Nie dekoduje zaszyfrowanego ruchu (HTTPS, TLS)
- Analiza oparta na wzorcach (możliwe fałszywe pozytywne/negatywne)
- Wydajność zależy od natężenia ruchu sieciowego
- Niektóre zaawansowane techniki obfuskacji mogą ominąć detekcję

### Zgodność z prawem:
**UWAGA:** Przechwytywanie ruchu sieciowego może być regulowane prawem. Używaj tylko w:
- Własnych sieciach
- Środowiskach testowych
- Za zgodą właściciela sieci

## 10. Technologie i biblioteki

- **Python 3.8+** - język programowania
- **Scapy 2.5.0** - przechwytywanie i manipulacja pakietów
- **Tkinter** - GUI (wbudowane w Python)
- **psutil 5.9.8** - informacje o interfejsach sieciowych
- **cryptography 42.0.5** - wsparcie dla analizy kryptograficznej

## 11. Możliwe rozszerzenia

- Analiza w czasie rzeczywistym z alertami
- Integracja z bazą danych do historii skanów
- Eksport do SIEM (Security Information and Event Management)
- Machine Learning do wykrywania anomalii
- Wsparcie dla IPv6
- Analiza protokołów bezprzewodowych (WiFi)
- Dekodowanie protokołów aplikacyjnych (HTTP headers, DNS queries)

## 12. Rozwiązywanie problemów

### Problem: "Permission denied" przy przechwytywaniu
**Rozwiązanie:** Uruchom aplikację z uprawnieniami administratora

### Problem: "No such device" / brak interfejsów
**Rozwiązanie:** 
- Windows: Zainstaluj Npcap
- Linux: `sudo apt-get install libpcap-dev`
- Sprawdź czy interfejs jest aktywny

### Problem: Wolne przechwytywanie
**Rozwiązanie:** 
- Zmniejsz liczbę pakietów
- Użyj filtrów protokołów
- Zamknij inne aplikacje sieciowe

## 13. Kod źródłowy i licencja

Projekt edukacyjny - Bezpieczeństwo Sieci Komputerowych  
Rok akademicki: 2025/2026

**Uwaga:** Ten projekt został stworzony w celach edukacyjnych. Autor nie ponosi odpowiedzialności za niewłaściwe użycie oprogramowania.

## 14. Bibliografia

1. Scapy Documentation - https://scapy.readthedocs.io/
2. RFC 2616 - HTTP Protocol
3. RFC 5321 - SMTP Protocol
4. OWASP Top 10 - https://owasp.org/
5. Network Security Best Practices
6. Python Tkinter Documentation

---

**Data utworzenia dokumentacji:** 15.06.2026  
**Wersja:** 1.0
