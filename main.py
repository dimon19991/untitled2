from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01200120@localhost/Testing'

db = SQLAlchemy(app)


class ormPersons(db.Model):
    __tablename__ = 'orm_person'

    person_login = db.Column(db.String(50), primary_key=True)
    person_password = db.Column(db.String(32), nullable=False)
    person_name = db.Column(db.String(50), nullable=False)
    person_surname = db.Column(db.String(50), nullable=False)
    person_email = db.Column(db.String(50), nullable=True)
    person_birthday = db.Column(db.Date, nullable=False)

    Persons_Function = db.relationship("ormFunction")


class ormFunction(db.Model):
    __tablename__ = 'orm_function'

    function_name = db.Column(db.String(100), primary_key=True)
    person_text = db.Column(db.String(1000), nullable=False)
    counter_of_tests = db.Column(db.Integer, nullable=False)

    person_login_fk = db.Column(db.String(50), db.ForeignKey('orm_person.person_login'))

    Function_TescCase = db.relationship("ormTestCase")


class ormTestCase(db.Model):
    __tablename__ = 'orm_testcase'

    testcase_id = db.Column(db.Integer, primary_key=True)

    function_name_fk = db.Column(db.String(100), db.ForeignKey('orm_function.function_name'))

    TestCase_Parameters = db.relationship("ormParameters")
    TestCase_Result = db.relationship("ormResult")


class ormParameters(db.Model):
    __tablename__ = 'orm_parameters'

    parameters_index = db.Column(db.Integer, primary_key=True)
    testcase_iteration = db.Column(db.Integer, nullable=False)
    parameters_value = db.Column(db.String(100), nullable=False)

    testcase_id = db.Column(db.Integer, db.ForeignKey('orm_testcase.testcase_id'), primary_key=True)


class ormResult(db.Model):
    __tablename__ = 'orm_result'

    result_value = db.Column(db.Integer, nullable=False)
    testcase_iteration = db.Column(db.Integer, primary_key=True)

    testcase_id = db.Column(db.Integer, db.ForeignKey('orm_testcase.testcase_id'), primary_key=True)


db.create_all()


db.session.query(ormResult).delete()
db.session.query(ormParameters).delete()
db.session.query(ormTestCase).delete()
db.session.query(ormFunction).delete()
db.session.query(ormPersons).delete()




Dima = ormPersons(  person_login = "Dima",
                person_password = "0000",
                person_name = "Dima",
                person_surname = "Koltsov",
                person_email = "dik19994@gmail.com",
                person_birthday = "1999-01-01")

Vlad = ormPersons(  person_login = "Vlad",
                person_password = "0000",
                person_name = "Vlad",
                person_surname = "Kanevckyi",
                person_email = "vladkaneve@gmail.com",
                person_birthday = "1999-02-04")

Vadim = ormPersons(  person_login = "Vadim",
                person_password = "0000",
                person_name = "Vadim",
                person_surname = "Pits",
                person_email = None,
                person_birthday = "1998-10-29")

Yarik = ormPersons(  person_login = "Yarik",
                person_password = "0000",
                person_name = "Yarik",
                person_surname = "Artemenko",
                person_email = None,
                person_birthday = "1999-08-11")

Srhey = ormPersons(  person_login = "Srhey",
                person_password = "0000",
                person_name = "Srhey",
                person_surname = "Gorodnuk",
                person_email = None,
                person_birthday = "1999-10-02")

add = ormFunction( function_name = "add",
                person_text = "def add(a, b):\n\treturn a+b",
                counter_of_tests = 10)

sub = ormFunction( function_name = "sub",
                person_text = "def sub(a, b):\n\treturn a-b",
                counter_of_tests = 10)

mult = ormFunction( function_name = "mult",
                person_text = "def mult(a, b):\n\treturn a*b",
                counter_of_tests = 10)

div = ormFunction( function_name = "div",
                person_text = "def div(a, b):\n\treturn a/b",
                counter_of_tests = 10)

abs = ormFunction( function_name = "abs",
                person_text = "def abs(a):\n\treturn abs(a)",
                counter_of_tests = 10)


Dima.Persons_Function.append(add)
Vlad.Persons_Function.append(sub)
Vadim.Persons_Function.append(mult)
Yarik.Persons_Function.append(div)
Srhey.Persons_Function.append(abs)


# Boba = ormUser( user_name="Boba",
#                user_birthday='10-10-2001',
#                user_email='boba@gmail.com',
#                user_studybook='KM2222',
#                user_year='10-10-2010',
#                )
#
#
# Boban = ormUser( user_name="Boban",
#                user_birthday='10-10-2001',
#                user_email='boba@gmail.com',
#                user_studybook='KM2222',
#                user_year='10-10-2010',
#                )
#
#
# Biba = ormUser( user_name="Biba",
#                user_birthday='10-10-2011',
#                user_email='biba@gmail.com',
#                user_studybook='KM3333',
#                user_year='10-10-2017',
#                )
#
#
# Java = ormSkill(skill_name='Java')
# Oracle = ormSkill(skill_name='Oracle')
# Python = ormSkill(skill_name='Python')
#
# # create relations
# Bob.orm_skills.append(Java)
# Bob.orm_skills.append(Oracle)
# Bob.orm_skills.append(Python)
#
# Boba.orm_skills.append(Java)
#
# Boban.orm_skills.append(Oracle)
#
# # insert into database
db.session.add_all([Dima])
#
db.session.commit()
# # db.subquery("orm_function").delete()



@app.route('/')
def index():
    return "<h1 sttle='color: red'>hello flask</h1>"


if __name__ == "__main__":
    app.run()




