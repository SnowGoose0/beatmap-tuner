import os
import uuid
from beatmap import ModifierSettings
from beatmap import BeatmapBuilder
from osz import BeatmapOsz
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

session_cache = {}

def get_file_path(uuid, file_name):
    return os.path.join('.', 'tmp', str(uuid), file_name)

@app.route('/')
def index():
    return '<h1>To err is human</h1>'

@app.route('/osz-upload', methods=['POST'])
def osz_upload():
    file_uuid = str(uuid.uuid4())

    file = request.files['osz']

    if file:
        tmp_osz_dir = os.path.join('.', 'tmp', file_uuid)
        tmp_osz_path = get_file_path(file_uuid, file.filename)

        os.makedirs(tmp_osz_dir)
        file.save(tmp_osz_path)

    else:
        return jsonify({'status': 1})

    osz = BeatmapOsz(tmp_osz_path)
    session_cache[file_uuid] = {
        'fname': file.filename,
    }

    return jsonify({'fstatus': 0, 'fid': file_uuid, 'fdata': osz.difficulties})

@app.route('/difficulty-select', methods=['GET', 'POST'])
def difficulty_upload():
    data = request.json

    file_uuid = data['fid']
    file_name = session_cache[file_uuid]['fname']
    beatmap_difficulty = data['fdata']

    tmp_osz_path = get_file_path(file_uuid, file_name)
    bmap = BeatmapBuilder(tmp_osz_path, beatmap_difficulty)
    bmap.parse()
    bmap_settings = bmap.get_default_settings()

    session_cache[file_uuid]['fmap'] = bmap

    return jsonify({'fstatus': 0, 'fdata': bmap_settings})

@app.route('/difficulty-export', methods=['POST'])
def difficulty_export():
    data = request.json

    file_uuid = data['fid']
    user_settings = data['fdata']

    print(user_settings)

    bmap_settings = ModifierSettings(user_settings)
    bmap = session_cache[file_uuid]['fmap']
    bmap_difficulty_name = bmap.modify(bmap_settings)
    bmap_modified_buffer = bmap.serialize()

    bmap_export_path = os.path.join('.', 'tmp', str(file_uuid), bmap_difficulty_name)
    with open('.'.join([bmap_export_path, 'osu']), 'w') as f:
        f.write(bmap_modified_buffer)

    return jsonify({'fstatus': 0})

if __name__ == '__main__':
    app.run(debug=True)