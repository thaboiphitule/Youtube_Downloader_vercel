from flask import Flask, render_template, flash, request, send_file, session, redirect
from pytube import YouTube

app = Flask(__name__)
app.secret_key = "admin"

@app.route('/')
def index():
    link = ""
    return render_template('youtube_index.html')

@app.route('/view', methods=['POST', 'GET'])
def view():
    session['input'] = str(request.form['link'])
    yt = YouTube(session['input'])
    flash("Title: " + yt.title, 'category1')
    flash("Views: " + str(yt.views), 'category1')
    flash(str(yt.thumbnail_url), 'thumbnail')

    count = 0
    streams = yt.streams.filter(res=str(request.form['res']))
    for stream in streams:
        count +=1
        flash("Stream" + str(count) + " Size(MB):" + str(stream.filesize_mb) + "," + " itag:" + str(stream.itag) + "," + " " + stream.resolution, 'category2')
    return render_template('initiate.html')

@app.route('/download', methods=['POST', 'GET'])
def download():
    input = session.get('input')
    yn = YouTube(input)
    yd = yn.streams.get_by_itag(int(request.form['itag']))
    return send_file(yd.download(), mimetype='video/mp4'), redirect('/')    
