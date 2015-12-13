from flask import Flask, render_template, request, send_file, redirect, url_for
import youtube_dl
import re
from moviepy.editor import *
app = Flask(__name__)
app.debug = True

class MyLogger(object):
	def debug(self, msg):
		pass
 
	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)


def my_hook(d):
	if d['status'] == 'finished':
		print(d['filename'])


@app.route('/')
def main():
	return render_template('index.html')

@app.route('/madeGif')
def madeGif():
	return render_template('madeGif.html')

@app.route('/dlGif',methods=['POST'])
def dlGif():
	_url = request.form['url']
	print(_url)
	filename = _url[_url.index('=')+1:]
	ydl_opts = {'outtmpl': filename,
				'postprocessors': [{
				'key': 'FFmpegVideoConvertor',
				'preferedformat': 'mp4'}],
				'logger': MyLogger(),
				'progress_hooks':[my_hook]}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([_url])
	clip = (VideoFileClip(filename+".mp4").subclip((2.65),(3.2)))
	clip.write_gif(filename+".gif")
	print("Here")
	return 'You should login! Go to back to <a href="/">the beginning<a>'

@app.route('/<file_name>')
def getGif(file_name):
	return send_file(file_name+'.gif', mimetype='image/gif')

	
if __name__ == '__main__':
	app.run()