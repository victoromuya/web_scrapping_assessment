import os
from datetime import datetime

DASHBOARD_HTML = os.path.join(os.path.dirname(__file__), "output", "dashboard.html")

def write_dashboard_section(new_records):
    """
    Appends a section to the dashboard HTML file listing new_records.
    If dashboard.html does not exist, create it with minimal HTML scaffolding.
    """
    os.makedirs(os.path.dirname(DASHBOARD_HTML), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # If file doesn't exist, create with HTML header:
    if not os.path.exists(DASHBOARD_HTML):
        with open(DASHBOARD_HTML, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n")
            f.write("<meta charset='utf-8'>\n<title>IBDB Broadway Dashboard</title>\n")
            f.write("<style>body { font-family: Arial, sans-serif; margin: 20px; }")
            f.write("table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }")
            f.write("th, td { border: 1px solid #ddd; padding: 8px; }")
            f.write("th { background-color: #f2f2f2; }\n")
            f.write("</style>\n</head>\n<body>\n")
            f.write(f"<h1>IBDB Broadway Scraper Dashboard</h1>\n")
            f.write("</body>\n</html>")

    with open(DASHBOARD_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    insert_pos = html.rfind("</body>")
    if insert_pos == -1:
        insert_pos = len(html)

    section = []
    section.append(f"<h2>New Shows Detected at {timestamp}</h2>\n")
    section.append("<table>\n<thead><tr>")
    headers = ["Title", "Date", "Theatre", "Show Type", "Detail Link"]
    for h in headers:
        section.append(f"<th>{h}</th>")
    section.append("</tr></thead>\n<tbody>\n")
    for rec in new_records:
        section.append("<tr>")
        section.append(f"<td>{rec.get('Title','')}</td>")
        section.append(f"<td>{rec.get('Date','')}</td>")
        section.append(f"<td>{rec.get('Theatre','')}</td>")
        section.append(f"<td>{rec.get('Show Type','')}</td>")
        section.append(f"<td><a href=\"{rec.get('Detail Link','')}\" target=\"_blank\">Link</a></td>")
        section.append("</tr>\n")
    section.append("</tbody>\n</table>\n")

    new_html = html[:insert_pos] + "".join(section) + html[insert_pos:]
    with open(DASHBOARD_HTML, "w", encoding="utf-8") as f:
        f.write(new_html)
