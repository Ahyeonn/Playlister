from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

def video_url_creator(id_lst):
    videos = []
    for vid_id in id_lst: 
        video = 'https://youtube.com/embed/' + vid_id
        videos.append(video)
    return videos

uri = os.environ.get('MONGODB_URI','mongodb://mongodb:27017/Playlister')
client = MongoClient(uri)
db = client.get_default_database()
playlists = db.playlists
comments = db.comments

@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlists_new():
    """Create a new playlist."""
    return render_template('playlists_new.html', playlist={}, title='New Playlist')

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)}) 
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    video_ids = request.form.get('video_ids').split() # ["asdfasdf", "asdfsadf"]
    videos = video_url_creator(video_ids)  
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids,
        'rating': request.form.get('rating')
    }
    playlists.insert_one(playlist) 
    return redirect(url_for('playlists_show', playlist_id=playlist['_id'])) #look up playlist_id

@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))

@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)}) 
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')

@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    video_ids = request.form.get('video_ids').split()
    videos = video_url_creator(video_ids)
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids,
        'rating': request.form.get('rating')
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    comment = {
        'playlist_id':ObjectId(request.form.get('playlist_id')),
        'title': request.form.get('title'),
        'content': request.form.get('content')
    }
    comments.insert_one(comment) 
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))

@app.route('/playlists/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

