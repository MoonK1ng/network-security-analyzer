# SPRAWOZDANIE Z PROJEKTU KOLOKWIUM
## Bezpieczeństwo Sieci Komputerowych

---

### Dane podstawowe

**Autor:** [Wpisz swoje imię i nazwisko]  
**Grupa:** [Wpisz swoją grupę]  
**Wariant:** 3 - Aplikacja do analizy bezpieczeństwa protokołów sieciowych  
**Data:** 15.06.2026

---

## 1. Cel projektu

Celem projektu było stworzenie aplikacji w języku Python do monitorowania i analizy bezpieczeństwa ruchu sieciowego. Aplikacja ma za zadanie:

- Przechwytywać pakiety sieciowe w czasie rzeczywistym
- Analizować protokoły komunikacyjne (HTTP, HTTPS, DNS, FTP, SMTP)
- Wykrywać zagrożenia bezpieczeństwa
- Generować szczegółowe raporty

## 2. Zakres realizacji

### 2.1 Zrealizowane funkcjonalności

✅ **Przechwytywanie pakietów sieciowych**
- Wykorzystanie biblioteki Scapy do sniffingu
- Obsługa wielu interfejsów sieciowych
- Identyfikacja protokołów warstwy aplikacji
- Przechwytywanie asynchroniczne (osobny wątek)

✅ **Analiza bezpieczeństwa**
- Wykrywanie niezaszyfrowanych protokołów (HTTP, FTP, SMTP, Telnet)
- Skanowanie payloadów pod kątem wrażliwych danych (hasła, tokeny, API keys)
- Identyfikacja podejrzanej aktywności portowej
- Klasyfikacja zagrożeń: KRYTYCZNE, WYSOKIE, ŚREDNIE

✅ **Generowanie raportów**
- Format tekstowy (TXT) - do wydruku
- Format HTML - z wizualizacją i kolorami
- Format JSON - do dalszego przetwarzania

✅ **Interfejs graficzny (GUI)**
- Intuicyjny interfejs Tkinter
- Wybór interfejsu sieciowego
- Kontrola procesu przechwytywania
- Wyświetlanie wyników w zakładkach
- Generowanie raportów jednym kliknięciem

### 2.2 Zastosowane technologie

| Technologia | Wersja | Zastosowanie |
|-------------|--------|--------------|
| Python | 3.8+ | Język programowania |
| Scapy | 2.5.0 | Przechwytywanie pakietów |
| Tkinter | Built-in | Interfejs graficzny |
| psutil | 5.9.8 | Informacje o interfejsach |
| cryptography | 42.0.5 | Wsparcie kryptograficzne |

## 3. Architektura aplikacji

### 3.1 Struktura modułów

```
network-security-analyzer/
├── main.py                   # Punkt wejścia
├── gui.py                    # Interfejs GUI
├── packet_capture.py         # Przechwytywanie
├── security_analyzer.py      # Analiza zagrożeń
├── report_generator.py       # Generowanie raportów
├── demo.py                   # Demonstracja
├── requirements.txt          # Zależności
├── README.md                 # Dokumentacja
├── DOKUMENTACJA_TECHNICZNA.md
└── INSTRUKCJA_UZYTKOWNIKA.md
```

### 3.2 Przepływ danych

```
[Interfejs sieciowy]
        ↓
[PacketCapture] → Przechwytywanie pakietów
        ↓
[Lista pakietów]
        ↓
[SecurityAnalyzer] → Analiza zagrożeń
        ↓
[Lista zagrożeń]
        ↓
[ReportGenerator] → Raporty (TXT/HTML/JSON)
        ↓
[Pliki raportów]
```

## 4. Implementacja kluczowych modułów

### 4.1 PacketCapture - Przechwytywanie

**Kluczowe funkcje:**
- `start_capture()` - inicjalizacja sniffingu
- `process_packet()` - przetwarzanie pojedynczego pakietu
- `stop_capture()` - zatrzymanie operacji

**Wykrywane protokoły:**
- HTTP (port 80)
- HTTPS (port 443)
- FTP (port 21)
- SMTP (port 25)
- DNS (port 53)

### 4.2 SecurityAnalyzer - Analiza

**Metody wykrywania zagrożeń:**

1. **check_unencrypted_protocol()**
   - Wykrywa HTTP, FTP, SMTP bez szyfrowania
   - Poziom: ŚREDNIE do WYSOKIE

2. **check_sensitive_data()**
   - Regex patterns dla haseł, tokenów, API keys
   - Poziom: KRYTYCZNE

3. **check_suspicious_ports()**
   - Monitoruje porty: 23, 69, 135, 445, 3389
   - Poziom: WYSOKIE

### 4.3 ReportGenerator - Raporty

**Formaty wyjściowe:**

| Format | Zastosowanie | Cechy |
|--------|--------------|-------|
| TXT | Dokumentacja | Prosty, czytelny |
| HTML | Prezentacja | Wizualizacja, kolory |
| JSON | Integracja | Strukturalny, API-ready |

## 5. Wyniki testów

### 5.1 Test demonstracyjny

Uruchomiono skrypt `demo.py` z 10 przykładowymi pakietami:

**Wyniki:**
- Przechwycone pakiety: 10
- Wykryte zagrożenia: 11
  - Krytyczne: 3 (hasła, tokeny w HTTP)
  - Wysokie: 5 (FTP, SMTP, RDP, Telnet, SMB)
  - Średnie: 3 (HTTP bez HTTPS)

### 5.2 Przykładowe wykryte zagrożenia

1. **HTTP z hasłem FTP**
   - Protokół: FTP
   - Payload: `USER admin\r\nPASS password123`
   - Poziom: KRYTYCZNE
   - Rekomendacja: Użyj SFTP/FTPS

2. **Połączenie RDP**
   - Port: 3389
   - Poziom: WYSOKIE
   - Rekomendacja: VPN + 2FA

3. **HTTP zamiast HTTPS**
   - Protokół: HTTP
   - Poziom: ŚREDNIE
   - Rekomendacja: Migracja na HTTPS

## 6. Interfejs użytkownika

### 6.1 Główne okno aplikacji

**Sekcje:**
1. Panel kontrolny - wybór interfejsu, ustawienia
2. Przyciski akcji - Start, Stop, Analizuj, Raport
3. Status i statystyki - bieżący stan, liczniki
4. Zakładki wyników - Pakiety, Zagrożenia

### 6.2 Przykładowy workflow

```
1. Wybierz interfejs sieciowy (Wi-Fi/Ethernet)
2. Ustaw liczbę pakietów (np. 100)
3. Kliknij "Rozpocznij przechwytywanie"
4. Poczekaj na zakończenie
5. Kliknij "Analizuj"
6. Przejrzyj zagrożenia w zakładce
7. Kliknij "Generuj raport"
8. Otwórz demo_report.html w przeglądarce
```

## 7. Bezpieczeństwo i etyka

### 7.1 Wymagania prawne

⚠️ **WAŻNE:** Aplikacja wymaga świadomego użycia:
- Przechwytywanie tylko w autoryzowanych sieciach
- Zgodność z lokalnym prawem
- Brak użycia w celach nielegalnych

### 7.2 Wymagane uprawnienia

- **Windows:** Uprawnienia administratora + Npcap
- **Linux:** sudo + libpcap-dev
- **macOS:** sudo (libpcap wbudowane)

## 8. Możliwości rozwoju

### 8.1 Planowane rozszerzenia

- [ ] Analiza w czasie rzeczywistym z alertami
- [ ] Baza danych dla historii skanów
- [ ] Machine Learning do wykrywania anomalii
- [ ] Wsparcie dla IPv6
- [ ] Integracja z SIEM
- [ ] Dekodowanie zaawansowanych protokołów
- [ ] Eksport do formatu PDF
- [ ] Dashboard webowy

### 8.2 Ulepszenia wydajności

- Optymalizacja przetwarzania dużych wolumenów
- Filtrowanie pakietów na poziomie kernel (BPF)
- Kompresja raportów dla długich sesji
- Cache dla powtarzających się analiz

## 9. Wnioski

### 9.1 Osiągnięte cele

✅ Wszystkie założone cele zostały zrealizowane:
- Przechwytywanie pakietów działa poprawnie
- Analiza wykrywa realne zagrożenia
- Raporty są czytelne i użyteczne
- GUI jest intuicyjny

### 9.2 Napotkane trudności

1. **Problem:** Kodowanie UTF-8 w Windows console
   **Rozwiązanie:** Wymuszenie UTF-8 przez `io.TextIOWrapper`

2. **Problem:** Brak uprawnień do sniffingu
   **Rozwiązanie:** Dokumentacja wymagań (admin/sudo)

3. **Problem:** Identyfikacja protokołów aplikacyjnych
   **Rozwiązanie:** Analiza portów + payload patterns

### 9.3 Wnioski końcowe

Projekt udowadnia, że:
- **Niezaszyfrowane protokoły** nadal są powszechnie używane
- **Wrażliwe dane** często przesyłane bez zabezpieczeń
- **Automatyczne narzędzia** mogą wykryć podstawowe zagrożenia
- **Świadomość bezpieczeństwa** jest kluczowa

**Praktyczne zastosowania:**
- Audyt bezpieczeństwa sieci domowej
- Test aplikacji webowych
- Edukacja w zakresie cyberbezpieczeństwa
- Podstawa dla zaawansowanych narzędzi SIEM

## 10. Bibliografia

1. **Scapy Documentation** - https://scapy.readthedocs.io/
2. **RFC 2616** - Hypertext Transfer Protocol (HTTP/1.1)
3. **RFC 959** - File Transfer Protocol (FTP)
4. **RFC 5321** - Simple Mail Transfer Protocol (SMTP)
5. **OWASP Top 10** - https://owasp.org/www-project-top-ten/
6. **NIST Cybersecurity Framework** - https://www.nist.gov/cyberframework
7. **Python Official Documentation** - https://docs.python.org/3/
8. **Wireshark Display Filter Reference** - https://www.wireshark.org/docs/

## 11. Załączniki

### 11.1 Pliki projektu

- `main.py` - 30 linii
- `gui.py` - 230 linii
- `packet_capture.py` - 90 linii
- `security_analyzer.py` - 140 linii
- `report_generator.py` - 150 linii
- `demo.py` - 180 linii

**Suma:** ~820 linii kodu (bez komentarzy i pustych linii)

### 11.2 Przykładowe raporty

- `demo_report.txt` - raport tekstowy
- `demo_report.html` - raport HTML (otwórz w przeglądarce)
- `demo_report.json` - raport JSON

### 11.3 Dokumentacja

- `README.md` - podstawowa dokumentacja
- `DOKUMENTACJA_TECHNICZNA.md` - szczegóły techniczne
- `INSTRUKCJA_UZYTKOWNIKA.md` - poradnik użytkownika

---

## Oświadczenie

Oświadczam, że projekt został wykonany samodzielnie i wszystkie wykorzystane źródła zostały wskazane w bibliografii.

**Podpis:** ___________________  
**Data:** 15.06.2026

---

**Wersja sprawozdania:** 1.0  
**Ostatnia aktualizacja:** 2026-06-15
