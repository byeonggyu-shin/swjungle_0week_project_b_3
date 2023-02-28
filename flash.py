from flask import Flask, request, render_template, flash, jsonify

app = Flask(__name__)
app.secret_key = '사용자지정비밀번호'

@app.route("/login", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        id = request.form.get("id")
        pw = request.form.get("pw")

        if id == "":
            flash("Please Input ID")
            return render_template("login.html")
        elif pw == "":
            flash("Please Input PW")
            return render_template("login.html")
        else:
            return jsonify({"Login": "Completed"})
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=9999)