from flask import Flask, request, redirect, render_template,session,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20))
    password = db.Column(db.String(15))
    blogs = db.relationship('bPost', backref = 'blog_ID')
    def __init__(self,userName,password):
        self.userName = userName
        self.password = password

class bPost(db.Model):
    __tablename__ = "bPost"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(500))
    posted = db.Column(db.Boolean)
    blog_Identification = db.Column(db.Integer,db.ForeignKey('User.id'))

    def __init__(self, name,body,blog_ID):
        self.name = name
        self.posted = False
        self.body = body
        self.blog_ID = blog_ID
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','post','index']
    if request.endpoint not in allowed_routes and 'userName' not in session:
        return redirect('/login')



@app.route('/', methods=['POST', 'GET'])
def index():

    
       

    posts = bPost.query.all()
    completed_posts = bPost.query.filter_by(posted=True).all()
    users = User.query.all()
    
    return render_template('post.html',title="Add post", 
        posts=posts, completed_posts=completed_posts,users = users)
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_Id = User.query.filter_by(userName=session['userName']).first()
        post_name = request.form['post']
        postId =  request.args.get('id')
        post_entry = bPost.query.filter_by(id = postId).first()
       
       
        post_body = request.form['post_body']
        new_post = bPost(post_name,post_body,blog_Id)
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
        blog_record = User.query.filter_by(userName=session['userName']).first()
        
        return render_template('showpost.html',id=id,post_entry = post_entry, blog_record = blog_record)

        



    return render_template('post.html',post_id = post_id)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        user = User.query.filter_by(userName=userName).first()
        if user and user.password == password:
            session['userName'] = userName
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')
         

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        verify = request.form['verify']


        existing_user = User.query.filter_by(userName=userName).first()
        if userName == "" or password == "" :
            flash("One or more feilds are blank - please fill out all feilds", 'error')
        elif password != verify :
            flash("password and verification feilds do not match - please be sure to enter the same password into both feilds",'error')
        elif len(password) < 3 :
            flash("password must be at least 4 charaters long","error")
        elif not existing_user:
            new_user = User(userName, password)
            db.session.add(new_user)
            db.session.commit()
            session['userName'] = userName
            return redirect('/signup')
        else:
            
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')
@app.route('/logout')
def logout():
    del session['userName']
    return redirect('/')
@app.route('/index')
def Index():
    users = User.query.all()
    return render_template('index.html',users = users)
@app.route('/user')
def user():
    users = User.query.filter_by(userName = request.args.get('userName')).first()
    print('\n')
    print(users.id)
    print('\n') 
    usersId = bPost.query.filter_by(blog_Identification = users.id).all()
    print(usersId)
    print('\n')
    return render_template('post.html',posts = usersId)



if __name__ == '__main__':
    app.run()