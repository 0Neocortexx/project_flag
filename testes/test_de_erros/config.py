from flask import *
app = Flask(__name__)

@app.route('/')
def roda():
    return render_template('index.html')

app.run()