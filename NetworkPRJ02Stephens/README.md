[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Br9IXfp-)
# Overview

Web services are essential components of distributed applications, enabling controlled access to datasets through mechanisms such as authentication, pagination, and search parameters. The objective of this project is to design and implement a web service from scratch, based on a provided dataset and a set of functional requirements. This includes:

* Defining a clear and well-structured API; 
* Implementing authentication and access control; and 
* Supporting pagination and search/filtering capabilities.

In addition to building the web service, you are also required to develop a client application that interacts with the service, demonstrating its functionality and usage. 

# Instructions 

In this project, you are tasked with implementing a web service for sharing cybersecurity incidents. The dataset for this project was originally obtained from the [Cyber Events Database Home](https://cissm.umd.edu/research-impact/publications/cyber-events-database-home) and has been provided to you in CSV format at: [data/incidents.csv](data/incidents.csv). 

Alternatively, you may choose to build a web service using a different dataset. However, your implementation must meet the minimum functionality requirements outlined in this document. If you decide to use a different dataset, please consult with your instructor early in the process to ensure your project remains aligned with the expectations.

You are required to use the tools discussed in class to build web services, including Python and the Flask web app framework. 

Begin this project by creating and activatating your local virtual environment, followed by installing all of the required Python libraries in [requirements.txt](requirements.txt). 

```
pip3 install -r requirements.txt
```

Your first task is to complete the TODO in [src/init_db.py](src/init_db.py) and populate your SQLite database with all the incidents from the CSV file. Be sure to run [src/init_db.py](src/init_db.py) from the project's main folder, not from the src directory.

Once the database is populated, proceed to the TODO in [src/api/models.py](src/api/models.py), where the **Incident** class model is defined. This model should accurately represent the structure of the incident data stored in the database.

Next, implement the view function **get_incidents**, which returns all incidents that match the search criteria in JSON format. If a valid key is not provided, the service should return an unauthorized message. If no incidents match the search, a 404 error should be returned. The search criteria may include the following optional parameters: event_date, month, year, actor, actor_type, organization, industry_code, industry, motive, event_type, event_subtype, country, actor_country, and offset. Note that month, year, and industry_code are integers, while all other parameters are strings. If offset is not specified, it should default to 0.

Finally, complete the implementation of a client script that prompts the user—either via command-line arguments or interactive input—for the following parameters: key, year, and country. The client should then query the web service and display the description of all matching incidents.

# Evaluation 

You are NOT required to deploy the API. However, I should be able to run it locally starting flask from the project's folder using: 

```
export FLASK_APP=src/api
flask run
```

# Rubric 

```
+25 data is loaded correctly from the CSV dataset 
+25 Incidents model is implemented correctly based on the incidents' table columns
+28 API works with each of the search criteria (14x2)
+6 API checks the key for authorization
+6 The API returns a 404 error when no results are found for the search.
+10 The API client
```