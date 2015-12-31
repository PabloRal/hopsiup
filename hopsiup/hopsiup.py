import sqlite3
from flask import Flask, request, session, g, redirect, \
     abort, render_template, flash, url_for

app = Flask(__name__)
app.config.from_object('init')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_main():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' +\
            'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('show_links.html', links=links)

@app.route('/user')
def user_account():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' +\
            'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('user_account.html', links=links)

@app.route('/articles_stat')
def user_articles_stat():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' +\
            'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('user_stat_articles.html', links=links)

@app.route('/blog_stat')
def user_blog_stat():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' +\
            'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('user_stat_blog.html', links=links)

@app.route('/social_stat')
def user_social_stat():
    data = g.db.execute('select l.lpoints, l.link_id, l.title, l.description, u.login from links as l,' +\
            'users as u on l.user_id = u.user_id order by lpoints desc')
    links = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], user=row[4]) for row in data.fetchall()]
    return render_template('user_stat_social.html', links=links)

@app.route('/l/<id>')
def show_link_page(id=None):
    data = g.db.execute('select l.lpoints, l.link, l.title, l.description, u.login from links as l,' +
            'users as u on l.user_id == u.user_id where l.link_id={0}'.format(id))
    link_infos = [dict(points=row[0], id=row[1], title=row[2], desc=row[3], author=row[4]) for row in data.fetchall()]
    return render_template('link_page.html', link_info=link_infos[0])

@app.route('/add', methods=['POST'])
def add_link():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into links (link, title, user_id) values (?, ?)',
                 [request.form('url'), request.form['title'], request.form['user_id']])

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = g.db.execute('select login, password from users')
        users_from_db = [dict(login=row[0], password=row[1])\
                for row in data.fetchall()]
        print(users_from_db)
        for row in users_from_db:
            if row["login"] == username and row["password"] == password:
                session['logged_in'] = True
                session['user'] = username
                flash('Zalogowano pomyślnie!')
                return redirect(url_for('show_main'))
        error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_main'))

@app.route('/ranking')
def ranking():
    data = g.db.execute('select login, upoints from users order by upoints')
    users = [dict(login=row[0], points=row[1]) for row in data.fetchall()]
    return render_template('ranking.html', users=users)

if __name__ == '__main__':
    app.run()
