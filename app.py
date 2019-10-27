from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms.person_form import PersonForm
from forms.function_form import FunctionForm
from forms.tectcase_form import TestCaseForm
from sqlalchemy.sql import func
import plotly
import json
import plotly.graph_objs as go



app = Flask(__name__)
app.secret_key = 'key'




ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01200120@localhost/Testing'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://icpwmbrgnzgqfn:f405302b939ca13749bc99e77fe88195a491c4023ebb8090130157648216f732@ec2-107-21-126-201.compute-1.amazonaws.com:5432/df437o4oceoh5s'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


db.session.query(ormResult).delete()
db.session.query(ormParameters).delete()
db.session.query(ormTestCase).delete()
db.session.query(ormFunction).delete()
db.session.query(ormPersons).delete()

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/person', methods=['GET'])
def person():

    result = db.session.query(ormPersons).all()

    return render_template('person.html', persons = result)


@app.route('/new_person', methods=['GET','POST'])
def new_person():

    form = PersonForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('person_form.html', form=form, form_name="New person", action="new_person")
        else:
            new_person= ormPersons(
                                person_login=form.person_login.data,
                                person_password=form.person_password.data,
                                person_name=form.person_name.data,
                                person_surname=form.person_surname.data,
                                person_email=form.person_email.data,
                                person_birthday = form.person_birthday.data.strftime("%d-%b-%y")
                            )

            db.session.add(new_person)
            db.session.commit()


            return redirect(url_for('person'))

    return render_template('person_form.html', form=form, form_name="New person", action="new_person")



@app.route('/edit_person', methods=['GET','POST'])
def edit_person():

    form = PersonForm()


    if request.method == 'GET':

        person_login =request.args.get('person_login')
        person = db.session.query(ormPersons).filter(ormPersons.person_login == person_login).one()

        # fill form and send to user
        form.person_login.data = person.person_login
        form.person_password.data = person.person_password
        form.person_name.data = person.person_name
        form.person_surname.data = person.person_surname
        form.person_email.data = person.person_email
        form.person_birthday.data = person.person_birthday

        return render_template('person_form.html', form=form, form_name="Edit person", action="edit_person")


    else:

        if form.validate() != False:
            return render_template('person_form.html', form=form, form_name="Edit person", action="edit_person")
        else:
            # find user
            person = db.session.query(ormPersons).filter(ormPersons.person_login == form.person_login.data).one()

            # update fields from form data
            person.person_login = form.person_login.data
            person.person_password = form.person_password.data
            person.person_name = form.person_name.data
            person.person_surname = form.person_surname.data
            person.person_email = form.person_email.data
            person.person_birthday = form.person_birthday.data.strftime("%d-%b-%y")

            db.session.commit()

            return redirect(url_for('person'))





@app.route('/delete_person', methods=['POST'])
def delete_person():

    person_login = request.form['person_login']

    result = db.session.query(ormPersons).filter(ormPersons.person_login == person_login).one()

    db.session.delete(result)
    db.session.commit()


    return person_login


@app.route('/function', methods=['GET'])
def function():

    result = db.session.query(ormFunction).all()

    return render_template('function.html', functions = result)


@app.route('/new_function/<person_login>', methods=['GET','POST'])
def new_function(person_login):

    form = FunctionForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('function_form.html', form=form, form_name="New function", action="new_function")
        else:
            new_function= ormFunction(
                                function_name=form.function_name.data,
                                person_text=form.person_text.data,
                                counter_of_tests=form.counter_of_tests.data,
                                person_login_fk=person_login
                            )

            db.session.add(new_function)
            db.session.commit()


            return redirect(url_for('function'))

    return render_template('function_form.html', form=form, form_name="New function", action="new_function/"+person_login)



@app.route('/edit_function', methods=['GET','POST'])
def edit_function():

    form = FunctionForm()


    if request.method == 'GET':

        function_name = request.args.get('function_name')
        function = db.session.query(ormFunction).filter(ormFunction.function_name == function_name).one()

        # fill form and send to user
        form.function_name.data = function.function_name
        form.person_text.data = function.person_text
        form.counter_of_tests.data = function.counter_of_tests
        form.person_login_fk.data = function.person_login_fk

        return render_template('function_form.html', form=form, form_name="Edit function", action="edit_function")


    else:

        if form.validate() != False:
            return render_template('function_form.html', form=form, form_name="Edit function", action="edit_function")
        else:
            # find user
            function = db.session.query(ormFunction).filter(ormFunction.function_name == form.function_name.data).one()

            # update fields from form data
            function.function_name = form.function_name.data
            function.person_text = form.person_text.data
            function.counter_of_tests = form.counter_of_tests.data
            function.person_login_fk = form.person_login_fk.data

            db.session.commit()

            return redirect(url_for('function'))





@app.route('/delete_function', methods=['POST'])
def delete_function():

    function_name = request.form['function_name']

    result = db.session.query(ormFunction).filter(ormFunction.function_name == function_name).one()

    db.session.delete(result)
    db.session.commit()


    return function_name

@app.route('/testcase', methods=['GET'])
def testcase():

    result = db.session.query(ormTestCase).all()

    return render_template('testcase.html', testcases = result)


@app.route('/new_testcase/<function_name>', methods=['GET','POST'])
def new_testcase(function_name):

    form = TestCaseForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('testcase_form.html', form=form, form_name="New testcase", action="new_testcase")
        else:
            new_testcase= ormTestCase(
                                testcase_id=form.testcase_id.data,
                                function_name_fk=function_name,
                            )

            db.session.add(new_testcase)
            db.session.commit()


            return redirect(url_for('testcase'))

    return render_template('testcase_form.html', form=form, form_name="New testcase", action="new_testcase/"+function_name)



@app.route('/edit_testcase', methods=['GET','POST'])
def edit_testcase():

    form = TestCaseForm()


    if request.method == 'GET':

        testcase_id =request.args.get('testcase_id')
        testcase = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == testcase_id).one()

        # fill form and send to user
        form.testcase_id.data = testcase.testcase_id
        form.function_name_fk.data = testcase.function_name_fk

        return render_template('testcase_form.html', form=form, form_name="Edit testcase", action="edit_testcase")


    else:

        if form.validate() != False:
            return render_template('testcase_form.html', form=form, form_name="Edit testcase", action="edit_testcase")
        else:
            # find user
            testcase = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == form.testcase_id.data).one()

            # update fields from form data
            testcase.testcase_id = form.testcase_id.data
            testcase.function_name_fk = form.function_name_fk.data

            db.session.commit()

            return redirect(url_for('testcase'))





@app.route('/delete_testcase', methods=['POST'])
def delete_testcase():

    testcase_id = request.form['testcase_id']

    result = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == testcase_id).one()

    db.session.delete(result)
    db.session.commit()


    return result

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    query1 = (
        db.session.query(
            ormPersons.person_login,
            func.count(ormFunction.function_name).label('function_count')
        ).
            outerjoin(ormFunction).
            group_by(ormPersons.person_login)
    ).all()

    query2 = (
        db.session.query(
            ormFunction.function_name,
            func.count(ormTestCase.testcase_id).label('testcase_count')
        ).
            outerjoin(ormTestCase).
            group_by(ormFunction.function_name)
    ).all()

    login, function_count = zip(*query1)
    bar = go.Bar(
        x=login,
        y=function_count
    )

    name, testcase_count = zip(*query2)
    pie = go.Pie(
        labels=name,
        values=testcase_count
    )

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)
if __name__ == "__main__":
    app.debug = True
    app.run()




