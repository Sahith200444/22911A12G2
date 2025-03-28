from flask import Flask, render_template, request
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

TOKEN = ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQzMTUyODYzLCJpYXQiOjE3NDMxNTI1NjMsImlzcyI6IkFmZm9yZG1lZCIs"
         "Imp0aSI6ImUxMTMxNzE1LTZiMzAtNDdiNS1iMTBkLTUxMzIwZWE2ZWU5ZCIsInN1YiI6IjIyOTExYTEyZzJAdmppdC5hYy5pbiJ9LCJjb21wYW55TmFtZSI6"
         "IkFmZm9ybWVkIiwiY2xpZW50SUQiOiJlMTEzMTcxNS02YjMwLTQ3YjUtYjEwZC01MTMyMGVhNmVlOWQiLCJjbGllbnRTZWNyZXQiOiJDTEhGV2Z2a1BJQWd0UEht"
         "Iiwib3duZXJOYW1lIjoiTSBTYWhpdGggcmVkZHkiLCJvd25lckVtYWlsIjoiMjI5MTFhMTJnMkB2aml0LmFjLmluIiwicm9sbE5vIjoiMjI5MTFBMTJHMiJ9."
         "SEA5RB51dVmmVfqC_EgaXL6XWvohXQyoWKp5MW7F9So")
BASE_URL = "http://20.244.56.144/test"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def signup():
    msg = None
    if request.method == "POST":
        comp = request.form.get("companyName")
        ownr = request.form.get("ownerName")
        mail = request.form.get("ownerEmail")
        roll = request.form.get("rollNo")
        code = request.form.get("accessCode")
        payload = {"companyName": comp, "ownerName": ownr, "ownerEmail": mail, "rollNo": roll, "accessCode": code}
        try:
            r = requests.post(f"{BASE_URL}/register", json=payload)
            if r.status_code in (200, 201):
                msg = "Registration successful!"
            else:
                msg = f"Registration failed (Status {r.status_code}): {r.text}"
        except Exception as e:
            msg = f"Error: {str(e)}"
    return render_template("register.html", message=msg)



@app.route("/users")
def users():
    hdr = {"Authorization": TOKEN, "Content-Type": "application/json"}
    logging.debug("Fetching users with %s", hdr)
    resp = requests.get(f"{BASE_URL}/users", headers=hdr)
    logging.debug("Status: %s, Body: %s", resp.status_code, resp.text)
    if resp.status_code != 200:
        return render_template("users.html", error=f"Failed to fetch users. Status code: {resp.status_code}")
    data = resp.json()
    return render_template("users.html", users=data)




@app.route("/posts")
def posts():
    hdr = {"Authorization": TOKEN, "Content-Type": "application/json"}
    logging.debug("Fetching posts with %s", hdr)
    resp = requests.get(f"{BASE_URL}/posts", headers=hdr)
    logging.debug("Status: %s, Body: %s", resp.status_code, resp.text)
    if resp.status_code != 200:
        return render_template("posts.html", error=f"Failed to fetch posts. Status code: {resp.status_code}")
    data = resp.json()
    return render_template("posts.html", posts=data)
@app.route("/posts/<int:pid>/comments")
def comments(pid):
    hdr = {"Authorization": TOKEN, "Content-Type": "application/json"}
    logging.debug("Fetching comments for post %s with %s", pid, hdr)
    resp = requests.get(f"{BASE_URL}/posts/{pid}/comments", headers=hdr)
    logging.debug("Status: %s, Body: %s", resp.status_code, resp.text)
    if resp.status_code != 200:
        return render_template("post_comments.html", error=f"Failed to fetch comments for post {pid}. Status code: {resp.status_code}", post_id=pid)
    data = resp.json()
    return render_template("post_comments.html", comments=data, post_id=pid)

if __name__ == "__main__":
    app.run(debug=True)
