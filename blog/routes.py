from flask import render_template, request, flash, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route("/")
def index():
   all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", all_posts=all_posts)

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id=0):
    errors = None
    if entry_id!=0:
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
    else:
       form = EntryForm()
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