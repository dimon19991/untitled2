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


# db.session.query(ormUserSkill).delete()
# db.session.query(ormSkill).delete()
# db.session.query(ormUser).delete()


#
# Bob = ormUser( user_name="Bob",
#                user_birthday='10-10-2000',
#                user_email='bob@gmail.com',
#                user_studybook='KM1111',
#                user_year='10-09-2010',
#                )
#
#
#
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
# db.session.add_all([Java,Oracle,Python,Boban,Boba,Bob,Biba])
#
db.session.commit()
# # db.subquery("orm_function").delete()



@app.route('/')
def index():
    return "<h1 sttle='color: red'>hello flask</h1>"


if __name__ == "__main__":
    app.run()




