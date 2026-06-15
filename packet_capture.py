from scapy.all import sniff, IP, TCP, UDP, Raw
from datetime import datetime
import threading

class PacketCapture:
    def __init__(self):
        self.captured_packets = []
        self.is_capturing = False
        self.capture_thread = None

    def start_capture(self, interface=None, packet_count=100):
        """Rozpocznij przechwytywanie pakietów"""
        if self.is_capturing:
            return False

        self.is_capturing = True
        self.captured_packets = []

        def capture():
            try:
                sniff(iface=interface, prn=self.process_packet,
                      count=packet_count, store=False)
            except Exception as e:
                print(f"Błąd przechwytywania: {e}")
            finally:
                self.is_capturing = False

        self.capture_thread = threading.Thread(target=capture, daemon=True)
        self.capture_thread.start()
        return True

    def stop_capture(self):
        """Zatrzymaj przechwytywanie"""
        self.is_capturing = False

    def process_packet(self, packet):
        """Przetwórz przechwycony pakiet"""
        if not IP in packet:
            return

        packet_info = {
            'timestamp': datetime.now(),
            'src_ip': packet[IP].src,
            'dst_ip': packet[IP].dst,
            'protocol': packet[IP].proto,
            'size': len(packet)
        }

        if TCP in packet:
            packet_info['src_port'] = packet[TCP].sport
            packet_info['dst_port'] = packet[TCP].dport
            packet_info['transport'] = 'TCP'

            if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                packet_info['app_protocol'] = 'HTTP'
            elif packet[TCP].dport == 443 or packet[TCP].sport == 443:
                packet_info['app_protocol'] = 'HTTPS'
            elif packet[TCP].dport == 21 or packet[TCP].sport == 21:
                packet_info['app_protocol'] = 'FTP'
            elif packet[TCP].dport == 25 or packet[TCP].sport == 25:
                packet_info['app_protocol'] = 'SMTP'
            else:
                packet_info['app_protocol'] = 'OTHER'

        elif UDP in packet:
            packet_info['src_port'] = packet[UDP].sport
            packet_info['dst_port'] = packet[UDP].dport
            packet_info['transport'] = 'UDP'

            if packet[UDP].dport == 53 or packet[UDP].sport == 53:
                packet_info['app_protocol'] = 'DNS'
            else:
                packet_info['app_protocol'] = 'OTHER'

        if Raw in packet:
            packet_info['payload'] = bytes(packet[Raw].load)
        else:
            packet_info['payload'] = b''

        self.captured_packets.append(packet_info)

    def get_packets(self):
        """Pobierz przechwycone pakiety"""
        return self.captured_packets
