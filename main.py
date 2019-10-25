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

i_1 = ormTestCase(testcase_id = 1)
i_2 = ormTestCase(testcase_id = 2)
i_3 = ormTestCase(testcase_id = 3)
i_4 = ormTestCase(testcase_id = 4)
i_5 = ormTestCase(testcase_id = 5)

add.Function_TescCase.append(i_1)
sub.Function_TescCase.append(i_2)
mult.Function_TescCase.append(i_3)
div.Function_TescCase.append(i_4)
abs.Function_TescCase.append(i_5)

p_0i_1_1 = ormParameters(parameters_index = 0,
    testcase_iteration = 1,
    parameters_value = 2)

p_1i_1_2 = ormParameters(parameters_index = 1,
    testcase_iteration = 1,
    parameters_value = 3)

p_0i_1_3 = ormParameters(parameters_index = 0,
    testcase_iteration = 1,
    parameters_value = 4)

p_1i_1_4 = ormParameters(parameters_index = 1,
    testcase_iteration = 1,
    parameters_value = 5)

p_0i_1_5 = ormParameters( parameters_index = 0,
    testcase_iteration = 1,
    parameters_value = -7)


i_1.TestCase_Parameters.append(p_0i_1_1)
i_1.TestCase_Parameters.append(p_1i_1_2)
i_2.TestCase_Parameters.append(p_0i_1_3)
i_2.TestCase_Parameters.append(p_1i_1_4)
i_5.TestCase_Parameters.append(p_0i_1_5)


iter_1 = ormResult(result_value = 5,
                    testcase_iteration = 1)

iter_2 = ormResult(result_value = -1,
                    testcase_iteration = 1)

iter_3 = ormResult(result_value = 4,
                    testcase_iteration = 1)

iter_4 = ormResult(result_value = 0.25,
                    testcase_iteration = 1)

iter_5 = ormResult(result_value = 7,
                    testcase_iteration = 1)

i_1.TestCase_Result.append(iter_1)
i_2.TestCase_Result.append(iter_2)
i_3.TestCase_Result.append(iter_3)
i_4.TestCase_Result.append(iter_4)
i_5.TestCase_Result.append(iter_5)


db.session.add_all([Dima, Vlad, Vadim, Yarik, Srhey, add, sub, mult, div, abs, i_1, i_2, i_3, i_4, i_5,
                    p_0i_1_1, p_1i_1_2, p_0i_1_3, p_1i_1_4, p_0i_1_5, iter_1, iter_2, iter_3, iter_4, iter_5])

db.session.commit()




@app.route('/')
def index():
    return "<h1 sttle='color: red'>hello flask</h1>"


if __name__ == "__main__":
    app.run()




