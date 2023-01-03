import os
from flask import Flask, render_template, request
from math import ceil
from flask_sqlalchemy import SQLAlchemy

# basic_query = 'SELECT humanoids.name, humanoids.gender, humanoids.age, races.name, occupations.name FROM humanoids INNER JOIN races ON humanoids.race_id=races.id INNER JOIN humanoids_occupations ON humanoids_occupations.humanoid_id=humanoids.id INNER JOIN occupations ON humanoids_occupations.occupation_id=occupations.id'
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

class Link:
  def __init__(self, link, page):
    self.link = link
    self.page = page
  
class WorldInfo:
  def __init__(self, servant_count, merchant_count, warrior_count, scientist_count, human_count, dwarf_count, elf_count):
    self.servant_count = servant_count
    self.merchant_count = merchant_count
    self.warrior_count = warrior_count
    self.scientist_count = scientist_count
    self.human_count = human_count
    self.dwarf_count = dwarf_count
    self.elf_count = elf_count

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
  
def get_world_info(humanoids):
  servant_count = 0
  merchant_count = 0
  warrior_count = 0 
  scientist_count = 0
  human_count = 0
  dwarf_count = 0 
  elf_count = 0

  for humanoid in humanoids:
    if humanoid.race:
      if humanoid.race == 'Elf':
        elf_count += 1
      elif humanoid.race == 'Dwarf':
        dwarf_count += 1
      elif humanoid.race == 'Human':
        human_count += 1
    
    if humanoid.occupation:
      if humanoid.occupation == 'Servant':
        servant_count += 1
      elif humanoid.occupation == 'Merchant':
        merchant_count += 1
      elif humanoid.occupation == 'Warrior':
        warrior_count += 1
      elif humanoid.occupation == 'Scientist':
        scientist_count += 1
  
  return WorldInfo(servant_count, merchant_count, warrior_count, scientist_count, human_count, dwarf_count, elf_count)


@app.route('/',  methods=['GET'], defaults={"page": 1})
@app.route('/<int:page>', methods=['GET'])
def index(page):
  humanoids = get_humanoids().paginate(page=page,per_page=10,error_out=False)
  pages = get_pages(humanoids.total)
  links = []
  for page in pages:
    links.append(Link(f'/{page}', page))
  humanoid_list = format_humanoids(humanoids.items)
  world_info = get_world_info(humanoid_list)
  return render_template('index.html',humanoids=humanoid_list,links=links,cur_page=humanoids.page, world_info=world_info)


@app.route('/search/<int:page>', methods=['GET'])
def search(page):
  query_string = request.query_string.decode("utf-8")
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
  links = []
  for page in pages:
    links.append(Link(f'/search/{page}?{query_string}', page))
  humanoids = format_humanoids(humanoid_list.items)
  world_info = get_world_info(humanoids)
  return render_template('index.html',humanoids=humanoids,links=links,cur_page=humanoid_list.page,world_info=world_info)

@app.route('/sort/<int:page>', methods=['GET'])
def sort(page):
  query_string = request.query_string.decode("utf-8")
  sort_choise = request.args.get('sort')
  humanoid_list = []

  if sort_choise == 'age':
    humanoid_list = get_humanoids().order_by(Humanoids.age.asc()).paginate(page=page,per_page=10,error_out=False)
  elif sort_choise == 'name':
    humanoid_list = get_humanoids().order_by(Humanoids.name.asc()).paginate(page=page,per_page=10,error_out=False)
  else:
    humanoid_list = get_humanoids().paginate(page=page,per_page=10,error_out=False)
  
  pages = get_pages(humanoid_list.total)
  humanoids = format_humanoids(humanoid_list.items)
  world_info = get_world_info(humanoids)
  links = []
  for page in pages:
    links.append(Link(f'/sort/{page}?{query_string}', page))
  return render_template('index.html',humanoids=humanoids,links=links,cur_page=humanoid_list.page,world_info=world_info)
  
    
if __name__ == "__main__":
  app.run(debug=True)