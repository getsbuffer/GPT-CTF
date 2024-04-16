from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

    name = request.form.get('name')
    desc = request.form.get('desc')
    category = request.form.get('category')
    general_info = request.form.get('general-info')
    files = request.files.getlist('files')

    saved_files = []
    for file in files:
        if file and file.filename:
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            saved_files.append(file.filename)

    return render_template('index.html', name=name, desc=desc, category=category, general_info=general_info, saved_files=saved_files)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
