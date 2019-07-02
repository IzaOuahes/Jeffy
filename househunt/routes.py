import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from househunt import app, db, bcrypt
from househunt.forms import RegistrationForm, LoginForm, HouseHunt
from househunt.models import User
from BigQueryQueryfier import BigQueryQueryfier
import json
from househunt.config import Auth, Config, DevConfig, ProdConfig, GoogleUser
from flask_security import login_required



@app.route("/")



@app.route("/about")
@login_required
def about():
    return render_template('about.html', title='About')

@app.route("/home", methods=['GET', 'POST'])
def home():
    """Collect form inputs and redirect to display results."""
    search = HouseHunt(request.form)
    print(search)
    if request.method == 'POST':
        return display_results(search)
    return render_template('home.html', title='Jeffy', form=search)
# @app.route('/Google_login')
# def google_login():
#     if current_user.is_authenticated():
#         return redirect(url_for('about'))
#     google = get_google_auth()
#     auth_url, state = google.authorization_url( Auth.AUTH_URI, access_type='offline')
#     session['oauth_state'] = state
#     return render_template('login.html', auth_url=auth_url)

# @app.route('/gCallback')
# def callback():
#     # Redirect googleUser to home page if already logged in.
#     if current_user is not None and current_user.is_authenticated():
#         return redirect(url_for('index'))
#     if 'error' in request.args:
#         if request.args.get('error') == 'access_denied':
#             return 'You denied access.'
#         return 'Error encountered.'
#     if 'code' not in request.args and 'state' not in request.args:
#         return redirect(url_for('Google_login'))
#     else:
#         # Execution reaches here when user has successfully authenticated our app.
#         google = get_google_auth(state=session['oauth_state'])
#         try:
#             token = google.fetch_token( Auth.TOKEN_URI, client_secret=Auth.CLIENT_SECRET, authorization_response=request.url)
#         except HTTPError:
#             return 'HTTPError occurred.'
#         google = get_google_auth(token=token)
#         resp = google.get(Auth.USER_INFO)
#         if resp.status_code == 200:
#             user_data = resp.json()
#             email = user_data['email']
#             google_user = GoogleUser.query.filter_by(email=email).first()
#             if user is None:
#                 googleUser = GoogleUser()
#                 googleUser.email = email
#             googleUser.name = user_data['name']
#             googleUser.tokens = json.dumps(token)
#             googleUser.avatar = user_data['picture']
#             db.session.add(googleUser)
#             db.session.commit()
#             login_user(googleUser)
#             return redirect(url_for('index'))
#         return ('Could not fetch your information.')






@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@jeffy.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/results', methods=['GET'])
def display_results(s):
    """Render data from dateset with place name and description."""
    search_place=str(s.data['search_place'])
    search_description=str(s.data['search_description'])  
    print(search_description)  
    SQL = """ SELECT id, created_on, property_type, place_name, country_name, state_name, geonames_id, lat_lon, price, surface_total_in_m2, floor, rooms, expenses, properati_url, description, title, image_thumbnail 
    FROM `properati-data-public.properties_mx.properties_rent_201802` 
        WHERE place_name LIKE '%{search_place}%'
              AND description  LIKE '%{search_description}%'
       limit 15 """.format(search_place=search_place, search_description=search_description)

    bqq = BigQueryQueryfier(project_id='zinc-bucksaw-245306',
                            credentials_filename='zinc-bucksaw-245306-4b1c1d26fd11.json')
    
    df = bqq.query_to_df(sql_query=SQL)
    
    data=df[['title','image_thumbnail']]
    print(data)

    dico= data.to_dict(orient='record')
    print(dico)
    return render_template('results.html', results=dico)


if __name__ == '__main__':
    app.run(debug=True)