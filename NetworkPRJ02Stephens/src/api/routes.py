'''
CS 3700 - Networking & Distributed Computing - Fall 2025
Instructor: Thyago Mota
Student(s): Andrew Stephens
Description: Project 02 - Incidents WS (routes)
'''

from typing import List
from typing import Union
from typing import Optional
from api import app, db
#from src.api import app, db
from api.models import Incident, Key
#from src.api.models import Incident, Key
from flask import request, jsonify


# TODO #3: complete the view function that returns a json with all of the incidents that satisfy the search criteria
@app.get('/incidents')
def get_incidents():

    """
    Returns a list of incidents that satisfy a search criteria
    
    """
    key = request.args.get('key')
    if not key:
        return jsonify({"error": "Unauthorized: invalid or missing API key"}), 401

    key_obj = db.session.query(Key).filter_by(key=key).first()
    if not key_obj:
        return jsonify({"error": "Unauthorized: invalid API key"}), 401

    slug = request.args.get('slug')
    event_date = request.args.get('event_date')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    actor = request.args.get('actor')
    actor_type = request.args.get('actor_type') 
    organization = request.args.get('organization')
    industry_code = request.args.get('industry_code', type=int)
    industry = request.args.get('industry')
    motive = request.args.get('motive')
    event_type = request.args.get('event_type')
    event_subtype = request.args.get('event_subtype')
    description = request.args.get('description')
    source_url = request.args.get('source_url')
    country = request.args.get('country')
    actor_country = request.args.get('actor_country')   
    offset = request.args.get('offset', default=0, type=int)
    
    query = db.session.query(Incident)

    if slug:
        query = query.filter(Incident.slug.ilike(f"%{slug}%"))
    if event_date:
        query = query.filter(Incident.event_date == event_date)
    if year:
        query = query.filter(Incident.year == year)
    if month:
        query = query.filter(Incident.month == month)
    if actor:
        query = query.filter(Incident.actor.ilike(f"%{actor}%"))
    if actor_type:
        query = query.filter(Incident.actor_type.ilike(f"%{actor_type}%"))
    if organization:
        query = query.filter(Incident.organization.ilike(f"%{organization}%"))
    if industry_code:
        query = query.filter(Incident.industry_code == industry_code)
    if industry:
        query = query.filter(Incident.industry.ilike(f"%{industry}%"))
    if motive:
        query = query.filter(Incident.motive.ilike(f"%{motive}%"))
    if event_type:
        query = query.filter(Incident.event_type.ilike(f"%{event_type}%"))
    if event_subtype:
        query = query.filter(Incident.event_subtype.ilike(f"%{event_subtype}%"))
    if description:
        query = query.filter(Incident.description.ilike(f"%{description}%"))
    if source_url:
        query = query.filter(Incident.source_url.ilike(f"%{source_url}%"))
    if country:
        query = query.filter(Incident.country.ilike(f"%{country}%"))
    if actor_country:
        query = query.filter(Incident.actor_country.ilike(f"%{actor_country}%"))

    incidents = query.offset(offset).all()

    if not incidents:
        return jsonify({"Error": "No incidents found matching the criteria"}), 404

    results = [incident.as_dict() for incident in incidents]
    return jsonify(results), 200