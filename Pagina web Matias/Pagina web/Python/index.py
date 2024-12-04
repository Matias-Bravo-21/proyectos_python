#instalamos flask
#pip install flask

from flask import Flask, render_template
app = Flask(__name__, template_folder='../Templates')

@app.route('/')
def principal():
    return render_template('Html/Login.html')


if __name__=='__main__':
    app.run(debug=True,port="5017")