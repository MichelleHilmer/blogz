#validation for blog title and blog body not empty and leaves the previously 
#entered information

from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "cheeseburgersaregood"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(350))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')


@app.route("/blog", methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')

    if blog_id == None:
        blog_entries = Blog.query.all()
        return render_template('blog.html', blog_entries=blog_entries)

    else:
        blog_entry = Blog.query.get(blog_id)
        return render_template('post.html', blog_entry=blog_entry)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == "POST":
        title_post = request.form['title_post']
        blog_body = request.form['blog_body']
        title_error = ''
        body_error = ''

        if len(title_post) <= 0 :
            title_error = 'Please enter a blog title.'
            title_post = ''

        if len(blog_body) < 1 :
            body_error = 'Please enter a blog entry.'
            blog_body = ''


        if not title_error and not body_error:
            blog_entry = Blog(title_post, blog_body)
            db.session.add(blog_entry)
            db.session.commit()
            return render_template('post.html', blog_entry=blog_entry)

        else:
            return render_template('newpost.html', title_post=title_post, blog_body=blog_body, title_error=title_error,
            body_error=body_error)

    return render_template('newpost.html')




if __name__ == "__main__":
    app.run()
