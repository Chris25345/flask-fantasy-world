import os
import psycopg2
from sqlalchemy import ARRAY

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS humanoids;')
cur.execute('CREATE TABLE humanoids (id serial PRIMARY KEY,'
                                 'name varchar (200) NOT NULL,'
                                 'gender varchar (200) NOT NULL,'
                                 'age integer NOT NULL,'
				 'race_id integer NOT NULL,'
				 'FOREIGN KEY(race_id) REFERENCES races(id));'
                                )
cur.execute('DROP TABLE IF EXISTS races cascade;')
cur.execute('CREATE TABLE races (id serial PRIMARY KEY,'
                                 'name varchar (200) NOT NULL);'
                                )
cur.execute('DROP TABLE IF EXISTS occupations cascade;')
cur.execute('CREATE TABLE occupations (id serial PRIMARY KEY,'
                                 'name varchar (200) NOT NULL);'
                                )

cur.execute('DROP TABLE IF EXISTS humanoids_occupations cascade;')
cur.execute('CREATE TABLE humanoids_occupations (humanoid_id integer NOT NULL,'
                                 'occupation_id integer NOT NULL);'
                                )                               

cur.executemany('INSERT INTO humanoids_occupations (humanoid_id, occupation_id) VALUES (%s, %s)',
            ((int(1),int(3)),
	    (int(2),int(1)),
            (int(3),int(2)),
            (int(4),int(4)),
            (int(5),int(3)),
            (int(6),int(2)),
            (int(7),int(4)),
            (int(8),int(2)),
            (int(9),int(4)),
            (int(10),int(2)),
	    (int(11),int(4)),
            (int(12),int(2)),
            (int(13),int(4)),
            (int(14),int(3)),
            (int(15),int(2)),
            (int(16),int(4)),
            (int(17),int(2)),
            (int(18),int(4)),
            (int(19),int(2)),
	    (int(20),int(4)),
            (int(21),int(4)),
            (int(22),int(2)),
            (int(23),int(4)),
            (int(24),int(3)),
            (int(25),int(2)),
            (int(26),int(4)),
            (int(27),int(2)),
            (int(28),int(4)),
            (int(29),int(2)),
	    (int(30),int(4)),
	    (int(31),int(4)),
            ))

cur.executemany('INSERT INTO humanoids (name, gender, age, race_id) VALUES (%s, %s, %s, %s)',
            (('Navrour','Female',int(489),int(1)),
	    ('Vixen','Female',int(200),int(3)),
            ('Kidmuc', 'Male',int(623),int(2)),
	    ('Elashor','Female',int(400),int(1)),
	    ('Skatrirlun','Male',int(100),int(2)),
	    ('Kate','Female',int(40),int(3)),
	    ('Navarre','Male',int(8000),int(1)),
	    ('Elmnith','Female',int(333),int(2)),
	    ('Othorion','Male',int(5600),int(1)),
	    ('Raven','Female',int(10000),int(1)),
            ('Logen','Female',int(200),int(3)),
            ('Mandragoran', 'Male',int(623),int(2)),
	    ('Jessica','Female',int(400),int(1)),
	    ('Anomander','Male',int(100),int(2)),
	    ('Jasnah','Female',int(40),int(3)),
	    ('Beric','Male',int(8000),int(1)),
	    ('Emreis','Female',int(333),int(2)),
	    ('Celebrimbor','Male',int(5600),int(1)),
	    ('Tattersail','Female',int(10000),int(1)),
	    ('Vic','Female',int(70),int(3)),
            ('Fordhugia','Female',int(200),int(3)),
            ('Alexandericked', 'Male',int(623),int(2)),
	    ('Coxbell','Female',int(400),int(1)),
	    ('Adath','Male',int(100),int(2)),
	    ('Cagturner','Female',int(40),int(3)),
	    ('Bennettzuzu','Male',int(8000),int(1)),
	    ('Morganadrina','Female',int(333),int(2)),
	    ('Gigantrper','Male',int(5600),int(1)),
	    ('Titanlton','Female',int(10000),int(1)),
	    ('Fangtterson','Female',int(70),int(3)),
            ('Antijimenez','Female',int(70),int(3))
            ))
cur.executemany('INSERT INTO races (name) VALUES (%s)',
            (('Elf',),
	    ('Dwarf',),
	    ('Human',)))
cur.executemany('INSERT INTO occupations (name) VALUES (%s)',
            (('Servant',),
            ('Merchant',),
            ('Warrior',),
            ('Scientist',)))
conn.commit()

cur.close()
conn.close()
