import os

import json

import psycopg2
from flask import Flask, abort, render_template, request, jsonify
from sqlalchemy import create_engine, MetaData, insert
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func

from flask_jsontools import jsonapi, MethodView, methodview
from sqlalchemy.ext.serializer import loads, dumps


from sqlalchemy.ext.declarative import DeclarativeMeta
import models
from models import Base

DATABASE_URL = os.environ['DATABASE_URL']

#engine = create_engine("postgresql://postgres:1953@localhost:5432/chinook")

engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


Base.query = db_session.query_property()

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/longest_tracks')
def longest_tracks():
    tracks = db_session.query(models.Track).order_by(models.Track.milliseconds.desc()).limit(10)
    li = []
    di = {}
    if tracks is None:
        return "" , 404
    for elem in tracks:
        di["album_id"] = str(elem.album_id)
        di["bytes"] = str(elem.bytes)
        di["composer"] = str(elem.composer)
        di["genre_id"] = str(elem.genre_id)
        di["media_type_id"] = str(elem.media_type_id)
        di["milliseconds"] = str(elem.milliseconds)
        di["name"] = str(elem.name)
        di["track_id"] = str(elem.track_id)
        di["unit_price"] = str(elem.unit_price)
        li.append(dict(di))
    return jsonify(li)


@app.route('/longest_tracks_by_artist')
def longest_tracks_by_artist():
    artist = request.args.get('artist')
    tracks = db_session.query(models.Track).join(models.Album).join(models.Artist).filter(models.Artist.name == artist).order_by(models.Track.milliseconds.desc()).limit(10)
    li = []
    di = {}
    for elem in tracks:
        di["album_id"] = str(elem.album_id)
        di["bytes"] = str(elem.bytes)
        di["composer"] = str(elem.composer)
        di["genre_id"] = str(elem.genre_id)
        di["media_type_id"] = str(elem.media_type_id)
        di["milliseconds"] = str(elem.milliseconds)
        di["name"] = str(elem.name)
        di["track_id"] = str(elem.track_id)
        di["unit_price"] = str(elem.unit_price)
        li.append(dict(di))
    if not li:
        abort(404)
    return jsonify(li)


@app.route('/count_songs')
def count_songs():
    artists = request.args.get('artist')
    if artists is None:
        abort(404)
    artists = artists.split(',')
    li = []
    di = {}
    for artist in artists:
        count = db_session.query(func.count(models.Track.track_id)).join(models.Album).join(models.Artist).filter(models.Artist.name == artist)
        for elem in count:
            if elem[0] is 0:
                continue
            di[artist] = elem[0]
    if not di:
        abort(404)
    return jsonify(di)


@app.route('/artist', methods=['GET', 'POST'])
def artists():
    data = request.json
    if data is None or not 'name' in data or len(data['name']) == 0 or len(data.keys()) > 1:
        return "", 400

    artist_name = data.get("name")
    ins = insert(models.Artist)
    ins = ins.values(name=artist_name, artist_id=1500)
    db_session.execute(ins)
    di = dict()
    di["artist_id"] = '15000'
    di["name"] = artist_name

    return jsonify(di)


@app.route('/counter')
def counter():
    f = open('counter.txt', 'r')
    counter = int(f.read())
    f.close()
    f = open('counter.txt', 'w')
    counter += 1
    f.write(str(counter))
    f.close()
    return f"{counter}"


if __name__ == '__main__':
    app.run(debug=True)
