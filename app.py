from flask import Flask
from flask import request
from flask import jsonify
import requests
import datetime

from config import Config
from mongo import client


config = Config().file_db
db_obj = client(config['username'], config['password'], config['database'], host=config['host'])
file_db = db_obj[config['database']]
app = Flask(__name__)


def create_file_mapping(url, bucket_name):
    req = requests.get(url)
    content_type = req.headers['Content-Type']
    return  {
        'key': url.split('https://docs.turtlemint.com/')[1],
        'bucketName': bucket_name,
        'host': 'localhost',
        'mimeType': content_type,
        'createdAt': datetime.datetime.now(),
        'updatedAt': datetime.datetime.now()
    }

def save_file_mapping(url, bucket_name):
    file_mapping = create_file_mapping(url, bucket_name)
    db_file_result = file_db['fileMapping'].insert_one(file_mapping)
    file_mapping['id'] = str(db_file_result.inserted_id)
    print file_mapping.pop('_id')
    return file_mapping


@app.route("/file", methods=["POST"])
def file_mapping():
    form = request.form
    if not form.has_key('url'):
        return jsonify({'meta': {'msg': 'url is required key'}}), 400
    bucket_name = "docs.turtlemint.com" if not form.has_key('bucketName') else form.get('bucketName')
    return jsonify(save_file_mapping(form.get('url'), bucket_name))

if __name__ == "__main__":
    app.run()
