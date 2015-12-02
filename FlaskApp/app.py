from flask import Flask, render_template
import youtube_dl, requests
app = Flask(__name__)
app.debug = True

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/madeGif')
def madeGif():
	#_url = request.form['url']
	ydl_opts = {}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download(["https://www.youtube.com/watch?v=sqV3pL5x8PI"])
	return render_template('madeGif.html')
	
if __name__ == '__main__':
	app.run()