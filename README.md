# Politico_API
## Introduction
[![Build Status](https://travis-ci.org/erycoking/Politico_API.svg?branch=develop_v2)](https://travis-ci.org/erycoking/Politico_API)
[![Coverage Status](https://coveralls.io/repos/github/erycoking/Politico_API/badge.svg?branch=develop_v2)](https://coveralls.io/github/erycoking/Politico_API?branch=develop_v2)
[![Maintainability](https://api.codeclimate.com/v1/badges/46f93969162ab80fd0c4/maintainability)](https://codeclimate.com/github/erycoking/Politico_API/maintainability)

## Run in Postman
https://dl.pstmn.io/download/latest/linux64

### Features

1. A client will be able to add a user
2. A client will be able to update a user
3. A client will be able to delete a user
4. A client will be able to get a user
5. A client will be able to get all user
6. A client will be able to add a party
7. A client will be able to update a party
8. A client will be able to delete a party
9. A client will be able to get a party
10. A client will be able to get all parties
11. A client will be able to add a political seat/office
12. A client will be able to update a political seat/office
13. A client will be able to delete a political seat/office
14. A client will be able to get a political seat/office
15. A client will be able to get all political seat/office
16. A client will be able to add a candidate
17. A client will be able to vote
18. A client will be able to petition
19. A client will be able to view election results

### Installing

*step 1*

Clone the repository using the following command
```
git clone https://github.com/erycoking/Politico_API.git
``` 

Change directrory to Politico_API using the following command 
```
cd Politico_API
```

Create and activate a virtual environment
```
virtualenv venv
```
```
source venv/bin/activate
```

Install project dependencies
```
pip install -r requirements.txt
```

*step 2*

### Run the Application

``` python run.py```

*step 3*

### Test the Application
``` pytest```

## API ENDPOINTS FOR VERSION 1
### User Endpoint :/api/v1
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /users | Gets all users
GET | /users/int:id | Gets a single user
POST | /users | Adds a user
PATCH | /users | Updates a user
DELETE | /users/int:id | Deletes a user

### Party Endpoint :/api/v1
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /parties | Gets all parties
GET | /parties/int:id | Gets a single party
POST | /parties | Adds a party
PATCH | /parties | Updates a party
DELETE | /parties/int:id | Deletes a party

### Office Endpoint :/api/v1
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /offices | Gets all offices
GET | /offices/int:id | Gets a single office
POST | /offices | Adds a office
PATCH | /offices | Updates a office
DELETE | /offices/int:id | Deletes a office

### Candidate Endpoint :/api/v1
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /candidates | Gets all Candidates
GET | /candidates/int:id | Gets a single Candidate
POST | /candidates | Adds a Candidate
PATCH | /candidates | Updates a Candidate
DELETE | /candidates/int:id | Deletes a Candidate

## API ENDPOINTS FOR VERSION 2

### Auth Endpoint :/api/v2
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
POST | /auth/signup | User Sign up
POST | /auth/login | User Login

### User Endpoint :/api/v2
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /users | Gets all users
GET | /users/int:id | Gets a single user
PATCH | /users | Updates a user
DELETE | /users/int:id | Deletes a user

### Party Endpoint :/api/v2
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /parties | Gets all parties
GET | /parties/int:id | Gets a single party
POST | /parties | Adds a party
PATCH | /parties | Updates a party
DELETE | /parties/int:id | Deletes a party

### Office Endpoint :/api/v2
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /offices | Gets all offices
GET | /offices/int:id | Gets a single office
POST | /offices | Adds a office
PATCH | /offices | Updates a office
DELETE | /offices/int:id | Deletes a office

### Candidate Endpoint :/api/v2
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /office/int:id/candidates | Gets all Candidates belonging to a particular office
GET | /office/int:id/candidates/int:id | Gets a single Candidate belonging to a particular office
POST | /office/int:id/register | Adds a Candidate to a particular office
PATCH | /office/int:id/candidates | Updates a Candidate belonging to a particular office
DELETE | /office/int:id/candidates/int:id | Deletes a Candidate belonging to a particular office

### Vote Endpoint :/api/v2
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /votes | Gets all votes
GET | /offices/int:id/result | Gets votes for a single office
POST | /votes | Cast a votes

### Petition Endpoint :/api/v2
METHOD | ENDPOINT | FUNCTIONALITY
-------|-----------|--------------
GET | /petitions | Gets all petitions
GET | /petitions/int:id | Gets a single petition
POST | /petitions | Adds a petition
PATCH | /petitions | Updates a petition
DELETE | /petitions/int:id | Deletes a petition

