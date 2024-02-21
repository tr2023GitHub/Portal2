from flask import Flask, render_template, g
import sqlite3
import Base

# создаем приложение/Объекта Flask
app = Flask(__name__)
# настройки приложения
app.config['DATABASE'] = "static/bd/softOffers.db"
app.secret_key = "asdf1234"             # ключ для кеширования, для Flask он обязан быть

def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row         # выведит в виде словарика, а не картежей
    return con
   

# проверка уже есть подключение БД в этом приложение, g отвечает за взаимодействия контекста данного приложения;
# пользователи работают с контекстом(копия) прлиложения ; если нет подключения g=0
def get_connect():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

navMenu = [
    {"link": "/main_list", "name": "Программы"},
    {"link": "/projects", "name": "Проекты"},
    {"link": "/articles", "name": "Статьи"}
]

@app.route("/main_list")
@app.route("/")
def main_list(): 
    con = get_connect()
    base = Base.ProductDB(con)
    return render_template("main_list.html", menu=navMenu, cards = base.getAllProduct()) # от render_template получаем шаблон и выводим в браузере; передаем аргумент файл html и что надо в шаблон подставить

@app.route("/projects")
def schedule():
    con = get_connect()
    base = Base.ProductDB(con)
    return render_template("projects.html", menu=navMenu, cards = base.getAllProduct())

@app.route("/contacts")
def contacts():
    return render_template("articies.html", menu=navMenu)

@app.route("/card/<int:value>")
def prod(value):
    con = get_connect()
    base = Base.ProductDB(con)
    product = base.getProduct(value)
    
    #создать шаблон и вызвать его тут
    # return render_template("card.html", menu=navMenu, name = product["name"], des = product["description"], 
    #                        img=product["img"], price=product["price"], trip=product["trip"], img1=product["img1"], img2=product["img2"])
    return render_template("card.html", menu=navMenu, name_soft=product["name_soft"], class_soft=product["name_class"],ind_soft=product["name"],
                           min_dsc=product["min_description"],max_dsc=product["max_description"], logo_com=product["logo"], site_com=product["site"])
# разрыв подключения
@app.teardown_appcontext 
def close_connect(error):
    if hasattr(g, "link_db"):
        g.link_db.close()
    

if __name__ == "__main__":
    app.run()