import imagehash
from PIL import Image
from glob import glob
from flask import Flask, request, render_template

hashfunc = imagehash.whash

def compute_hashes(files):
    db = {}
    for i, fname in enumerate(files):
        img = Image.open(fname)
        hash = hashfunc(img)
        db[fname] = hash
    return db


def lookup(img, db):
    hash = hashfunc(img)
    results = [(fname, hash - h) for fname, h in db.items()]
    return min(results, key=lambda r: r[1])


if __name__ == '__main__':
    db = compute_hashes(glob('library/*.jpg'))
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            file = request.files['photo']
            img = Image.open(file.stream)
            result, dist = lookup(img, db)
        else:
            result, dist = None, None
        return render_template('index.html', result=result, distance=dist)

    app.run(host='0.0.0.0', port=5001, debug=True)
