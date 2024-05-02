from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def make_query(name, desc, category, flag_format, general_info, files):
    query = "I am trying to solve a CTF problem in "

    if category:
        query = query + "the " + category
    else:
        query = query + " an unknown category"

    if name:
        query = query + " called " + name 
    else:
        query = query + " with an unknown name"

    if desc:
        query = query + " with a description  " + desc + "." 
    else:
        query = query + " with no description provided."

    if flag_format:
        query = query + " The flag format is " + flag_format + "."
    else:
        query = query + " The flag format was not provided."

    if general_info:
        query = query + " Some general info/hints that were provided are " + general_info + "."
    else:
        query = query + " No other general information or hints were provided."

    query = query + " With the given information, try to find the flag. Keep reprompting yourself until the flag is found."
    return query

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

    name = request.form.get('name')
    desc = request.form.get('desc')
    category = request.form.get('category')
    flag_format = request.form.get('flag_format')
    general_info = request.form.get('general-info')
    files = request.files.getlist('files')

    saved_files = []
    for file in files:
        if file and file.filename:
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            saved_files.append(file.filename)

    query = make_query(name, desc, category, flag_format, general_info, files)
    print(query)
    return render_template('index.html', name=name, desc=desc, flag_format=flag_format, category=category, general_info=general_info, saved_files=saved_files)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
