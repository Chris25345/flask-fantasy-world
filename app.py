import os
import psycopg2
from flask import Flask, render_template, request
from math import ceil
from flask_sqlalchemy import SQLAlchemy

basic_query = 'SELECT humanoids.name, humanoids.gender, humanoids.age, races.name, occupations.name FROM humanoids INNER JOIN races ON humanoids.race_id=races.id INNER JOIN humanoids_occupations ON humanoids_occupations.humanoid_id=humanoids.id INNER JOIN occupations ON humanoids_occupations.occupation_id=occupations.id'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
  user=os.environ['DB_USERNAME'],
  pw=os.environ['DB_PASSWORD'],
  host="localhost",
  port="5432",
  db="flask_db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

class Humanoids(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200),nullable=False)
  gender = db.Column(db.String(200),nullable=False)
  age = db.Column(db.Integer,nullable=False)
  race_id = db.Column(db.Integer,db.ForeignKey('races.id'),nullable=False)

class Races(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200),nullable=False)

class Occupations(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200),nullable=False)

class Humanoids_Occupations(db.Model):
  __tablename__ = 'humanoids_occupations'
  id = db.Column(db.Integer, primary_key=True)
  humanoid_id = db.Column(db.Integer,db.ForeignKey('humanoids.id'),nullable=False)
  occupation_id = db.Column(db.Integer,db.ForeignKey('occupations.id'),nullable=False)

class Humanoid:
  def __init__(self, name, age, gender, race, occupation):
    self.name = name
    self.gender = gender
    self.age = age
    self.race = race
    self.occupation = occupation

def format_humanoids(humanoids):
  humanoid_list = []
  for humanoid in humanoids:
    new_humanoid = Humanoid(humanoid[0], humanoid[1], humanoid[2], humanoid[3], humanoid[4])
    humanoid_list.append(new_humanoid)
  return humanoid_list 

def get_pages(total):
  page_count = ceil(total / 10)
  pages = []
  curr_page = 1
  while curr_page <= page_count:
    pages.append(curr_page)
    curr_page = curr_page + 1
  return pages

def get_humanoids():
  return db.session.query(Humanoids.name, Humanoids.age, Humanoids.gender, Races.name, Occupations.name)\
    .join(Races, Humanoids.race_id==Races.id)\
    .join(Humanoids_Occupations, Humanoids_Occupations.humanoid_id==Humanoids.id )\
    .join(Occupations, Humanoids_Occupations.occupation_id==Occupations.id)

@app.route('/',  methods=['GET'], defaults={"page": 1})
@app.route('/<int:page>', methods=['GET'])
def index(page):
  humanoids = get_humanoids().paginate(page=page,per_page=10,error_out=False)
  pages = get_pages(humanoids.total)
  humanoid_list = format_humanoids(humanoids.items)
  return render_template('index.html',humanoids=humanoid_list,pages=pages,cur_page=humanoids.page)


@app.route('/<int:page>/search', methods=['GET'], defaults={"page": 1})
def search(page):
  selected_race = request.args.get('race')
  selected_occupation = request.args.get('occupation')
  selected_gender = request.args.get('gender')
  humanoid_list = []
  gender = 'Female' if selected_gender == '1' else 'Male'

  if selected_race:
    if selected_occupation:
      if selected_gender:
        humanoid_list = get_humanoids().filter(Races.id==selected_race,Occupations.id==selected_occupation,Humanoids.gender==gender).paginate(page=page,per_page=10,error_out=False)
      else:
        humanoid_list = get_humanoids().filter(Races.id==selected_race,Occupations.id==selected_occupation).paginate(page=page,per_page=10,error_out=False)
    else:
      if selected_gender:
        humanoid_list = get_humanoids().filter(Races.id==selected_race,Humanoids.gender==gender).paginate(page=page,per_page=10,error_out=False)
      else:
        humanoid_list = get_humanoids().filter(Races.id==selected_race).paginate(page=page,per_page=10,error_out=False)
  else:
    if selected_occupation:
      if selected_gender:
        humanoid_list = get_humanoids().filter(Occupations.id==selected_occupation,Humanoids.gender==gender).paginate(page=page,per_page=10,error_out=False)
      else:
        humanoid_list = get_humanoids().filter(Occupations.id==selected_occupation).paginate(page=page,per_page=10,error_out=False)
    else:
      if selected_gender:
        humanoid_list = get_humanoids().filter(Humanoids.gender==gender).paginate(page=page,per_page=10,error_out=False)
      else:
        humanoid_list = get_humanoids().paginate(page=page,per_page=10,error_out=False)

  pages = get_pages(humanoid_list.total)
  humanoids = format_humanoids(humanoid_list.items)
  return render_template('index.html',humanoids=humanoids,pages=pages,cur_page=humanoid_list.page)

@app.route('/<int:page>/sort', methods=['GET'], defaults={"page": 1})
def sort(page):
  sort_choise = request.args.get('sort')
  humanoid_list = []

  if sort_choise == 'age':
    humanoid_list = get_humanoids().order_by(Humanoids.age.desc()).paginate(page=page,per_page=10,error_out=False)
  elif sort_choise == 'name':
    humanoid_list = get_humanoids().order_by(Humanoids.name.desc()).paginate(page=page,per_page=10,error_out=False)
  else:
    humanoid_list = get_humanoids().paginate(page=page,per_page=10,error_out=False)
  
  pages = get_pages(humanoid_list.total)
  humanoids = format_humanoids(humanoid_list.items)
  return render_template('index.html',humanoids=humanoids,pages=pages,cur_page=humanoid_list.page)
  
    
if __name__ == "__main__":
  app.run(debug=True)