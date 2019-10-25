from datetime import datetime as dt

from flask import Flask, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy
#from forms import UserForm, FileForm, DocumentationForm, LanguageForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01200120@localhost/Testing'
db = SQLAlchemy(app)

class Goods_Have_Characteristic(db.Model):
    __tablename__ = 'goods_Have_Characteristic'
    g_left_name = db.Column(db.Integer, db.ForeignKey('goods.good_id'), primary_key=True)
    g_right_name = db.Column(db.Integer, db.ForeignKey('charakteristic.charac_id'), primary_key=True)


class Store_Have_Goods(db.Model):
    __tablename__  = 'store_Have_Goods'
    s_left_name = db.Column(db.Integer, db.ForeignKey('goods.good_id'), primary_key=True)
    s_right_name = db.Column(db.Integer, db.ForeignKey('store.store_id'), primary_key=True)


class Charakteristic(db.Model):

    __tablename__ = 'charakteristic'
    charac_id = db.Column(db.Integer, primary_key=True)
    charac_description= db.Column(db.String(100), unique=True, nullable=False)
    good_id_charac_fk = db.relationship("Goods", secondary="goods_Have_Characteristic")


class Goods(db.Model):

    __tablename__ = 'goods'
    good_id = db.Column(db.Integer, primary_key=True)
    good_name = db.Column(db.String(45))
    good_model = db.Column(db.String(100))
    charac_id_fk = db.relationship("Charakteristic", secondary="goods_Have_Characteristic")
    store_id_fk = db.relationship("Store", secondary="store_Have_Goods")
    results = db.relationship("Result")


class Store(db.Model):

    __tablename__ = 'store'
    store_id = db.Column(db.Integer, primary_key=True)
    store_name= db.Column(db.String(20), unique=True, nullable=False)
    store_link = db.Column(db.String(40), unique=True)
    good_id_store_fk = db.relationship("Goods", secondary="store_Have_Goods")



class Result(db.Model):

    __tablename__ = 'result'

    result_id=db.Column(db.Integer, primary_key=True)
    good_id_fk = db.Column(db.Integer, db.ForeignKey('goods.good_id'))
    result_availability = db.Column(db.String(20), nullable=False)

db.create_all()

'''
db.session.query(Charakteristic).delete()
session.query(Goods).delete()
db.session.query(Goods_Have_Characteristic).delete()
db.session.query(Store).delete()
db.session.query(Result).delete()
db.session.query(Store_Have_Goods).delete()

class Language(db.Model):
    tablename = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    version = db.Column(db.String(20))
    documentation_id = db.Column(db.Integer, db.ForeignKey('documentations.id'))

    def repr(self):
        return '<Language %r>' % self.name

class Documentation(db.Model):
    tablename = 'documentations'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(100))
    actor = db.Column(db.String(45))

    def repr(self):
        return '<Documentation %r>' % self.link

@app.route('/', methods=['GET'])
def home():
    return render_template('main.html')

@app.route('/user', methods=['GET'])
def users():
    result = []
    users = User.query.all()
    for user in users:
        result.append([user.id, user.name, user.email])
    return render_template('users.html', rows=result)

@app.route('/file', methods=['GET'])
def files():
    result = []
    files = File.query.all()
    for file in files:
        result.append([file.id, file.name, file.link])
    return render_template('files.html', rows=result)

@app.route('/document', methods=['GET'])
def doc():
    rows = [
        [1, "https://example.com", "Serhii", "Python"],
        [2, "https://example2.com", "Olha", "C"]
    ]
    return render_template('doc.html', rows=rows)

@app.route('/language', methods=['GET'])
def language():
    rows = [
        [1, "Python", "3.7"],
        [2, "C", "-"]
    ]
    return render_template('doc.html', rows=rows)

'''

Result1 = Result(
    result_id =4,
    good_id = 0,
    result_availability = "yes"
)

Result2 = Result(
    result_id =0,
    good_id = 1,
    result_availability = "no",
               )

Result3 = Result(
    result_id =3,
    good_id = 2,
    result_availability = "yes",
)

Result4 = Result(
    result_id =2,
    good_id = 4,
    result_availability = "no",
               )
Result5 = Result(
    result_id =1,
    good_id = 2,
    result_availability = "no",
)

Good1 = Goods(
    good_id=0,
    good_name ="Samsung",
    good_model ="S10",
               )
Good2 = Goods(
    good_id=4,
    good_name="OnePlus",
    good_model="7 PRO",
)
Good3 = Goods(
    good_id=1,
    good_name="IPhone",
    good_model="11",
)
Good4 = Goods(
    good_id=2,
    good_name="Huawei",
    good_model="P30 PRO",
)
Good5 = Goods(
    good_id=3,
    good_name="Xiaomi",
    good_model="Mi9",
)


Charc1 = Charakteristic(
    charac_id=3,
    charac_description="RAM",
        )

Charc2 = Charakteristic(
    charac_id=2,
    charac_description="Color",
        )

Charc3 = Charakteristic(
    charac_id=4,
    charac_description="Capacity",
        )

Charc4 = Charakteristic(
    charac_id=1,
    charac_description="Display",
        )

Charc5 = Charakteristic(
    charac_id=0,
    charac_description="Front Camera",
        )


Store1 = Store(
    store_id = 2,
    store_name="Rozetka",
    store_link="https://rozetka.com.ua"
               )
Store2 = Store(
    store_id = 1,
    store_name="Comfy",
    store_link="https://comfy.com.ua"
               )
Store3 = Store(
    store_id = 4,
    store_name="Citrus",
    store_link="https://citrus.com.ua"
               )
Store4 = Store(
    store_id = 3,
    store_name="Hotline",
    store_link="https://hotline.com.ua"
               )
Store5 = Store(
    store_id = 0,
    store_name="Allo",
    store_link="https://allo.com.ua"
               )
'''
GHC1 = Goods_Have_Characteristic(
    charac_id=3,
    good_id=0,
)

GHC2 = Goods_Have_Characteristic(
    charac_id=2,
    good_id=4,
)

GHC3 = Goods_Have_Characteristic(
    charac_id=4,
    good_id=1,
)

GHC4 = Goods_Have_Characteristic(
    charac_id=1,
    good_id=2,
)

GHC5 = Goods_Have_Characteristic(
    charac_id=0,
    good_id=3,
)



SHG1 = Goods_Have_Characteristic(
    id_store=2,
    good_id=0,
)
SHG2 = Goods_Have_Characteristic(
    id_store=1,
    good_id=4,
)
SHG3 = Goods_Have_Characteristic(
    id_store=4,
    good_id=1,
)
SHG4 = Goods_Have_Characteristic(
    id_store=3,
    good_id=2,
)
SHG5 = Goods_Have_Characteristic(
    id_store=0,
    good_id=3,
)
'''
# create relations
Good1.results.append(Result1)
Good2.results.append(Result2)
Good3.results.append(Result3)
Good4.results.append(Result4)
Good5.results.append(Result5)

Good1.store_id_fk.append(Store1)
Good2.store_id_fk.append(Store2)
Good3.store_id_fk.append(Store3)
Good4.store_id_fk.append(Store4)
Good5.store_id_fk.append(Store5)

Good1.charac_id_fk.append(Charc1)
Good2.charac_id_fk.append(Charc2)
Good3.charac_id_fk.append(Charc3)
Good4.charac_id_fk.append(Charc4)
Good5.charac_id_fk.append(Charc5)


# insert into database
db.session.add_all([Result1,Result2,Result3,Result4,Result5])
db.session.add_all([Charc1,Charc2,Charc3,Charc4,Charc5])
db.session.add_all([Good1,Good2,Good3,Good4,Good5])
db.session.add_all([Store1,Store2,Store3,Store4,Store5])






if __name__ == "__main__":
    app.run()