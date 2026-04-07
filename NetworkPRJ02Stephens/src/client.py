'''
CS 3700 - Networking & Distributed Computing - Fall 2025
Instructor: Thyago Mota
Student(s): Andrew Stephens
Description: Project 02 - Incidents WS (models)
'''
import requests
import sys

API_URL = 'http://127.0.0.1:5000/incidents'

print("Prompt:: Provide API key, year, and country to search for incidents.:\n")
if len(sys.argv) == 4:
    key = sys.argv[1]
    year = sys.argv[2]
    country = sys.argv[3]
else:
    key = input("Enter API Key: ")
    year = input("Enter Year: ")
    country = input("Enter Country: ")

response = requests.get(API_URL, params={'key': key, 'year': int(year), 'country': country})

if response.status_code == 200:
    incidents = response.json() 
    if incidents:
        print(f"{len(incidents)} incidents found:\n")
        for inc in incidents:
            print(f"- {inc['description']}")
    else:
        print("No incidents matched the search criteria.")
elif response.status_code == 401:
    print("Unauthorized: Invalid API key.")
elif response.status_code == 404:
    print("No incidents found.")
else:
    print(f"Error {response.status_code}: {response.text}")

if __name__ == '__main__':

    pass