#!/usr/bin/python3
from flask import Flask, render_template, redirect, make_response, request, url_for, json
app = Flask(__name__)

@app.route("/")
def home():
	ck = request.cookies.get('ck')
	ck = json.loads(ck)
	return render_template('home.html', ck = ck)

@app.route("/nice", methods=["POST"])
def MakeNice():
	inputUrl = request.form['inputUrl']
	niceUrl = request.form['niceUrl']
	if takeUrl(niceUrl) == '':
		with open('urls.txt', 'a') as f:
			f.write(niceUrl + ' ' + inputUrl + '\n')
		free = 1
	else:
		free = 0
	resp = make_response(redirect(url_for('home')))
	ck = {'inputUrl': inputUrl, 'niceUrl': niceUrl, 'niceFull': 'http://'+request.headers['Host']+'/'+niceUrl, 'free': free}
	resp.set_cookie('ck', json.dumps(ck))
	return resp

@app.route("/<link>")
def follow(link):
	return redirect(takeUrl(link))

def takeUrl(niceUrl):
	with open('urls.txt', 'r') as f:
		for line in f:
			if line.split(' ')[0]==niceUrl:
				return line.split(' ')[1].rstrip('\n')
	return ''

if __name__ == "__main__":
	app.run(debug=True)