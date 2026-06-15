import re
from datetime import datetime

class SecurityAnalyzer:
    def __init__(self):
        self.threats = []
        self.suspicious_patterns = {
            'password': rb'(password|passwd|pwd)[\s:=]+[\w]+',
            'api_key': rb'(api[_-]?key|apikey)[\s:=]+[\w\-]+',
            'token': rb'(token|auth)[\s:=]+[\w\-\.]+',
            'email': rb'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'credit_card': rb'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b'
        }

    def analyze_packets(self, packets):
        """Analizuj pakiety pod kątem zagrożeń bezpieczeństwa"""
        self.threats = []

        for packet in packets:
            # Sprawdź niezaszyfrowane protokoły
            if packet.get('app_protocol') in ['HTTP', 'FTP', 'SMTP']:
                self.check_unencrypted_protocol(packet)

            # Sprawdź wrażliwe dane w payload
            if packet.get('payload'):
                self.check_sensitive_data(packet)

            # Sprawdź podejrzane porty
            self.check_suspicious_ports(packet)

        return self.threats

    def check_unencrypted_protocol(self, packet):
        """Wykryj użycie niezaszyfrowanych protokołów"""
        protocol = packet.get('app_protocol')
        threat = {
            'type': 'Niezaszyfrowany protokół',
            'severity': 'ŚREDNIE' if protocol == 'HTTP' else 'WYSOKIE',
            'timestamp': packet['timestamp'],
            'details': f"Wykryto użycie niezaszyfrowanego protokołu {protocol}",
            'src_ip': packet['src_ip'],
            'dst_ip': packet['dst_ip'],
            'protocol': protocol,
            'recommendation': self.get_protocol_recommendation(protocol)
        }
        self.threats.append(threat)

    def check_sensitive_data(self, packet):
        """Wykryj wrażliwe dane w pakietach"""
        payload = packet.get('payload', b'')

        for data_type, pattern in self.suspicious_patterns.items():
            if re.search(pattern, payload, re.IGNORECASE):
                threat = {
                    'type': 'Wrażliwe dane bez szyfrowania',
                    'severity': 'KRYTYCZNE',
                    'timestamp': packet['timestamp'],
                    'details': f"Wykryto {data_type} przesyłane w niezabezpieczony sposób",
                    'src_ip': packet['src_ip'],
                    'dst_ip': packet['dst_ip'],
                    'protocol': packet.get('app_protocol', 'UNKNOWN'),
                    'data_type': data_type,
                    'recommendation': f"Użyj szyfrowanego połączenia (HTTPS/TLS) do przesyłania {data_type}"
                }
                self.threats.append(threat)

    def check_suspicious_ports(self, packet):
        """Wykryj podejrzaną aktywność na portach"""
        suspicious_ports = {
            23: 'Telnet (niezaszyfrowany)',
            69: 'TFTP (niezabezpieczony)',
            135: 'MS RPC (często wykorzystywany przez malware)',
            445: 'SMB (podatny na ataki)',
            3389: 'RDP (cel ataków brute-force)'
        }

        dst_port = packet.get('dst_port')
        if dst_port in suspicious_ports:
            threat = {
                'type': 'Podejrzana aktywność portowa',
                'severity': 'WYSOKIE',
                'timestamp': packet['timestamp'],
                'details': f"Połączenie na port {dst_port}: {suspicious_ports[dst_port]}",
                'src_ip': packet['src_ip'],
                'dst_ip': packet['dst_ip'],
                'port': dst_port,
                'recommendation': 'Rozważ zablokowanie tego portu lub użycie bezpieczniejszej alternatywy'
            }
            self.threats.append(threat)

    def get_protocol_recommendation(self, protocol):
        """Zwróć rekomendację dla danego protokołu"""
        recommendations = {
            'HTTP': 'Użyj HTTPS zamiast HTTP dla bezpiecznej komunikacji',
            'FTP': 'Użyj SFTP lub FTPS zamiast FTP',
            'SMTP': 'Użyj SMTP z TLS/SSL (port 587 lub 465)',
            'Telnet': 'Użyj SSH zamiast Telnet',
            'DNS': 'Rozważ użycie DNS over HTTPS (DoH) lub DNS over TLS (DoT)'
        }
        return recommendations.get(protocol, 'Użyj szyfrowanej wersji tego protokołu')

    def generate_summary(self):
        """Generuj podsumowanie zagrożeń"""
        if not self.threats:
            return {
                'total': 0,
                'critical': 0,
                'high': 0,
                'medium': 0,
                'message': 'Nie wykryto zagrożeń bezpieczeństwa'
            }

        severity_count = {
            'KRYTYCZNE': 0,
            'WYSOKIE': 0,
            'ŚREDNIE': 0
        }

        for threat in self.threats:
            severity = threat.get('severity', 'ŚREDNIE')
            severity_count[severity] = severity_count.get(severity, 0) + 1

        return {
            'total': len(self.threats),
            'critical': severity_count['KRYTYCZNE'],
            'high': severity_count['WYSOKIE'],
            'medium': severity_count['ŚREDNIE'],
            'threats': self.threats
        }
