from flask import (
    Flask,
    g,
    jsonify,
    request,
)
import sqlite3

app = Flask(__name__)

DATABASE = 'chinook.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():
    return 'Hello World!'


def pager(per_page, page, query):
    if per_page is not None:
        per_page = int(per_page)
        query += f"LIMIT {per_page} "

    if page is not None:
        page = int(page)
        query += f"OFFSET {per_page * (page - 1)}"

    return query


@app.route('/tracks')
def tracks_list():
    db = get_db()
    artist = request.args.get('artist')
    per_page = request.args.get('per_page')
    page = request.args.get('page')

    if artist is not None:
        query = """SELECT tracks.Name
                              FROM tracks
                              JOIN albums ON albums.AlbumId = tracks.AlbumId
                              JOIN artists ON albums.ArtistId = artists.ArtistId
                              WHERE artists.Name = :artist
                              ORDER BY tracks.Name COLLATE NOCASE ASC """

        query = pager(per_page, page, query)
        data = db.execute(query, {'artist': artist}).fetchall()
    else:
        query = 'SELECT Name FROM tracks ORDER BY Name COLLATE NOCASE ASC '

        query = pager(per_page, page, query)
        data = db.execute(query).fetchall()
    js = []
    for elem in data:
        js.append(elem[0])
    return jsonify(js)


@app.route('/tracks', methods=['POST'])
def add_track():
    db = get_db()
    js = request.get_json()
    try:
        db.execute("""INSERT INTO tracks(Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
                         VALUES(:name, :album_id, :media_type_id, :genre_id, :composer, :milliseconds, :bytes, :price)""", js)
        db.commit()
        idx = db.execute('SELECT last_insert_rowid()').fetchone()
        js['track_id'] = idx[0]
        return jsonify(js)
    except:
        return "", 400


@app.route('/genres')
def genres_list():
    db = get_db()
    data = db.execute("""SELECT genres.Name, COUNT(tracks.TrackId)
                         FROM genres
                         JOIN tracks ON tracks.GenreId = genres.GenreId
                         GROUP BY genres.Name
                         ORDER BY genres.Name ASC""").fetchall()
    js = {}
    for elem in data:
        js[elem[0]] = elem[1]
    return jsonify(js)


if __name__ == '__main__':
    app.run(debug=True)
