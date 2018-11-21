# -*- coding: utf-8 -*-
import argparse
import argparse
import os.path
# if os.path.basename(os.getcwd()) != 'web_VideoCaptioning':
#     os.chdir('../web_VideoCaptioning')
import utils
import os
from flask import Flask, render_template, request, url_for, send_from_directory


#Parse argument
parser = argparse.ArgumentParser()
parser.add_argument("-p", dest="video_path",
                    help="input video path", default='/     Users/banzhiyong/final_project/data/MSVD/YouTubeClips')
parser.add_argument("-n", dest="video_file_name", nargs='+',
                    help="input video file name", default='_O9kWD8nuRU_50_56.avi')
parser.add_argument("-fp", dest="video_full_path",
                    help="input video full path")
args = parser.parse_args()

ALLOWED_EXTENSIONS = set(['avi', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        if file and allowed_file(file.filename):
            filename = file.filename
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if args.video_full_path == None:
                video_full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            else:
                video_full_path = args.video_full_path

            # extract features and generate sentence
            video_feat = utils.extract_video_features(video_full_path)
            generated_sentence = utils.get_caption(video_feat)

            # file_url = url_for('uploaded_file', filename=filename)
            file_url = url_for('static', filename='uploads/' + filename)

            # print('123')
            # print(generated_sentence)
            entries = dict(sentence=generated_sentence, url=file_url)
            return render_template('message.html', entries=entries)     # + '<br><img src=' + file_url + '>'

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)