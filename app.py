from flask import Flask, request, redirect, url_for, render_template_string, flash
import sqlite3, re
from difflib import SequenceMatcher

app = Flask(__name__)
app.secret_key = "change-this-before-production"
DB = "records.db"

PAGE = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Data Redundancy Removal</title>
<style>
body{font:16px Arial;background:#f3f6fb;color:#182235;margin:0}.wrap{max-width:900px;margin:35px auto;padding:20px}
.card{background:white;padding:22px;border-radius:14px;box-shadow:0 5px 22px #18223512;margin:16px 0}
h1{margin-bottom:5px}input{padding:11px;border:1px solid #ccd4e0;border-radius:7px;margin:5px;width:27%;min-width:160px}
button{padding:11px 18px;background:#2457d6;color:white;border:0;border-radius:7px;cursor:pointer}
table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:10px;border-bottom:1px solid #e7ebf1}
.msg{padding:12px;background:#eaf1ff;border-radius:8px;margin:10px 0}.muted{color:#68758a;font-size:14px}
</style></head><body><div class="wrap">
<h1>Data Redundancy Removal System</h1><p class="muted">Validate incoming records, detect duplicates and retain unique verified data.</p>
<div class="card"><h3>Add a new record</h3>
<form method="post" action="/add">
<input name="name" placeholder="Full name" required>
<input name="email" type="email" placeholder="Email address" required>
<input name="phone" placeholder="Phone number">
<button type="submit">Validate & Save</button></form>
{% for m in messages %}<div class="msg">{{m}}</div>{% endfor %}
</div><div class="card"><h3>Stored unique records ({{records|length}})</h3>
<table><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th></tr>
{% for r in records %}<tr><td>{{r[0]}}</td><td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3]}}</td></tr>{% else %}
<tr><td colspan="4">No records yet. Add the first record above.</td></tr>{% endfor %}</table></div>
<p class="muted">Demo note: exact email/phone matches are duplicates. Similar names are flagged for manual review to reduce false positives.</p>
</div></body></html>
"""

def db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE, phone TEXT)""")
    return con

def clean(value):
    return re.sub(r"\s+", " ", (value or "").strip()).lower()

@app.route("/")
def home():
    con = db()
    records = con.execute("SELECT id,name,email,phone FROM records ORDER BY id DESC").fetchall()
    con.close()
    messages = request.args.getlist("m")
    return render_template_string(PAGE, records=records, messages=messages)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = re.sub(r"\D", "", request.form.get("phone", ""))
    if not name or not email or "@" not in email:
        return redirect(url_for("home", m="Invalid input: provide a name and valid email."))
    con = db()
    rows = con.execute("SELECT name,email,phone FROM records").fetchall()
    for old_name, old_email, old_phone in rows:
        if email == old_email.lower() or (phone and phone == re.sub(r"\D", "", old_phone or "")):
            con.close()
            return redirect(url_for("home", m="DUPLICATE DETECTED: matching email or phone. Record was not saved."))
    for old_name, old_email, old_phone in rows:
        if SequenceMatcher(None, clean(name), clean(old_name)).ratio() >= 0.88:
            con.close()
            return redirect(url_for("home", m="POSSIBLE DUPLICATE / FALSE-POSITIVE CHECK: similar name found. Review manually; record was not auto-saved."))
    try:
        con.execute("INSERT INTO records(name,email,phone) VALUES(?,?,?)", (name, email, phone))
        con.commit()
    except sqlite3.IntegrityError:
        con.close()
        return redirect(url_for("home", m="Duplicate email rejected by database constraint."))
    con.close()
    return redirect(url_for("home", m="SUCCESS: unique and verified record saved."))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
