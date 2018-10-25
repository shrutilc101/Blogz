from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:Blogz18@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(360))
    post = db.Column(db.String(5000))
    
    def __init__(self,title,post):
        self.title = title
        self.post = post

@app.route('/blog')
def display_blog():
    blog_id = request.args.get('id')
    if(blog_id):
        a_post = Blog.query.get(blog_id)
        return render_template('post.html', blog=a_post)
    else:
        a_all_post = Blog.query.all()
        return render_template('blogp.html',blogs=a_all_post)




@app.route('/newpost',methods=['POST', 'GET'])
def newpost():
    blog_title = ''
    blog_post = ''
    blog_title_error = ''
    blog_post_error = ''

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
            new_blog = Blog(blog_title,blog_post)
            db.session.add(new_blog)
            db.session.commit()
            post_link = "/blog?id=" + str(new_blog.id)
            return redirect(post_link)
        
        return redirect('/blog')

    return render_template('/npost.html', title = 'Add a new Blog', blog_title=blog_title, blog_post=blog_post, blog_title_error=blog_title_error, blog_post_error=blog_post_error)

    

if __name__ =='__main__':
    app.run()