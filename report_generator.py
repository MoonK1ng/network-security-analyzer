from datetime import datetime
import json

class ReportGenerator:
    def __init__(self):
        pass

    def generate_text_report(self, analysis_summary, output_file='security_report.txt'):
        """Generuj raport tekstowy"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RAPORT BEZPIECZEŃSTWA SIECI\n")
            f.write("=" * 70 + "\n")
            f.write(f"Data generowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("PODSUMOWANIE\n")
            f.write("-" * 70 + "\n")
            f.write(f"Całkowita liczba zagrożeń: {analysis_summary['total']}\n")
            f.write(f"  - Krytyczne: {analysis_summary['critical']}\n")
            f.write(f"  - Wysokie: {analysis_summary['high']}\n")
            f.write(f"  - Średnie: {analysis_summary['medium']}\n\n")

            if analysis_summary['total'] == 0:
                f.write(analysis_summary['message'] + "\n")
                return output_file

            f.write("SZCZEGÓŁOWE ZAGROŻENIA\n")
            f.write("=" * 70 + "\n\n")

            for idx, threat in enumerate(analysis_summary.get('threats', []), 1):
                f.write(f"[{idx}] {threat['type']}\n")
                f.write(f"Poziom zagrożenia: {threat['severity']}\n")
                f.write(f"Czas: {threat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Źródło: {threat['src_ip']}\n")
                f.write(f"Cel: {threat['dst_ip']}\n")
                f.write(f"Protokół: {threat.get('protocol', 'N/A')}\n")
                f.write(f"Szczegóły: {threat['details']}\n")
                f.write(f"Rekomendacja: {threat['recommendation']}\n")
                f.write("-" * 70 + "\n\n")

        return output_file

    def generate_json_report(self, analysis_summary, output_file='security_report.json'):
        """Generuj raport JSON"""
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total': analysis_summary['total'],
                'critical': analysis_summary['critical'],
                'high': analysis_summary['high'],
                'medium': analysis_summary['medium']
            },
            'threats': []
        }

        for threat in analysis_summary.get('threats', []):
            threat_data = threat.copy()
            threat_data['timestamp'] = threat['timestamp'].isoformat()
            report_data['threats'].append(threat_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        return output_file

    def generate_html_report(self, analysis_summary, output_file='security_report.html'):
        """Generuj raport HTML"""
        html_content = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raport Bezpieczeństwa Sieci</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .summary-box {{ flex: 1; padding: 20px; border-radius: 5px; color: white; text-align: center; }}
        .critical {{ background: #dc3545; }}
        .high {{ background: #fd7e14; }}
        .medium {{ background: #ffc107; }}
        .threat {{ border: 1px solid #ddd; margin: 15px 0; padding: 15px; border-radius: 5px; background: #fafafa; }}
        .threat-header {{ font-weight: bold; color: #007bff; margin-bottom: 10px; font-size: 1.1em; }}
        .severity {{ display: inline-block; padding: 5px 10px; border-radius: 3px; color: white; font-size: 0.9em; }}
        .severity-critical {{ background: #dc3545; }}
        .severity-high {{ background: #fd7e14; }}
        .severity-medium {{ background: #ffc107; }}
        .detail-row {{ margin: 5px 0; }}
        .label {{ font-weight: bold; color: #555; }}
        .recommendation {{ background: #e7f3ff; border-left: 4px solid #007bff; padding: 10px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Raport Bezpieczeństwa Sieci</h1>
        <p><strong>Data generowania:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <h2>Podsumowanie</h2>
        <div class="summary">
            <div class="summary-box critical">
                <h3>{analysis_summary['critical']}</h3>
                <p>Krytyczne</p>
            </div>
            <div class="summary-box high">
                <h3>{analysis_summary['high']}</h3>
                <p>Wysokie</p>
            </div>
            <div class="summary-box medium">
                <h3>{analysis_summary['medium']}</h3>
                <p>Średnie</p>
            </div>
        </div>

        <h2>Wykryte zagrożenia ({analysis_summary['total']})</h2>
"""

        if analysis_summary['total'] == 0:
            html_content += f"<p>{analysis_summary['message']}</p>"
        else:
            for idx, threat in enumerate(analysis_summary.get('threats', []), 1):
                severity_class = threat['severity'].lower().replace('ś', 's').replace('ó', 'o')
                if severity_class == 'srednie':
                    severity_class = 'medium'
                elif severity_class == 'krytyczne':
                    severity_class = 'critical'
                elif severity_class == 'wysokie':
                    severity_class = 'high'

                html_content += f"""
        <div class="threat">
            <div class="threat-header">
                [{idx}] {threat['type']}
                <span class="severity severity-{severity_class}">{threat['severity']}</span>
            </div>
            <div class="detail-row"><span class="label">Czas:</span> {threat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</div>
            <div class="detail-row"><span class="label">Źródło:</span> {threat['src_ip']}</div>
            <div class="detail-row"><span class="label">Cel:</span> {threat['dst_ip']}</div>
            <div class="detail-row"><span class="label">Protokół:</span> {threat.get('protocol', 'N/A')}</div>
            <div class="detail-row"><span class="label">Szczegóły:</span> {threat['details']}</div>
            <div class="recommendation">
                <strong>Rekomendacja:</strong> {threat['recommendation']}
            </div>
        </div>
"""

        html_content += """
    </div>
</body>
</html>"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return output_file
