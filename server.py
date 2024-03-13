from flask import Flask, render_template, request, session, g 
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

@app.route("/main_list",methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def main_list(): 
    con = get_connect()
    # base = Base.ProductDB(con)
    cursor = con.cursor()

     # Получаем все уникальные значения name_class для фильтра
    cursor.execute('SELECT DISTINCT  name_class, id FROM class')
    classes = cursor.fetchall()

    # selected_classes = request.form.getlist('class_filter')
    # clear_filter = 'clear_filter' in request.form

    # Получаем все уникальные значения industry.name_ind для фильтра
    cursor.execute('SELECT DISTINCT  name_ind, id FROM industry')
    industries = cursor.fetchall()

    # selected_industries = request.form.getlist('ind_filter')
    # clear_filter = 'clear_filter' in request.form

    # Получаем сохраненные значения фильтров из сессии
    selected_classes = session.get('selected_classes', [])
    selected_industries = session.get('selected_industries', [])
    # clear_filter = 'clear_filter' in request.form

    # # Сбрасываем фильтры только при первом входе на страницу "/main_list"
    # if request.path == "/main_list" and not request.args:
    #     selected_classes = []
    #     selected_industries = []

     # Проверяем, был ли это первый запрос на страницу или переход между страницами
    if not request.referrer or request.referrer.endswith("/main_list"):
        # Сбрасываем фильтры только при первом входе на страницу "/main_list"
        selected_classes = []
        selected_industries = []


    # Обработка POST-запроса
    if request.method == 'POST':
    # Если выбран чекбокс "Clear All", сбрасываем все фильтры
        if 'clear_filter' in request.form:
            selected_classes = []
            selected_industries = []
        else:
            selected_classes = request.form.getlist('class_filter')
            selected_industries = request.form.getlist('ind_filter')
   
    # Если выбраны классы, фильтруем данные
    if selected_classes:
        placeholders = ', '.join(['?'] * len(selected_classes))
        query = f'SELECT * FROM class WHERE name_class IN ({placeholders})'
        cursor.execute(query, selected_classes)
        data = cursor.fetchall()
    else:
        # Если ничего не выбрано, отображаем все данные
        cursor.execute('SELECT * FROM class')
        data = cursor.fetchall()
    
    # Если выбраны отрасли, фильтруем данные
    if selected_industries:
        placeholders = ', '.join(['?'] * len(selected_industries))
        query = f'SELECT * FROM industry WHERE name_ind IN ({placeholders})'
        cursor.execute(query, selected_industries)
        data_ind = cursor.fetchall()
    else:
        # Если ничего не выбрано, отображаем все данные
        cursor.execute('SELECT * FROM industry')
        data_ind = cursor.fetchall()

    # Сохраняем выбранные значения фильтров в сессии
    session['selected_classes'] = selected_classes
    session['selected_industries'] = selected_industries

    # con.close()

    # return render_template('main_list.html', classes=classes, data=data, selected_classes=selected_classes)
    base = Base.ProductDB(con)
    return render_template("main_list.html", menu=navMenu, cards = base.getAllProduct(), classes=classes, data=data, selected_classes=selected_classes,
                           industries = industries, data_ind = data_ind, selected_industries = selected_industries)
 # от render_template получаем шаблон и выводим в браузере; передаем аргумент файл html и что надо в шаблон подставить
    
  
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
    max_dsc = "/static/files/test_dsc"+str(product["id"])+".html"

    # nav_value = request.args.get('nav_value', 'description')
    
    #создать шаблон и вызвать его тут
    # return render_template("card.html", menu=navMenu, name = product["name"], des = product["description"], 
    #                        img=product["img"], price=product["price"], trip=product["trip"], img1=product["img1"], img2=product["img2"])
    return render_template("card.html", menu=navMenu, name_soft=product["name_soft"], class_soft=product["name_class"],ind_soft=product["name_ind"],
                           min_dsc=product["min_description"],max_dsc=max_dsc, logo_com=product["logo"], site_com=product["site"],
                           offer_id = product["id"])

# разрыв подключения
@app.teardown_appcontext 
def close_connect(error):
    if hasattr(g, "link_db"):
        g.link_db.close()
    

if __name__ == "__main__":
    app.run()