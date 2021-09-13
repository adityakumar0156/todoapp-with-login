from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # creating the Flask class object
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///info_user.db"

app.secret_key="hello"

#app.config['SQLALCHEMY_DATABASE_URI'] =f"sqlite:///{}.db"


db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class info(db.Model):#class ka naam table k naam se match krna chahiye
    sno = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"{self.email}--{self.password}"


class info_user(db.Model):#class ka naam table k naam se match krna chahiye
    sno = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    id = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"{self.email}--{self.password}"

@app.route('/')  # decorator drfines the
def home():
    if 'email' in session:
        email=session['email']
        data = info_user.query.all()
        data.reverse()
        return render_template('profile.html',email=email,data=data)
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #check user exist or not and the log in
        data = info.query.all()
        flag_email = False
        for i in data:
            if i.email==email:
                flag_email=True
                if i.password == password:
                    flag_pass = True
                    print("user found")
                    session['email'] = i.email
                    s = session['email']
                    #we can also pass data
                    data = info_user.query.all()
                    data.reverse()
                    return render_template('profile.html', email=s,data=data)
                else:
                    error = "Incorrect password"
                    return render_template('login.html', error=error, email=email)
        if flag_email ==False:
            error="No such user exist"
            return render_template('login.html',error=error)

    if 'email' in session:
        s = session['email']
        data=info_user.query.all()
        data.reverse()
        return render_template('profile.html', email=s,data=data)
    else:
        print("going to set session")
        return render_template('login.html')


@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        #check and validate
        data = info.query.all()
        flag_email = True
        flag_pass=False
        for i in data:

            if i.email == email:
                flag_email = False
                error="Email already exist"
                print(error)
                return render_template('signin.html',error=error)

        if len(password)>5:
            flag_pass=True
        if len(password)<=5:
            error="Password length must be greater than five."
            print(error)
            return render_template('signin.html', error=error,email=email)
        if flag_email == True and flag_pass==True:
            #way to email and password is clear
            entry = info(password=password, email=email)
            db.session.add(entry)
            db.session.commit()

    if 'email' in session:
        s = session['email']
        data=info_user.query.all()
        data.reverse()
        return render_template('profile.html', email=s,data=data)
    else:
        return render_template('signin.html')

@app.route('/logout')
def logout():
    #delete session and redirect user to home page
    session.pop('email',None)
    return render_template('index.html')

@app.route('/delete/<int:i>')
def delete(i):
    if 'email' in session:
      try:
        data = info_user.query.filter_by(sno=i).first()
        db.session.delete(data)
        db.session.commit()
      except:
        print("Error occured while deleting")
      data=info_user.query.all()
      data.reverse()
      return render_template('profile.html',data=data,email=session['email'])
    else:
        return render_template('login.html')


@app.route('/update/<int:i>',methods=['POST','GET'])
def update(i):
    if 'email' in session:
       try:
        if request.method=='POST':
            email=request.form.get('email')
            password=request.form.get('password')
            data = info_user.query.filter_by(sno=i).first()
            data.email = email
            data.password = password
            db.session.add(data)
            db.session.commit()
            data = info_user.query.all()
            data.reverse()
            return render_template('profile.html',data=data,email=session['email'])
        data = info_user.query.filter_by(sno=i).first()
        return render_template('update.html',data=data)
       except:
           print("Error occured while updating data")
    else:
        return render_template('login.html')

@app.route('/profile',methods=['POST','GET'])
def profile():
    if 'email' in session:
        if request.method=='POST':
            email=request.form.get('email')
            password=request.form.get('password')
            entry = info_user(password=password, email=email,id=session['email'])
            db.session.add(entry)
            db.session.commit()
        data = info_user.query.all()
        data.reverse()
        s = session['email']
        return render_template('profile.html', email=s,data=data)
    else:
        print("going to set session")
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)