from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

main = Flask(__name__)
# настроить базу данных SQLite относительно папки экземпляра приложения
main.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
# создаем расширение
db = SQLAlchemy()
# инициализировать приложение с расширением
db.init_app(main)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

#В методе ниже указано, что будет возвращаться значение из поля «title»
    def __repr__(self):
        return '<Article %r>' % self.id

with main.app_context():
    db.create_all()

@main.route('/') #Домашная страница
@main.route('/home')
def index_home():
    return render_template("index.html")

@main.route('/about') #Добавил страницу "О нас"
def about():
    return render_template("about.html")

@main.route('/user/<string:name>/<int:id>') #Старница пользователя
def user(name,id):
    return "Страница пользователя"+' ' + name +" " + str(id)

@main.route('/create-article', methods=['POST','GET']) #Добавляем список методов
def create_article():
    if request.method == 'POST': #Отправка на сервер поста
        title = request.form['title'] #Обращаемся к input формы title в base.html
        intro = request.form['intro']  # Обращаемся к input формы intro в base.html
        text = request.form['text']  # Обращаемся к input формы text в base.html

        article=Article(title=title, intro=intro, text=text) #Передаем данные в бд
        try:
            db.session.add(article) # Добавляем данные в бд
            db.session.commit()
            return redirect('/posts') #Возвращение на страницу с постами
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create-article.html')

@main.route('/posts/<int:id>/update', methods=['POST', 'GET'])  # Добавляем список методов, а так же указываем ссылку
def post_upgrade(id):
    article = Article.query.get(id)
    if request.method == 'POST':  # Отправка на сервер поста
        article.title = request.form['title']  # Обращаемся к input формы title в base.html
        article.intro = request.form['intro']  # Обращаемся к input формы intro в base.html
        article.text = request.form['text']  # Обращаемся к input формы text в base.html

        try:
            db.session.commit()
            return redirect('/posts')  # Возвращение на страницу с постами
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template('post_update.html', article=article)


@main.route('/posts') #Добавил страницу "Посты"
def posts():
    articles = Article.query.order_by(Article.date.desc()).all() #Вытащить данные из бд с сортировкой по дате
    return render_template("posts.html", articles=articles) #передаем список в шаблон

@main.route('/posts/<int:id>') #Создаем страницу с детальным описанием статьи
def post_detail(id):
    article = Article.query.get(id) #В качестве ссылки используем Id статьи
    return render_template("posts_detail.html", article=article) #передаем список в шаблон

@main.route('/posts/<int:id>/del') #Создаем страницу для удаления статей
def post_del(id):
    article = Article.query.get_or_404(id) #В качестве ссылки используем Id, если не найдено то 404

    try:
        db.session.delete(article) #Удаление статьи из бд
        db.session.commit()
        return redirect ('/posts')
    except:
        return "При удалении статьи произошла ошибка"


if __name__=="__main__":
    main.run(debug=True)