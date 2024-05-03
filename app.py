from flask import Flask, render_template, request
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

conversation_history = []


def send_message_and_receive_response(role, query):
    conversation_history.append({"role": role, "content": query})

    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="gpt-4-turbo"
    )

    return chat_completion.choices[0].message.content


def flag_found(response, flag_format):
    conversation_history.append({"role": "system", "content": response})

    response = send_message_and_receive_response(
        'user', 'If you found the flag, display it in just one sentence so I can extract the data nicely. The flag format should only appear once. If the flag was not found, do not mention the flag format at all.')

    start_index = response.find(flag_format)
    if start_index == -1:
        return [False, "Flag not found. Please try again."]

    end_index = response.find("}", start_index + len(flag_format))
    if end_index == -1:
        return [False, "Flag not found. Please try again."]

    return [True, response[start_index:end_index + 1]]


def make_query(name, desc, category, flag_format, general_info, data_from_files):
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

    if data_from_files:
        query += data_from_files

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

    file_contents = []
    for file in files:
        if file and file.filename:
            content = file.stream.read().decode('utf-8')
            file_contents.append(content)

    data_from_files = ', '.join(file_contents)

    query = make_query(name, desc, category, flag_format,
                       general_info, data_from_files)

    for i in range(10):
        if i == 0:
            response = send_message_and_receive_response('user', query)
        else:
            response = send_message_and_receive_response(
                'user', 'Please try to find the flag again.')

        print(f'i: {i} and response {response}')

        flag_found_results = flag_found(response, flag_format)

        if flag_found_results[0]:
            return render_template('index.html', message=flag_found_results[1])

    return render_template('index.html', message=flag_found_results[1])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
