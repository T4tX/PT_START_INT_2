from flask import Flask, render_template, url_for,request
import int_2

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hostname = request.form['hostname']
        port = int(request.form['port'])
        
        output = int_2.parse_lin(username=username, password=password, hostname=hostname, PORT=port)

        return render_template('index.html', output=output.get_info())

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)