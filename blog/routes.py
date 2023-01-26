from flask import render_template, request, flash, redirect, url_for, session
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
from blog.data_manager import DataManager
import functools

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('You are now logged out.', 'success')
    return redirect(url_for('index'))

@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get('next')
   if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  # Use cookie to store session.
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('index'))
       else:
           errors = form.errors
   return render_template("login_form.html", form=form, errors=errors)

@app.route("/")
def index():
   all_posts = data_manager.get_all_posts()
   return render_template("homepage.html", all_posts=all_posts)

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    errors = None
    header=f"Edycja wpisu nr {entry_id}"
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
            flash('Post został zedytowany!')
            all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
            return render_template("homepage.html", all_posts=all_posts)
        else:
            flash('Próba modyfikacji wpisu nieudana!')
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors, header=header)

@app.route("/new_post/", methods=["GET", "POST"])
@login_required
def new_post():
    form = EntryForm()
    errors = None
    header='Dodaj nowy wpis'
    if request.method == 'POST':
        if form.validate_on_submit():
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
            flash('Dodano nowy post')
            all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
            return render_template("homepage.html", all_posts=all_posts)
        else:
            flash('Próba dodania wpisu nieudana!')
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors, header=header)