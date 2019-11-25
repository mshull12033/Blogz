from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/buildABlog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class bPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(500))
    posted = db.Column(db.Boolean)

    def __init__(self, name,body):
        self.name = name
        self.posted = False
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():

    
       

    posts = bPost.query.all()
    completed_posts = bPost.query.filter_by(posted=True).all()
    
    return render_template('post.html',title="Add post", 
        posts=posts, completed_posts=completed_posts)
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        post_name = request.form['post']
        postId =  request.args.get('id')
        post_entry = bPost.query.filter_by(id = postId).first()
       
       
        post_body = request.form['post_body']
        new_post = bPost(post_name,post_body)
        db.session.add(new_post)
        
        db.session.commit()
    return render_template('showaddedpost.html',postId = postId,new_post = new_post)


@app.route('/delete-post', methods=['POST'])
def delete_post():

    post_id = int(request.form['post-id'])
    post = bPost.query.get(post_id)
    post.posted = True
    db.session.add(post)
    db.session.add(post_body)
    db.session.commit()

    return render_template('showpost.html',post_id = post_id)
@app.route('/addpost', methods=['POST', 'GET'])
def addpost():
    
    return render_template('addpost.html')
@app.route('/post', methods=['GET'])
def post():
    
   
        
       
       
        

    if request.args.get('id') is not None:
        postId =  request.args.get('id')
        post_entry = bPost.query.filter_by(id = postId).first()
        
        return render_template('showpost.html',id=id,post_entry = post_entry)

        



    return render_template('post.html',post_id = post_id)



if __name__ == '__main__':
    app.run()