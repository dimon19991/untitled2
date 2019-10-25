from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# подключение
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01200120@localhost/Testing'
# связь
db = SQLAlchemy(app)


class ormUser(db.Model):
    __tablename__ = 'orm_user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_studybook = db.Column(db.String(6), nullable=False)
    user_email = db.Column(db.String(40))
    user_year = db.Column(db.Date, nullable=False)
    user_birthday = db.Column(db.Date, nullable=False)

    orm_skills = db.relationship('ormSkill', secondary='orm_user_skill')


class ormSkill(db.Model):
    __tablename__ = 'orm_skill'
    skill_name = db.Column(db.String(40), primary_key=True)

    orm_users = db.relationship('ormUser', secondary='orm_user_skill')


class ormUserSkill(db.Model):
    __tablename__ = 'orm_user_skill'

    user_id = db.Column(db.Integer, db.ForeignKey('orm_user.user_id'), primary_key=True)
    skill_name = db.Column(db.String(40), db.ForeignKey('orm_skill.skill_name'), primary_key=True)


# создание всех таблиц
db.create_all()

# очистрка всех таблиц
db.session.query(ormUserSkill).delete()
db.session.query(ormSkill).delete()
db.session.query(ormUser).delete()

# создане объектов
Bob = ormUser(user_name="Bob",
              user_birthday='10-10-2000',
              user_email='bob@gmail.com',
              user_studybook='KM1111',
              user_year='10-09-2010',
              )

Boba = ormUser(user_name="Boba",
               user_birthday='10-10-2001',
               user_email='boba@gmail.com',
               user_studybook='KM2222',
               user_year='10-10-2010',
               )

Boban = ormUser(user_name="Boban",
                user_birthday='10-10-2001',
                user_email='boba@gmail.com',
                user_studybook='KM2222',
                user_year='10-10-2010',
                )

Biba = ormUser(user_name="Biba",
               user_birthday='10-10-2011',
               user_email='biba@gmail.com',
               user_studybook='KM3333',
               user_year='10-10-2017',
               )

Java = ormSkill(skill_name='Java')
Oracle = ormSkill(skill_name='Oracle')
Python = ormSkill(skill_name='Python')

# create relations
Bob.orm_skills.append(Java)
Bob.orm_skills.append(Oracle)
Bob.orm_skills.append(Python)

Boba.orm_skills.append(Java)

Boban.orm_skills.append(Oracle)

# insert into database
db.session.add_all([Java, Oracle, Python, Boban, Boba, Bob, Biba])
# commit
db.session.commit()


@app.route('/')
def index():
    return "<h1 sttle='color: red'>hello flask</h1>"


if __name__ == "__main__":
    app.run()
