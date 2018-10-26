from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:Blogz18@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "very_secretkey"
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(360))
    post = db.Column(db.String(5000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self,title,post,author):
        self.title = title
        self.post = post
        self.author = author

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    author = db.relationship('Blog', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['display_blog', 'login', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


def empty_value(x):
    if x:
        return True
    else:
        return False

def character_length(x):
    if len(x)>2 and len(x)<21:
        return True
    else:
        return False


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

    # Create empty strings for the error messages
        username_error = ""
        password_error = ""
        verify_error = ""

        if not empty_value(username):
            username_error="Required field."

        if not character_length(username):
            username_error="Must be between 3 and 20 characters."

        else:
            if " " in username:
                username_error="Spaces not allowed!"

        if not empty_value(password):
            password_error="Required field."

        if not character_length(password):
            password_error="Must be between 3 and 20 characters."

        else:
            if " " in password:
                password_error="Spaces not allowed!"

        if verify != password:
            verify_error="Passwords do not match."
                
        if not username_error and not password_error and not verify_error:
            existing_user = User.query.filter_by(username=username).first()
            
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
        
            else:
                flash("That Username already exis",)
                return redirect ('/signup')

            return redirect('/newpost')
        return render_template("signup.html", username=username, username_error=username_error, password=password, password_error=password_error, verify_error=verify_error, verify=verify)

    else:
        return render_template("signup.html",)

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')


@app.route('/blog')
def display_blog():
    if "user" in request.args:
        user_id = request.args.get("user")
        user = User.query.get(user_id)
        user_blogs = Blog.query.filter_by(author=user).all()
        
        return render_template("singleUser.html", page_title=user.username, user_blogs=user_blogs)
    a_blog = request.args.get('id')
    if(a_blog):
        a_post = Blog.query.get(a_blog)
        return render_template('post.html', blog=a_post)
    else:
        a_all_post = Blog.query.all()
        return render_template('blogp.html', page_title="All Blogs", blogs=a_all_post)



@app.route('/newpost',methods=['POST', 'GET'])
def newpost():
    blog_title = ''
    blog_post = ''
    blog_title_error = ''
    blog_post_error = ''

    author = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_post = request.form['post']

        if blog_title == "":
            blog_title_error = "Please enter the title of your blog."
            
            return render_template('/npost.html', blog_post=blog_post, blog_title_error=blog_title_error)
        
        
        if blog_post == "":
            blog_post_error = "Please add some text in your blog"

            return render_template('/npost.html', blog_title=blog_title, blog_post_error=blog_post_error)

        else:
            new_blog = Blog(blog_title,blog_post,author)
            blog = Blog.query.filter_by(author=author)
            db.session.add(new_blog)
            db.session.commit()
            post_link = "/blog?id=" + str(new_blog.id)
            return redirect(post_link)
        
        return redirect('/blog')

    return render_template('/npost.html', title = 'Add a new Blog', blog_title=blog_title, blog_post=blog_post, blog_title_error=blog_title_error, blog_post_error=blog_post_error)

@app.route('/', methods = ['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)   

if __name__ =='__main__':
    app.run()