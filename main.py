from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms.person_form import PersonForm
from dao.orm.model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01200120@localhost/Testing'
db = SQLAlchemy(app)



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
        if form.validate() == False:
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

        if form.validate() == False:
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

if __name__ == "__main__":
    app.run()




