'''
CS 3700 - Networking & Distributed Computing - Fall 2025
Instructor: Thyago Mota
Student: Andrew Stephens
Description: Project 02 - Incidents WS (db initialization)
Observation: RUN IT FROM THE MAIN PROJECT'S FOLDER
'''

import sqlite3
import csv
import os


try: 
    os.makedirs('instance')
except: 
    pass

conn = sqlite3.connect('instance/incidents.db')

with open('src/incidents.sql') as f:
    conn.executescript(f.read())

conn.commit()
# load incidents data
cur = conn.cursor()
count = 0

# TODO #1: populate the incidents table (defined in src/incidents.sql) from data/incidents.csv
with open('data/incidents.csv', 'rt', encoding = 'utf-8', errors = 'ignore') as g:
    reader = csv.DictReader(g)
    for row in reader:
       # print(row)
        slug = row['slug']
        event_date = row['event_date']
        year = int(row['year'])
        month = int(row['month'])
        actor = row['actor']
        actor_type = row['actor_type']
        organization = row['organization']   
        industry_code = int(row['industry_code']) 
        industry = row['industry']
        motive = row['motive']
        event_type = row['event_type']
        event_subtype = row['event_subtype']
        description = row['description']
        source_url = row['source_url']   
        country = row['country']
        actor_country = row['actor_country']
        sql = 'INSERT INTO incidents(slug, event_date, year, month, actor, actor_type, organization, industry_code, industry, motive, event_type, event_subtype, description, source_url, country, actor_country) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )'
        cur.execute(sql,[slug, event_date, year, month, actor, actor_type, organization, industry_code, industry, motive, event_type, event_subtype, description, source_url, country, actor_country])
    conn.commit()
pass

sql = 'SELECT COUNT(*) FROM incidents'
cur.execute(sql)
row = cur.fetchone()
print("Success: \n")
print(row[0], 'incidents inserted!')
conn.close()


