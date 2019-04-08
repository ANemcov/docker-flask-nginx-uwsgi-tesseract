from flask import Flask, jsonify, request, url_for
from flask import render_template, flash, redirect
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

app = Flask(__name__)
app.config.from_object('config')

from forms import LoginForm, UploadForm
from flask_uploads import UploadSet, IMAGES, configure_uploads

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

def recognize(source_image, lang):
    return pytesseract.image_to_string(source_image, lang=lang)

@app.route('/', methods=['GET', 'POST'])
def index():
    upload_form = UploadForm()
    
    if 'description' in request.values:
        upload_form.desc = request.values['description']
    else:
        upload_form.desc = ''
    
    if request.method == 'POST':
        if upload_form.validate_on_submit():
            f = upload_form.imagefile.data
            filename = secure_filename(f.filename)
            # f.save(os.path.join(
            #     app.instance_path, 'photos', filename
            # ))
            print('Filename: {}'.format(filename))
            res = recognize(Image.open(f), 'rus')
            return redirect(url_for('index', description=res))
        else:
            print("FORM ERROR")

    return render_template('upload.html', 
        title = 'Upload',
        form = upload_form)

@app.route('/health', methods=['GET'])
def health():
    return jsonify('Success')

@app.route('/recognize', methods=['POST'])
def parse():
    for f in request.files:
        img = Image.open(request.files[f])
        return jsonify({'success': recognize(img, 'rus')})
    return jsonify('')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
