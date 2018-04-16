from flask import Flask, request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy



app= Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)
app.secret_key = "asdfjkl!"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))


    def __init__(self,title,body):
        self.title=title
        self.body=body

@app.route("/blog")
def home():
    if request.args.get('id')==None:
        posts=Blog.query.all()
        return render_template("blog.html", title="My Posts",posts=posts)
    else:
        id=request.args.get('id')
        posts=Blog.query.filter_by(id=id).all()
        return render_template("blog-post.html", posts=posts)

@app.route("/submit")
def submit():
    return render_template("submit.html")

@app.route("/post-info", methods=['POST'])
def new_post():
    title=request.form['title']
    body=request.form['body']
    new_post=Blog(title,body)
    id=str(new_post.id)
    if title or body == "":
        flash("Make sure you enter a title and some content!")
        return render_template("submit.html", title=title,body=body)
    else:
        db.session.add(new_post)
        db.session.commit()
        return redirect("/blog?id="+id)


if __name__ == "__main__":
    app.run()