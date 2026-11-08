# Attendance Tracker

A local web app to log your daily arrival and departure times, see your stats, and export to Excel. A small Python server plus a browser page. No libraries, no internet.<br><br>


**> Run:** (requires Python 3)

```
python3 server.py
```

Open http://localhost:8000 and click any workday cell to log your time. Press Ctrl+C to stop.<br><br>


**> Arrival rating:**

Best: up to 7:15. Good: 7:15 to 8:00. Fair: 8:00 to 9:30. Late: after 9:30. The Arrival rating card shows the range you land in most often.<br><br>


**> Data:**

Saved automatically in `data.json`. If you edit it by hand, change only `in`, `out` and `note`, then restart the server.<br><br>


**> Export:**

Export Excel downloads `attendance.xlsx` with two sheets: Attendance and Summary.<br><br>


**> Screenshots:**
<img width="1512" height="947" alt="Screenshot 2026-11-08 at 2 40 10 PM" src="https://github.com/user-attachments/assets/1fdceeab-9ef7-43c9-a7ff-0503366aa5e3" />
<img width="1512" height="982" alt="Screenshot 2026-11-08 at 2 40 20 PM" src="https://github.com/user-attachments/assets/05fee90e-8865-4689-a7dc-14fbccba2258" />
<img width="1512" height="942" alt="Screenshot 2026-11-08 at 2 41 52 PM" src="https://github.com/user-attachments/assets/81e157b4-f195-4cb7-a1fd-c07f9bbd18e2" />
<img width="1508" height="948" alt="Screenshot 2026-11-08 at 2 42 07 PM" src="https://github.com/user-attachments/assets/130e0dc4-8274-4525-a52b-30a721a7f725" />
