# imports
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from pytz import timezone


# create Flask app instance
app = Flask(__name__)

# config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mainasm_website.db'

# create db instance
db = SQLAlchemy(app)

# timezone
east_africa_time = timezone('Africa/Nairobi')


# db model
class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  sender_fname = db.Column(db.String(50), nullable=False)
  sender_lname = db.Column(db.String(50), nullable=False)
  sender_email = db.Column(db.String(50), nullable=False)
  message = db.Column(db.String(2000), nullable=False)
  date_sent = db.Column(db.DateTime, default=datetime.now(east_africa_time))

  def __repr__(self):
    return f'<Message {self.id}: {self.message}, sent: {self.date_sent}, sender: {self.sender_fname} {self.sender_lname}>'


# routes
@app.route('/') 
def home():
  return redirect('/home')

@app.route('/home')
def index():
  return render_template('index.html')


@app.route('/contact-me', methods=['POST', 'GET'])
def contact_me():
  # collect data
  if request.method == 'POST': 
    s_fname = request.form['first_name']
    s_lname = request.form['last_name']
    s_email = request.form['email']
    msg = request.form['message']

    # new message
    new_message = Message(sender_fname=s_fname, sender_lname=s_lname, sender_email=s_email, message=msg)

    # update db
    try:
      db.session.add(new_message)
      db.session.commit()
      # test if messages are saved
      return redirect('/contact-me/test-if-messages-are-saved')

    except:
      return 'There was an error sendind your message!'
  
  # load contact page
  return render_template('contact.html')


@app.route('/contact-me/test-if-messages-are-saved')
def all_messages():
  all_messages_sent = Message.query.order_by(desc(Message.date_sent)).all()
  new_message = all_messages_sent[0]
  return render_template('test-messages.html', my_message=new_message, all_messages=all_messages_sent)


# projects
@app.route('/projects/1')
def project1():
  return render_template('portfolio-page.html')

@app.route('/projects/2')
def project2():
  return render_template('portfolioII-page.html')


# run app
if __name__ == '__main__':
  app.run(debug=True)
