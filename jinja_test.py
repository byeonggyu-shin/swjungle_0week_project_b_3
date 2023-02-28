from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/vars')
def vars():
    return render_template('vars.html')

@app.route('/jinja_test')
def login():
    var1 = request.args.get('var1')
    var2 = request.args.get('var2')
    return render_template('jinja_test.html', var1 = var1, var2 = var2)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="9999", debug=True)