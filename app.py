from flask import Flask, render_template, request
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

conversation_history = []


def make_query(name, desc, category, flag_format, general_info, files):
    query = "Please find the flag given the following CTF problem and remember to display the flag. "

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

    conversation_history.append({"role": "user", "content": query})

    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="gpt-4"
    )

    response = chat_completion.choices[0].message.content

    print(response)

    conversation_history.append({"role": "system", "content": response})

    conversation_history.append(
        {"role": "user", "content": "If you found the flag, display it in just one sentence so I can extract the data nicely. The flag format should only appear once. If the flag was not found, do not mention the flag format at all."})

    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="gpt-4"
    )

    response = chat_completion.choices[0].message.content

    start_index = response.find(flag_format)
    if start_index == -1:
        message = "Flag not found. Please try again."
        return render_template('index.html', message=message)

    end_index = response.find("}", start_index + len(flag_format))
    if end_index == -1:
        print("Ending character not found after the flag format.")
        return

    message = "The flag is: " + response[start_index:end_index + 1]

    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

'''    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": ""
        }],
        model="gpt-4"
    )

    print(chat_completion.choices[0].message.content)'''
