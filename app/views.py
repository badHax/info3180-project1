"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, SignupForm
from models import UserProfile
from flask import jsonify
import time


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup' ,methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # get data from form
            FirstName = form.FirstName.data
            LastName = form.LastName.data
            email = form.email.data
            password = form.password.data
            username = form.username.data
            image= "https://www.timeshighereducation.com/sites/default/files/byline_photos/default-avatar.png"
            age = 18
            bio = "Edit your bio"
            created_on = time.strftime("%c")

            # retrieve user from database
            user = UserProfile.query.filter_by(username=username, password=password).first()

            # if the user already exists then flash error message and redirect back to the registration page
            if user is not None:
                flash('An account with that email address already exists', 'danger')
                return redirect(url_for('signup', form=form))

            # create user object
            user = UserProfile(first_name=FirstName,
                               last_name=LastName,
                               password=password,
                               username=username,
                               created_on=created_on,
                               bio = bio,
                               age=age,
                               image=image)

            # insert user into UserProfile
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
            
    return render_template('signup.html', form = form, page_title = 'Signup to create a profile')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      user = UserProfile.query.filter_by(username=username, password=password).first()
      
      if user is not None:
          login_user(user)
          flash('Logged in successfully.', 'success')
          next = request.args.get('next')
          user = UserProfile.query.filter_by(username=username, password=password).first()
          userid = user.id
          return redirect(url_for('profile',userid=userid))
      else:
          flash('Username or Password is incorrect.', 'danger')
          flash(form)
    return render_template("login.html", form=form)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
    
def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@app.route('/profile/<userid>')
@login_required
def profile(userid):
    user = UserProfile.query.filter_by(id=userid).first()
    if user == None:
        flash('User ID %s not found.' % userid)
        return redirect(url_for('home'))
    
    if request_wants_json():
        return jsonify(items=[x.to_json() for x in user])
        
    return render_template('profile.html',
                           user=user)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    
###
#   Editing profile
###
@login_required
@app.route('/user_edit_first_name',methods=['GET', 'POST'])
def user_edit_first_name():
    id = request.form["pk"]
    user = UserProfile.query.get(id)
    user.first_name = request.form["value"]
    result = {}
    db.session.commit()
    return jsonify(result) #or, as it is an empty json, you can simply use return "{}"
    
@login_required
@app.route('/user_edit_last_name',methods=['GET', 'POST'])
def user_edit_last_name():
    id = request.form["pk"]
    user = UserProfile.query.get(id)
    user.last_name = request.form["value"]
    result = {}
    db.session.commit()
    return jsonify(result)

@login_required
@app.route('/user_edit_tagline',methods=['GET', 'POST'])
def user_edit_tagline(id):
    id = request.form["pk"]
    user = UserProfile.query.get(id)
    user.tagline = request.form["value"]
    result = {}
    db.session.commit()
    return jsonify(result)
    
@login_required    
@app.route('/user_edit_biography',methods=['GET', 'POST'])
def user_edit_biography():
    id = request.form["pk"]
    user = Users.query.get(id)
    user.bio = request.form["value"]
    result = {}
    db.session.commit()
    return jsonify(result)

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
