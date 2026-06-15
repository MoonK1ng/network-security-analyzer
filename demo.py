#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script - przykładowe dane dla Network Security Analyzer
Generuje symulowane wyniki analizy dla celów demonstracyjnych
"""

import sys
import io
from datetime import datetime
from security_analyzer import SecurityAnalyzer
from report_generator import ReportGenerator

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generate_demo_data():
    """Generuj przykładowe dane pakietów do demonstracji"""

    demo_packets = [
        # HTTP traffic - niezaszyfrowany
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '93.184.216.34',
            'src_port': 54321,
            'dst_port': 80,
            'app_protocol': 'HTTP',
            'protocol': 6,
            'size': 512,
            'payload': b'GET /index.html HTTP/1.1\r\nHost: example.com\r\n'
        },
        # FTP z hasłem
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '192.168.1.50',
            'src_port': 49152,
            'dst_port': 21,
            'app_protocol': 'FTP',
            'protocol': 6,
            'size': 256,
            'payload': b'USER admin\r\nPASS password123\r\n'
        },
        # HTTPS - bezpieczny
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '142.250.185.46',
            'src_port': 54322,
            'dst_port': 443,
            'app_protocol': 'HTTPS',
            'protocol': 6,
            'size': 1024,
            'payload': b'\x16\x03\x01\x00\x85'  # TLS handshake
        },
        # RDP connection - podejrzany port
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '192.168.1.10',
            'src_port': 54323,
            'dst_port': 3389,
            'app_protocol': 'OTHER',
            'protocol': 6,
            'size': 512,
            'payload': b''
        },
        # SMTP bez TLS
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '192.168.1.25',
            'src_port': 54324,
            'dst_port': 25,
            'app_protocol': 'SMTP',
            'protocol': 6,
            'size': 384,
            'payload': b'MAIL FROM:<user@example.com>\r\n'
        },
        # HTTP z kluczem API
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '203.0.113.50',
            'src_port': 54325,
            'dst_port': 80,
            'app_protocol': 'HTTP',
            'protocol': 6,
            'size': 768,
            'payload': b'Authorization: Bearer api_key=sk_test_123456789abcdef\r\n'
        },
        # DNS query - normalny
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '8.8.8.8',
            'src_port': 54326,
            'dst_port': 53,
            'app_protocol': 'DNS',
            'protocol': 17,
            'size': 128,
            'payload': b'\x00\x01\x01\x00\x00\x01\x00\x00'
        },
        # Telnet - bardzo niebezpieczny
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '192.168.1.20',
            'src_port': 54327,
            'dst_port': 23,
            'app_protocol': 'OTHER',
            'protocol': 6,
            'size': 256,
            'payload': b'login: admin\r\n'
        },
        # SMB connection - podatny protokół
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '192.168.1.30',
            'src_port': 54328,
            'dst_port': 445,
            'app_protocol': 'OTHER',
            'protocol': 6,
            'size': 512,
            'payload': b''
        },
        # HTTP z tokenem autoryzacyjnym
        {
            'timestamp': datetime.now(),
            'src_ip': '192.168.1.100',
            'dst_ip': '198.51.100.10',
            'src_port': 54329,
            'dst_port': 80,
            'app_protocol': 'HTTP',
            'protocol': 6,
            'size': 640,
            'payload': b'POST /api/login HTTP/1.1\r\nAuthorization: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\r\n'
        }
    ]

    return demo_packets

def main():
    print("=" * 70)
    print("Network Security Analyzer - Demonstracja")
    print("=" * 70)
    print("\nGenerowanie przykładowych danych...\n")

    # Generuj demo pakiety
    packets = generate_demo_data()
    print(f"✓ Wygenerowano {len(packets)} przykładowych pakietów")

    # Analizuj
    print("\nAnaliza bezpieczeństwa...")
    analyzer = SecurityAnalyzer()
    threats = analyzer.analyze_packets(packets)
    summary = analyzer.generate_summary()

    print(f"✓ Wykryto {summary['total']} zagrożeń:")
    print(f"  - Krytyczne: {summary['critical']}")
    print(f"  - Wysokie: {summary['high']}")
    print(f"  - Średnie: {summary['medium']}")

    # Generuj raporty
    print("\nGenerowanie raportów...")
    reporter = ReportGenerator()

    txt_file = reporter.generate_text_report(summary, 'demo_report.txt')
    print(f"✓ Raport tekstowy: {txt_file}")

    html_file = reporter.generate_html_report(summary, 'demo_report.html')
    print(f"✓ Raport HTML: {html_file}")

    json_file = reporter.generate_json_report(summary, 'demo_report.json')
    print(f"✓ Raport JSON: {json_file}")

    print("\n" + "=" * 70)
    print("Demo zakończone!")
    print("Otwórz demo_report.html w przeglądarce aby zobaczyć wyniki")
    print("=" * 70)

if __name__ == "__main__":
    main()
