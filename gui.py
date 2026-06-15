import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import psutil
from packet_capture import PacketCapture
from security_analyzer import SecurityAnalyzer
from report_generator import ReportGenerator

class NetworkSecurityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Security Analyzer")
        self.root.geometry("900x700")

        self.packet_capture = PacketCapture()
        self.security_analyzer = SecurityAnalyzer()
        self.report_generator = ReportGenerator()

        self.setup_ui()

    def setup_ui(self):
        # Ramka kontrolna
        control_frame = ttk.LabelFrame(self.root, text="Kontrola", padding=10)
        control_frame.pack(fill="x", padx=10, pady=5)

        # Wybór interfejsu
        ttk.Label(control_frame, text="Interfejs sieciowy:").grid(row=0, column=0, padx=5, pady=5)
        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(control_frame, textvariable=self.interface_var, width=30)
        self.interface_combo['values'] = self.get_network_interfaces()
        if self.interface_combo['values']:
            self.interface_combo.current(0)
        self.interface_combo.grid(row=0, column=1, padx=5, pady=5)

        # Liczba pakietów
        ttk.Label(control_frame, text="Liczba pakietów:").grid(row=0, column=2, padx=5, pady=5)
        self.packet_count_var = tk.StringVar(value="100")
        packet_entry = ttk.Entry(control_frame, textvariable=self.packet_count_var, width=10)
        packet_entry.grid(row=0, column=3, padx=5, pady=5)

        # Przyciski
        self.start_btn = ttk.Button(control_frame, text="Rozpocznij przechwytywanie", command=self.start_capture)
        self.start_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.stop_btn = ttk.Button(control_frame, text="Zatrzymaj", command=self.stop_capture, state="disabled")
        self.stop_btn.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        self.analyze_btn = ttk.Button(control_frame, text="Analizuj", command=self.analyze_packets, state="disabled")
        self.analyze_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.report_btn = ttk.Button(control_frame, text="Generuj raport", command=self.generate_report, state="disabled")
        self.report_btn.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        # Status
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill="x", padx=10, pady=5)

        self.status_label = ttk.Label(status_frame, text="Gotowy do pracy", foreground="green")
        self.status_label.pack()

        # Statystyki
        stats_frame = ttk.LabelFrame(self.root, text="Statystyki", padding=10)
        stats_frame.pack(fill="x", padx=10, pady=5)

        stats_inner = ttk.Frame(stats_frame)
        stats_inner.pack()

        ttk.Label(stats_inner, text="Przechwycone pakiety:").grid(row=0, column=0, padx=10, sticky="w")
        self.packets_label = ttk.Label(stats_inner, text="0", foreground="blue")
        self.packets_label.grid(row=0, column=1, padx=10, sticky="w")

        ttk.Label(stats_inner, text="Wykryte zagrożenia:").grid(row=0, column=2, padx=10, sticky="w")
        self.threats_label = ttk.Label(stats_inner, text="0", foreground="red")
        self.threats_label.grid(row=0, column=3, padx=10, sticky="w")

        # Notebook z wynikami
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab pakiety
        packets_frame = ttk.Frame(self.notebook)
        self.notebook.add(packets_frame, text="Pakiety")

        self.packets_text = scrolledtext.ScrolledText(packets_frame, wrap=tk.WORD, height=15)
        self.packets_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Tab zagrożenia
        threats_frame = ttk.Frame(self.notebook)
        self.notebook.add(threats_frame, text="Zagrożenia")

        self.threats_text = scrolledtext.ScrolledText(threats_frame, wrap=tk.WORD, height=15)
        self.threats_text.pack(fill="both", expand=True, padx=5, pady=5)

    def get_network_interfaces(self):
        """Pobierz listę interfejsów sieciowych"""
        interfaces = []
        try:
            addrs = psutil.net_if_addrs()
            for interface_name in addrs.keys():
                interfaces.append(interface_name)
        except Exception as e:
            print(f"Błąd pobierania interfejsów: {e}")
        return interfaces

    def start_capture(self):
        """Rozpocznij przechwytywanie pakietów"""
        try:
            interface = self.interface_var.get()
            packet_count = int(self.packet_count_var.get())

            if packet_count <= 0:
                messagebox.showerror("Błąd", "Liczba pakietów musi być większa od 0")
                return

            self.packets_text.delete(1.0, tk.END)
            self.threats_text.delete(1.0, tk.END)

            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.analyze_btn.config(state="disabled")
            self.report_btn.config(state="disabled")

            self.status_label.config(text="Przechwytywanie pakietów...", foreground="orange")

            success = self.packet_capture.start_capture(interface=interface, packet_count=packet_count)

            if success:
                self.root.after(1000, self.check_capture_status)
            else:
                messagebox.showerror("Błąd", "Przechwytywanie jest już aktywne")
                self.reset_buttons()

        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa liczba pakietów")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się rozpocząć przechwytywania: {e}")
            self.reset_buttons()

    def check_capture_status(self):
        """Sprawdź status przechwytywania"""
        packets = self.packet_capture.get_packets()
        self.packets_label.config(text=str(len(packets)))

        if self.packet_capture.is_capturing:
            self.root.after(1000, self.check_capture_status)
        else:
            self.on_capture_complete()

    def stop_capture(self):
        """Zatrzymaj przechwytywanie"""
        self.packet_capture.stop_capture()
        self.status_label.config(text="Przechwytywanie zatrzymane", foreground="blue")

    def on_capture_complete(self):
        """Obsłuż zakończenie przechwytywania"""
        self.reset_buttons()
        self.analyze_btn.config(state="normal")
        self.status_label.config(text="Przechwytywanie zakończone", foreground="green")

        packets = self.packet_capture.get_packets()
        self.display_packets(packets)

    def display_packets(self, packets):
        """Wyświetl przechwycone pakiety"""
        self.packets_text.delete(1.0, tk.END)

        if not packets:
            self.packets_text.insert(tk.END, "Brak przechwyconych pakietów\n")
            return

        self.packets_text.insert(tk.END, f"Przechwycono {len(packets)} pakietów:\n\n")

        for idx, packet in enumerate(packets[:50], 1):
            info = f"[{idx}] {packet['timestamp'].strftime('%H:%M:%S')} | "
            info += f"{packet['src_ip']}:{packet.get('src_port', 'N/A')} → "
            info += f"{packet['dst_ip']}:{packet.get('dst_port', 'N/A')} | "
            info += f"{packet.get('app_protocol', 'UNKNOWN')} | "
            info += f"{packet['size']} bytes\n"
            self.packets_text.insert(tk.END, info)

        if len(packets) > 50:
            self.packets_text.insert(tk.END, f"\n... i {len(packets) - 50} więcej pakietów\n")

    def analyze_packets(self):
        """Analizuj pakiety"""
        packets = self.packet_capture.get_packets()

        if not packets:
            messagebox.showwarning("Uwaga", "Brak pakietów do analizy")
            return

        self.status_label.config(text="Analiza pakietów...", foreground="orange")
        self.root.update()

        threats = self.security_analyzer.analyze_packets(packets)
        self.analysis_summary = self.security_analyzer.generate_summary()

        self.threats_label.config(text=str(len(threats)))
        self.display_threats()

        self.report_btn.config(state="normal")
        self.status_label.config(text="Analiza zakończona", foreground="green")

    def display_threats(self):
        """Wyświetl wykryte zagrożenia"""
        self.threats_text.delete(1.0, tk.END)

        summary = self.analysis_summary

        self.threats_text.insert(tk.END, "=== PODSUMOWANIE ZAGROŻEŃ ===\n\n")
        self.threats_text.insert(tk.END, f"Całkowita liczba: {summary['total']}\n")
        self.threats_text.insert(tk.END, f"Krytyczne: {summary['critical']}\n")
        self.threats_text.insert(tk.END, f"Wysokie: {summary['high']}\n")
        self.threats_text.insert(tk.END, f"Średnie: {summary['medium']}\n\n")

        if summary['total'] == 0:
            self.threats_text.insert(tk.END, summary['message'] + "\n")
            return

        self.threats_text.insert(tk.END, "=== SZCZEGÓŁY ===\n\n")

        for idx, threat in enumerate(summary.get('threats', []), 1):
            self.threats_text.insert(tk.END, f"[{idx}] {threat['type']} - {threat['severity']}\n")
            self.threats_text.insert(tk.END, f"Czas: {threat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.threats_text.insert(tk.END, f"Źródło: {threat['src_ip']} → Cel: {threat['dst_ip']}\n")
            self.threats_text.insert(tk.END, f"Protokół: {threat.get('protocol', 'N/A')}\n")
            self.threats_text.insert(tk.END, f"Szczegóły: {threat['details']}\n")
            self.threats_text.insert(tk.END, f"Rekomendacja: {threat['recommendation']}\n")
            self.threats_text.insert(tk.END, "-" * 70 + "\n\n")

    def generate_report(self):
        """Generuj raporty"""
        try:
            txt_file = self.report_generator.generate_text_report(self.analysis_summary)
            html_file = self.report_generator.generate_html_report(self.analysis_summary)
            json_file = self.report_generator.generate_json_report(self.analysis_summary)

            message = f"Raporty wygenerowane:\n\n"
            message += f"- {txt_file}\n"
            message += f"- {html_file}\n"
            message += f"- {json_file}"

            messagebox.showinfo("Sukces", message)
            self.status_label.config(text="Raporty wygenerowane", foreground="green")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wygenerować raportów: {e}")

    def reset_buttons(self):
        """Przywróć stan przycisków"""
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

def main():
    root = tk.Tk()
    app = NetworkSecurityGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
