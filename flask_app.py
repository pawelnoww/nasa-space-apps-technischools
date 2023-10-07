from flask import Flask, render_template

# Create a Flask web application
app = Flask(__name__)


# Define a route to display "Hello, World!"
@app.route('/')
def hello_world():
    return render_template('index.html')


@app.get('/features')
def features():
    urls = [
        {'name': 'Plots', 'address': 'http://127.0.0.1:8050/'},
        {'name': 'Meteorite map', 'address': 'https://j3rzy.dev/nasa/'}
    ]
    return render_template('features_page.html', urls=urls)


# Run the app if this script is executed
if __name__ == '__main__':
    app.run()
