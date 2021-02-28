from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
@app.route('/home')
def home():

    return render_template('index.html')

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/contact')
def contact():

    return render_template('contact.html')

@app.route('/map')
def map_page():

    return render_template('map.html')

@app.route('/fullmap')
def full_map():

    return render_template('fullmap.html')

@app.route('/genesis')
def gen_map():

    return render_template('genesismap.html')

@app.route('/exodus')
def exo_map():

    return render_template('exodusmap.html')

@app.route('/psalms')
def psalms_map():

    return render_template('psalmsmap.html')

@app.route('/songofsolomon')
def sol_map():

    return render_template('songofsolomonmap.html')

@app.route('/hebrews')
def heb_map():

    return render_template('hebrewsmap.html')

@app.route('/matthew')
def mat_map():

    return render_template('matthewmap.html')

@app.route('/mark')
def mar_map():

    return render_template('markmap.html')

@app.route('/luke')
def luk_map():

    return render_template('lukemap.html')

@app.route('/john')
def joh_map():

    return render_template('johnmap.html')

@app.errorhandler(404)
def page_not_found():

    return render_template('404.html')

if __name__ == '__main__':
    
    app.run('127.0.0.1', port=5000, debug=False)