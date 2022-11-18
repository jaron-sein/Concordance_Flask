from flask import Flask, request
from connect_db import cursor
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

phrase = 'a fat cat sat on a mat - it ate a fat rats'
regconfig = 'simple'

# Перечисление лексем и их позиций в документе
@app.route("/api/pos/", methods=['GET'])
def pos():
    print(phrase)
    query = f"select to_tsvector('{regconfig}', '{phrase}');"
    cursor.execute(query)
    return json.dumps(cursor.fetchall())

# Количество слов
@app.route("/api/stat/", methods=['GET'])
def stat():
    # query = "select ts_stat('select to_tsvector('%s')')"
    # cursor.execute(query, (phrase, ))
    # query = f"select ts_stat('select to_tsvector(''{regconfig}'', ''{phrase}'')')"
    query = f"select ts_stat('select to_tsvector(''{regconfig}'', ''{phrase}'')')"
    cursor.execute(query)
    return json.dumps(cursor.fetchall())

# Получение документа
@app.route("/api/post_file/", methods=['POST'])
def post_file():
    global phrase
    if request.method == 'POST':
        phrase = request.files['file'].read().decode('cp1251')
    return ''

# Получение измененного текста документа
@app.route("/api/post_edit_file/", methods=['POST'])
def post_edit_file():
    global phrase
    # print(dir(request))
    if request.method == 'POST':
        phrase = request.form['text']
    return ''

# Скачивание файла
@app.route("/api/test_download/", methods=['GET'])
def test_download():
    global phrase
    test_file = open('download_files/test.txt', 'rb')
    # return test_file.read()
    return phrase

# Получение N-грамм
@app.route("/api/ngramms/", methods=['GET'])
def ngramms():
    # json.dumps переводит результат запроса не так, как нужно, поэтому словарь создается вручную
    query = f"select to_tsvector('{regconfig}', '{phrase}');"
    cursor.execute(query)
    pos_json = {}
    for item in cursor.fetchall()[0][0].split(' '):
        item_parts = item.split(':')
        pos_json[item_parts[0].replace("'", "")] = [int(value) for value in item_parts[1].split(',')]
    text = phrase.split(' ')
    # Получение N-грамм
    
    ngramms = {}
    key_word = 'rats'
    n = 1
    positions = pos_json[key_word]
    for i in range(len(positions)):
        ngramms[i] = {}
        # n слов перед ключевым словом
        ngramms_before = []
        for j in range(n, 0, -1):
            idx = positions[i] - j - 1  # -1 с учетом того, что sql возвращает индексы с 1, а массив split с 0
            if idx > -1:
                ngramms_before.append(text[idx])
            print(f'!!! {j} {positions[i]} {text[idx]}')
        # n слов после ключевого слова
        ngramms_after = []
        for j in range(1, n + 1):
            idx = positions[i] + j - 1
            if idx < len(text):
                ngramms_after.append(text[idx])
            print(f'!!! {j} {positions[i]} {text[idx]}')
        ngramms[i]['before'] = ngramms_before
        ngramms[i]['key'] = key_word
        ngramms[i]['after'] = ngramms_after
    print(stat())
    return 'res_json'
