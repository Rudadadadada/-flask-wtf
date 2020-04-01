from flask import Flask, request, render_template
from professions import professions
from PIL import Image
from io import BytesIO
import json
import random


app = Flask(__name__)

count = 4
@app.route('/')
def route():
    return render_template('base.html')


@app.route('/training/<prof>')
def prof(prof):
    return render_template('training.html', title='Тренировка', prof=prof.lower())


@app.route('/list_prof/<list>')
def list_prof(list):
    return render_template('list_prof.html', title='Профессии', list_prof=professions, list_type=list)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    dictionary = dict()
    dictionary['title'] = 'Анкета'
    dictionary['surname'] = 'Watny'
    dictionary['name'] = 'Mark'
    dictionary['education'] = 'выше среднего'
    dictionary['profession'] = 'штурман марсохода'
    dictionary['sex'] = 'male'
    dictionary['motivation'] = 'Всегда мечтал застрять на Марсе!'
    dictionary['ready'] = 'True'
    return render_template('auto_answer.html', **dictionary)


@app.route('/login')
def login():
    return render_template('double_authentication.html', title='Аварийный доступ')


@app.route('/distribution')
def distribution():
    dictionary = dict()
    dictionary['title'] = 'Размещение по каютам'
    dictionary['list'] = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандерс', 'Шон Бин']
    return render_template('distribution.html', **dictionary)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    dictionary = dict()
    dictionary['title'] = 'Цвет каюты'
    dictionary['sex'] = sex
    dictionary['age'] = age
    return render_template('table.html', **dictionary)


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    global count
    dictionary = dict()
    dictionary['imgs'] = ['1.jpg', '2.jpg', '3.jpg']
    if request.method == 'GET':
        return render_template('galery.html', title='Красная планета')
    elif request.method == 'POST':
        photo = request.files['photo']
        im = Image.open(BytesIO(photo.read()))
        im.save(f'static/img/{count}.png')
        dictionary['imgs'].append(f'{count}.png')
        count += 1
        return render_template('galery.html', **dictionary)


@app.route('/member')
def member():
    with open('templates/astronauts.json', 'r', encoding='UTF-8-SIG') as file:
        astronauts = json.load(file)
    info = random.choice(astronauts['astronauts'])
    name = info['name']
    image = info['image']
    professions = ', '.join(info['professions'])
    return render_template('personal_card.html', title='Персональная карточка', name=name,
                           image=image, professions=professions)


if '__main__' == __name__:
    app.run(port=8080, host='127.0.0.1')