import http.server
import socketserver
import json
import os
from datetime import date as Date, timedelta
from urllib.parse import urlparse

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

# نفس إعدادات الصفحة (index.html)
START_DATE = Date(2026, 9, 20)
END_DATE = Date(2027, 2, 22)
WEEKEND_DAYS = [5, 6]  # الجمعة والسبت (Sunday=0 مثل JavaScript)
DAY_LABELS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
BEST_MAX_MIN = 435   # 7:15
LATE_MIN_MIN = 570   # بعد 9:30


def js_weekday(d):
    return (d.weekday() + 1) % 7  # Sunday=0


def to_minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def hours_between(t_in, t_out):
    if not t_in or not t_out:
        return None
    diff = to_minutes(t_out) - to_minutes(t_in)
    if diff < 0:
        diff += 24 * 60
    return diff / 60


def read_entries():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            obj = json.load(f)
    except Exception:
        return {}
    if isinstance(obj, dict) and isinstance(obj.get("entries"), dict):
        return obj["entries"]
    return obj if isinstance(obj, dict) else {}


def enrich(key, e):
    y, m, d = map(int, key.split("-"))
    hrs = hours_between(e.get("in"), e.get("out"))
    rec = {
        "day": DAY_LABELS[js_weekday(Date(y, m, d))],
        "in": e.get("in") or None,
        "out": e.get("out") or None,
        "hours": None if hrs is None else round(hrs, 2),
    }
    if e.get("note"):
        rec["note"] = e["note"]
    return rec


def compute_summary(entries):
    best = late = logged = arrival_sum = hours_count = 0
    hours_sum = 0.0
    cur = START_DATE
    while cur <= END_DATE:
        if js_weekday(cur) not in WEEKEND_DAYS:
            e = entries.get(cur.isoformat())
            if e and e.get("in"):
                logged += 1
                mins = to_minutes(e["in"])
                arrival_sum += mins
                if mins <= BEST_MAX_MIN:
                    best += 1
                if mins > LATE_MIN_MIN:
                    late += 1
                hrs = hours_between(e["in"], e.get("out"))
                if hrs is not None:
                    hours_sum += hrs
                    hours_count += 1
        cur += timedelta(days=1)
    avg_arrival = "-"
    if logged:
        a = round(arrival_sum / logged)
        avg_arrival = "%d:%02d" % (a // 60, a % 60)
    return {
        "best_arrival": best,
        "late_arrival": late,
        "avg_arrival": avg_arrival,
        "avg_hours": round(hours_sum / hours_count, 2) if hours_count else None,
        "logged_days": logged,
    }


def save_entries(entries):
    full = {k: enrich(k, v) for k, v in entries.items()}
    store = {"entries": full, "summary": compute_summary(full)}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2, sort_keys=True)
    return full


def load_data():
    return read_entries()


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/data":
            data = load_data()
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/save":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            status = 200
            try:
                payload = json.loads(raw.decode("utf-8"))
                date = payload.get("date")
                entry = payload.get("entry")  # {"in": "07:15", "out": "16:30", "note": "..."} or None
                if not date:
                    raise ValueError("missing date")
                Date.fromisoformat(date)  
                data = load_data()
                if entry and (entry.get("in") or entry.get("out")):
                    record = {"in": entry.get("in") or None, "out": entry.get("out") or None}
                    note = str(entry.get("note") or "").strip()
                    if note:
                        record["note"] = note[:2000]
                    data[date] = record
                else:
                    data.pop(date, None)
                data = save_entries(data)
                body = json.dumps({"ok": True, "data": data}, ensure_ascii=False).encode("utf-8")
            except Exception as e:
                status = 400
                body = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


socketserver.TCPServer.allow_reuse_address = True  # lets you restart the server right away


if __name__ == "__main__":
    os.chdir(BASE_DIR)
    save_entries(read_entries()) 
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"الخادم شغال على: http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nتم إيقاف الخادم")
