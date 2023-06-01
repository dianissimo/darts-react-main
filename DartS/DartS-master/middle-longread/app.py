import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
# Для работы системы используется фреймворк Flask, на котором основана логика работы задней части приложения,
# библиотека requests используется для получения и отправки данных на приложение созданное другим членом группы,
# которое занимается управлением базой данных, а также реализует CRUD функции необходимые для функционирования
# приложения. Библиотека CORS необходима для получения разрешений на запросы с фронтальной части приложения.

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join('staticFiles', 'images')

app = Flask(__name__, static_folder='staticFiles')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, support_credentials=True)


# Функция для передачи на фронтальную часть приложения всех лонгридов находящихся в базе данных
@app.route('/api/explore/', methods=['GET'])
def api_longread_index():
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/longreads/all'
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url)
    # Полученный ответ в виде списка всех лонгридов перенаправляется на фронтальную часть приложения
    longreads_data = response.json()
    # На фронтальную часть приложения нужно отправлять ссылку на сервер + ссылку на изображение внутри сервера
    for longread in longreads_data:
        longread["img_link"] = 'http://127.0.0.1:4000' + longread["img_link"]
    # JSON-текст перенаправляется на фронтальную часть приложения
    return jsonify(longreads_data), 200


# Функция для передачи на фронтальную часть приложения информации о лонгриде по его индексу,
# а также информации о всех связанных с ним глав
@app.route('/api/longreads/<int:longread_id>', methods=['GET'])
def api_longread(longread_id):
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/longread'
    # JSON-текст в котором указан идентификатор лонгрида
    todo = {"longread_id": longread_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=todo)
    # Полученный ответ в виде данных о лонгриде
    longread = response.json()

    # Ссылка на функцию на сервисе по управлению БД, которая возвращает все главы привязанные к лонгриду по
    # его идентификатору
    api_url = 'http://127.0.0.1:4000/longread/chapter/all'
    # JSON-текст в котором указан идентификатор лонгрида
    todo = {"longread_id": longread_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=todo)
    # Полученный ответ в виде списка всех глав
    chapter_data = response.json()

    # JSON-текст в котором указаны данные лонгрида, а также связанные с ним главы
    longread_data = {
        'id': longread["id"],
        'name': longread["name"],
        'description': longread["description"],
        'img_link': 'http://127.0.0.1:4000' + longread["img_link"],
        'chapters': chapter_data
    }
    # JSON-текст перенаправляется на фронтальную часть приложения
    return jsonify(longread_data), 200


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для создания лонгрида и
# привязки его к миру, идентификатор которого был указан. При создании лонгрида ему будет присвоена
# стандартная фотография
@app.route('/api/worlds/<int:world_id>/create/', methods=('GET', 'OPTIONS', 'POST'))
def api_longread_create(world_id):
    # Фронтальная часть приложения перед отправлением запроса на создание элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/longread/create'
    # JSON-текст в котором указан идентификатор мира, название и описание необходимые для создания лонгрида
    longread = {
        'world_id': world_id,
        'name': json["name"],
        'description': json["description"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=longread)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для редактирования
# лонгрида, идентификатор которого был указан
@app.route('/api/longreads/<int:longread_id>/edit/', methods=['GET', 'POST', 'OPTIONS'])
def api_longread_edit(longread_id):
    # Фронтальная часть приложения перед отправлением запроса на редактирование элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/longread/edit'
    # JSON-текст в котором указан идентификатор лонгрида, название и описание необходимые для изменения лонгрида
    longread = {
        'longread_id': longread_id,
        'name': json["name"],
        'description': json["description"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=longread)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД изображения из формы, на которую будет изменена фотография лонгрида,
# идентификатор которого был указан. Предыдущее изображение лонгрида будет удалено, если оно не являлось стандартным
@app.route('/api/longreads/<int:longread_id>/update-image/', methods=['GET', 'OPTIONS', 'POST'])
def api_update_longread_image(longread_id):
    # Фронтальная часть приложения перед отправлением запроса на изменение изображения привязанного к элементу
    # отправляет OPTIONS запрос, на который необходимо ответить ответом с необходимыми заголовками, в котором
    # указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    # Из полученного ответа достается файл изображения
    new = request.files["image"]
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/longread/' + str(longread_id) + '/edit_image'
    # JSON-текст в котором указан идентификатор лонгрида необходимый для изменения изображения привязанного к лонгриду
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, files={'uploaded-file': new})
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()
    return jsonify(message)


# Функция для передачи на сервис по управлению БД запроса на удаление лонгрида, указанного по его идентификатору, а
# также всех глав, которые с ним связаны
@app.route('/api/longreads/<int:longread_id>/delete/', methods=('GET', 'OPTIONS', 'DELETE'))
def api_longread_delete(longread_id):
    # Фронтальная часть приложения перед отправлением запроса на удаление элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/longread/delete'
    # JSON-текст в котором указан идентификатор лонгрида необходимый для удаления лонгрида
    longread = {'longread_id': longread_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=longread)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message)


# Функция для передачи на фронтальную часть приложения информации о главе по ее индексу,
# а также информации о всех связанных с ним контентных блоков
@app.route('/api/chapter/<int:chapter_id>', methods=['GET'])
def api_chapter(chapter_id):
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/longread/chapter'
    # JSON-текст в котором указан идентификатор главы
    todo = {"chapter_id": chapter_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=todo)
    # Полученный ответ в виде данных о главе
    chapter = response.json()

    api_url = 'http://127.0.0.1:4000/longread/chapter/blockcontent/all'
    # JSON-текст в котором указан идентификатор главы
    todo = {"chapter_id": chapter_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=todo)
    # Полученный ответ в виде списка всех контент блоков
    blockcontents_data = response.json()
    # На фронтальную часть приложения нужно отправлять ссылку на сервер + ссылку на изображение внутри сервера
    for blockcontent in blockcontents_data:
        blockcontent["img_link"] = 'http://127.0.0.1:4000' + blockcontent["img_link"]

    # JSON-текст в котором указаны данные главы, а также связанные с ней контент блоки
    chapter_data = {
        'id': chapter["id"],
        'name': chapter["name"],
        'longread_id': chapter["longread_id"],
        'blockcontents': blockcontents_data
    }
    # JSON-текст перенаправляется на фронтальную часть приложения
    return jsonify(chapter_data), 200


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для создания главы и
# привязки ее к лонгриду, идентификатор которого был указан
@app.route('/api/longreads/<int:longread_id>/create/', methods=('GET', 'OPTIONS', 'POST'))
def api_chapter_create(longread_id):
    # Фронтальная часть приложения перед отправлением запроса на создание элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/longread/chapter/create'
    # JSON-текст в котором указан идентификатор лонгрида и название необходимые для создания главы
    chapter = {
        'longread_id': longread_id,
        'name': json["name"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=chapter)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для редактирования
# главы, идентификатор которой был указан
@app.route('/api/chapter/<int:chapter_id>/edit/', methods=['GET', 'POST', 'OPTIONS'])
def api_chapter_edit(chapter_id):
    # Фронтальная часть приложения перед отправлением запроса на редактирование элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/longread/chapter/edit'
    # JSON-текст в котором указан идентификатор главы и название необходимые для изменения главы
    chapter = {
        'chapter_id': chapter_id,
        'name': json["name"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=chapter)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД запроса на удаление главы, указанной по ее идентификатору, а
# также изображения и всех контентных блоков, которые с ней связаны
@app.route('/api/chapter/<int:chapter_id>/delete/', methods=('GET', 'OPTIONS', 'DELETE'))
def api_chapter_delete(chapter_id):
    # Фронтальная часть приложения перед отправлением запроса на удаление элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/longread/chapter/delete'
    # JSON-текст в котором указан идентификатор главы необходимый для удаления главы
    chapter = {'chapter_id': chapter_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=chapter)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message)


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для создания контентного
# блока и привязки его к главе, идентификатор которой был указан
@app.route('/api/blockcontent/<int:longread_id>/<int:chapter_id>/create/', methods=('GET', 'OPTIONS', 'POST'))
def api_blockcontent_create(longread_id, chapter_id):
    # Фронтальная часть приложения перед отправлением запроса на создание элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/longread/chapter/blockcontent/create'
    # JSON-текст в котором указан идентификатор лонгрида, идентификатор главы и текст необходимые для
    # создания контент блока
    blockcontent = {
        'longread_id': longread_id,
        'chapter_id': chapter_id,
        'text': json["text"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=blockcontent)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для редактирования
# контентного блока, идентификатор которого был указан
@app.route('/api/blockcontent/<int:blockcontent_id>/edit/', methods=['GET', 'POST', 'OPTIONS'])
def api_blockcontent_edit(blockcontent_id):
    # Фронтальная часть приложения перед отправлением запроса на редактирование элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/longread/chapter/blockcontent/edit'
    # JSON-текст в котором указан идентификатор контент блока и текст необходимые для изменения контент блока
    blockcontent = {
        'blockcontent_id': blockcontent_id,
        'text': json["text"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=blockcontent)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД изображения из формы, на которую будет изменена фотография
# контентного блока, идентификатор которого был указан. Предыдущее изображение контентного блока будет удалено,
# если оно не являлось стандартным
@app.route('/api/blockcontent/<int:blockcontent_id>/update-image/', methods=['GET', 'OPTIONS', 'POST'])
def api_update_blockcontent_image(blockcontent_id):
    # Фронтальная часть приложения перед отправлением запроса на изменение изображения привязанного к элементу
    # отправляет OPTIONS запрос, на который необходимо ответить ответом с необходимыми заголовками, в котором
    # указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    # Из полученного ответа достается файл изображения
    new = request.files["image"]
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/longread/chapter/blockcontent/' + str(blockcontent_id) + '/edit_image'
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, files={'uploaded-file': new})
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()
    return jsonify(message)


# Функция для передачи на сервис по управлению БД запроса на удаление контентного блока, указанной по ее
# идентификатору, а изображения, которое с ним связано
@app.route('/api/blockcontent/<int:blockcontent_id>/delete/', methods=('GET', 'OPTIONS', 'DELETE'))
def api_blockcontent_delete(blockcontent_id):
    # Фронтальная часть приложения перед отправлением запроса на удаление элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/longread/chapter/blockcontent/delete'
    # JSON-текст в котором указан идентификатор контент блока
    blockcontent = {'blockcontent_id': blockcontent_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=blockcontent)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message)


# Функция для передачи на фронтальную часть приложения информации о всех мирах находящихся в базе данных, функция
# дублирует ответ, который отправляется функцией api_world_index однако может быть переопределена по запросу коллег из
# фронтальной части приложения, для отображения других данных на индексной странице приложения
@app.route('/api/', methods=['GET'])
def api_index():
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/worlds/all'
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url)
    # Полученный ответ в виде списка всех миров перенаправляется на фронтальную часть приложения
    worlds_data = response.json()
    # На фронтальную часть приложения нужно отправлять ссылку на сервер + ссылку на изображение внутри сервера
    for world in worlds_data:
        world["img_link"] = 'http://127.0.0.1:4000' + world["img_link"]
    # JSON-текст перенаправляется на фронтальную часть приложения
    return worlds_data, 200


# Функция для передачи на фронтальную часть приложения информации о всех мирах находящихся в базе данных
@app.route('/api/worlds/', methods=['GET'])
def api_world_index():
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/worlds/all'
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url)
    # Полученный ответ в виде списка всех миров перенаправляется на фронтальную часть приложения
    worlds_data = response.json()
    # На фронтальную часть приложения нужно отправлять ссылку на сервер + ссылку на изображение внутри сервера
    for world in worlds_data:
        world["img_link"] = 'http://127.0.0.1:4000' + world["img_link"]
    # JSON-текст перенаправляется на фронтальную часть приложения
    return worlds_data, 200


# Функция для передачи на фронтальную часть приложения информации о мире по его индексу,
# а также информации о всех связанных с ним лонгридов и объектов мира
@app.route('/api/worlds/<int:world_id>', methods=['GET'])
def api_world(world_id):
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world'
    # JSON-текст в котором указан идентификатор мира
    todo = {"world_id": world_id}
    # Запрос отсылается на сервис по управлению БД`
    response = requests.post(api_url, json=todo)
    # Полученный ответ в виде данных о мире
    world = response.json()

    # Ссылка на функцию на сервисе по управлению БД, которая возвращает все лонгриды привязанные к миру по
    # его идентификатору
    api_url = 'http://127.0.0.1:4000/world/longread/all'
    # JSON-текст в котором указан идентификатор мира
    todo = {"world_id": world_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=todo)
    # Полученный ответ в виде списка всех лонгридов
    longreads_data = response.json()
    # На фронтальную часть приложения нужно отправлять ссылку на сервер + ссылку на изображение внутри сервера
    for longread in longreads_data:
        longread["img_link"] = 'http://127.0.0.1:4000' + longread["img_link"]

    # Ссылка на функцию на сервисе по управлению БД, которая возвращает все объекты мира привязанные к миру по
    # его идентификатору
    api_url = 'http://127.0.0.1:4000/world/worldobj/all'
    # JSON-текст в котором указан идентификатор мира
    todo = {"world_id": world_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=todo)
    # Полученный ответ в виде списка всех объектов мира
    worldobjs_data = response.json()
    # На фронтальную часть приложения нужно отправлять ссылку на сервер + ссылку на изображение внутри сервера
    for worldobj in worldobjs_data:
        worldobj["img_link"] = 'http://127.0.0.1:4000' + worldobj["img_link"]

    # JSON-текст в котором указаны данные мира, а также связанные с ним лонгриды и объекты мира
    world_data = {
        'id': world["id"],
        'name': world["name"],
        'description': world["description"],
        'img_link': 'http://127.0.0.1:4000' + world["img_link"],
        'longreads': longreads_data,
        'worldobjs': worldobjs_data
    }
    # JSON-текст перенаправляется на фронтальную часть приложения
    return jsonify(world_data), 200


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для создания мира.
# При создании мира ему будет присвоена стандартная фотография
@app.route('/api/worlds/create/', methods=('GET', 'OPTIONS', 'POST'))
def api_world_create():
    # Фронтальная часть приложения перед отправлением запроса на создание элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/create'
    # JSON-текст в котором указано название и описание необходимые для создания мира
    world = {
        'name': json["name"],
        'description': json["description"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=world)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для редактирования
# мира, идентификатор которого был указан
@app.route('/api/worlds/<int:world_id>/edit/', methods=['GET', 'POST', 'OPTIONS'])
def api_world_edit(world_id):
    # Фронтальная часть приложения перед отправлением запроса на редактирование элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/edit'
    # JSON-текст в котором указано название, описание и идентификатор, необходимые для изменения мира
    world = {
        'world_id': world_id,
        'name': json["name"],
        'description': json["description"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=world)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД изображения из формы, на которую будет изменена фотография мира,
# идентификатор которого был указан. Предыдущее изображение мира будет удалено, если оно не являлось стандартным
@app.route('/api/worlds/<int:world_id>/update-image/', methods=['GET', 'OPTIONS', 'POST'])
def api_update_world_image(world_id):
    # Фронтальная часть приложения перед отправлением запроса на изменение изображения привязанного к элементу
    # отправляет OPTIONS запрос, на который необходимо ответить ответом с необходимыми заголовками, в котором
    # указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    # Из полученного ответа достается файл изображения
    new = request.files["image"]
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/' + str(world_id) + '/edit_image'
    # JSON-текст в котором указан идентификатор мира необходимый для изменения изображения привязанного к миру
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, files={'uploaded-file': new})
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()
    return jsonify(message)


# Функция для передачи на сервис по управлению БД запроса на удаление мира, указанного по ее идентификатору, а
# также изображения, всех лонгридов и объектов мира, которые с ним связаны
@app.route('/api/worlds/<int:world_id>/delete/', methods=('GET', 'OPTIONS', 'DELETE'))
def api_world_delete(world_id):
    # Фронтальная часть приложения перед отправлением запроса на удаление элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/delete'
    # JSON-текст в котором указан идентификатор мира
    world = {'world_id': world_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=world)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message)


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для создания объекта мира.
# При создании объекта мира ему будет присвоена стандартная фотография
@app.route('/api/worlds/<int:world_id>/create_worldobj/', methods=('GET', 'OPTIONS', 'POST'))
def api_worldobj_create(world_id):
    # Фронтальная часть приложения перед отправлением запроса на создание элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/worldobj/create'
    # JSON-текст в котором указан идентификатор мира, название и описание необходимое для создания объекта
    worldobj = {
        'world_id': world_id,
        'name': json["name"],
        'description': json["description"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=worldobj)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД данных из форм, которые будут использованы для редактирования
# объекта мира, идентификатор которого был указан
@app.route('/api/worldobj/<int:worldobj_id>/edit/', methods=['GET', 'POST', 'OPTIONS'])
def api_worldobj_edit(worldobj_id):
    # Фронтальная часть приложения перед отправлением запроса на редактирование элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    #Полученный JSON-текст парсится для извлечения из него данных
    json = request.json
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/worldobj/edit'
    # JSON-текст в котором указан идентификатор объекта мира, название и описание необходимые для изменения
    # объекта мира
    worldobj = {
        'worldobj_id': worldobj_id,
        'name': json["name"],
        'description': json["description"]
    }
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=worldobj)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message), 201


# Функция для передачи на сервис по управлению БД изображения из формы, на которую будет изменена фотография
# объекта мира, идентификатор которого был указан. Предыдущее изображение объекта мира будет удалено,
# если оно не являлось стандартным
@app.route('/api/worldobj/<int:worldobj_id>/update-image/', methods=['GET', 'OPTIONS', 'POST'])
def api_update_worldobj_image(worldobj_id):
    # Фронтальная часть приложения перед отправлением запроса на изменение изображения привязанного к элементу
    # отправляет OPTIONS запрос, на который необходимо ответить ответом с необходимыми заголовками, в котором
    # указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    # Из полученного ответа достается файл изображения
    new = request.files["image"]
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/worldobj/' + str(worldobj_id) + '/edit_image'
    # JSON-текст в котором указан идентификатор объекта мира необходимый для изменения изображения привязанного к
    # объекту мира
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, files={'uploaded-file': new})
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()
    return jsonify(message)


# Функция для передачи на сервис по управлению БД запроса на удаление объекта мира, указанного по ее идентификатору, а
# также изображения, которое с ним связано
@app.route('/api/worldobj/<int:worldobj_id>/delete/', methods=('GET', 'OPTIONS', 'DELETE'))
def api_worldobj_delete(worldobj_id):
    # Фронтальная часть приложения перед отправлением запроса на удаление элемента отправляет OPTIONS запрос,
    # на который необходимо ответить ответом с необходимыми заголовками, в котором указаны разрешенные методы
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return jsonify({'message': 'Approved'}), 201
    # Ссылка на соответствующую функцию на сервисе по управлению БД
    api_url = 'http://127.0.0.1:4000/world/worldobj/delete'
    # JSON-текст в котором указан идентификатор объекта мира
    world = {'worldobj_id': worldobj_id}
    # Запрос отсылается на сервис по управлению БД
    response = requests.post(api_url, json=world)
    # Полученный ответ перенаправляется на фронтальную часть приложения
    message = response.json()

    return jsonify(message)
