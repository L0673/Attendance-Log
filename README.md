# Attendance Tracker

A local web app to log your daily arrival and departure times, see your stats, and export to Excel. A small Python server plus a browser page. No libraries, no internet.


**Run** (requires Python 3)

```
python3 server.py
```

Open http://localhost:8000 and click any workday cell to log your time. Press Ctrl+C to stop.


**Arrival rating**

Best: up to 7:15. Good: 7:15 to 8:00. Fair: 8:00 to 9:30. Late: after 9:30. The Arrival rating card shows the range you land in most often.


**Data**

Saved automatically in `data.json`. If you edit it by hand, change only `in`, `out` and `note`, then restart the server.


**Export**

Export Excel downloads `attendance.xlsx` with two sheets: Attendance and Summary.


**Screenshots**
<img width="1502" height="937" alt="Screenshot 2026-10-02 at 10 19 35 PM" src="https://github.com/user-attachments/assets/a7070370-8fa3-4f68-9792-585bcd552e69" />
<img width="1512" height="982" alt="Screenshot 2026-10-02 at 10 20 17 PM" src="https://github.com/user-attachments/assets/adbf6c65-ade6-44fc-86e7-ac4050380b28" />
