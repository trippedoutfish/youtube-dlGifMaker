# Written by Doug Alexander, many thanks to documentations and stackoverflow for helping me get as far as I did
from flask import Flask, render_template, request, send_file
import youtube_dl
from moviepy.editor import *
app = Flask(__name__)
app.debug = True

#Logger for Youtube-DL
class MyLogger(object):
	#Print msg if you want to see debug messages
	def debug(self, msg):
		print(msg)
 
	#Prints warnings
	def warning(self, msg):
		print(msg)

	#Prints any errors
	def error(self, msg):
		print(msg)

#Hook to tell when Youtube-DL is done, does nothing useful at the moment.
def my_hook(d):
	if d['status'] == 'finished':
		pass

#Root site displays simple button
@app.route('/')
def main():
	return render_template('index.html')

#Template for grabbing the video
@app.route('/madeGif')
def madeGif():
	return render_template('madeGif.html')

#Ajax request routes to here automagically
@app.route('/dlGif',methods=['POST'])
def dlGif():
	#Needs to be a valid current youtube url
	_url = request.form['url']
	#Needs to be an float smaller than video length
	_start = request.form['start']
	#Needs to be an float less than or equal to video length
	_end = request.form['end']
	#Print information to console
	print(_url)
	print(_start)
	print(_end)
	#Decide on filename based on URL
	filename = _url[_url.index('=')+1:]
	#Define downloader options - Yes prefered is spelt wrong, I should probably submit a ticket about that it took me about an hour of debugging to discover
	ydl_opts = {'outtmpl': filename,
				'postprocessors': [{
				'key': 'FFmpegVideoConvertor',
				'preferedformat': 'mp4'}],
				'logger': MyLogger(),
				'progress_hooks':[my_hook]}
	#Download clip
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([_url])
	#Make the gif
	clip = (VideoFileClip(filename+".mp4").subclip(float(_start),float(_end)))
	clip.write_gif(filename+".gif")
	#Finished
	print("Done.")
	return "I can put whatever here and it does nothing"

#Need to call file by filename with no extension
@app.route('/<file_name>')
def getGif(file_name):
	return send_file(file_name+'.gif', mimetype='image/gif')

if __name__ == '__main__':
	app.run()