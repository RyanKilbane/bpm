# BPM: Better Process Modeling
The Better Process Modeler is a basic workflow managment tool.
# Running
Running the modeler is simple: do a pull then run 
```bash 
pip3 install -r requirements.txt
python3 application.py
```
And the application should run with it's basic configuration.

# Configuration
The main driving idea behind the Better Process Modeler is complete end user configuration, but it keep the configuration simple and easy. The way this is achived is twofold:
- Heavy use of SQLAlchemys' reflection coupled with Pythons nice metaprogramming

This allows us to just define a set of database tables and then run the present programme, which would then be reflected in the code and the classes that constitute the O part of the ORM can be constructed dynamically.

- A yaml file that holds some further configuration.

This allows further flexability over the table names and APIs.

 __Documentation on this file is still to come__

## A Note on Reflection in BPM
For SELECT and INSERT queries, we have achived complete flexability using reflectiona and metaprogramming. However, right now the dream of complete flexablity is still a little far away, this is down to the use of raw SQL statements in UPDATE queries. Some further experiementation needs to be done on this matter.

## APIs
Some brief notes on the APIs
### Ingest (/ingest)
Step 1. Data is posted to the API, a UUID is added and then persisted in the database. Before it is sent to the Data Prep Lambda function
### Tracking (/tracking)
The tracking API serves as a generic endpoint where tracking data can be posted for review.
### Allocations (/allocate)
If an ingested dataset has had issues raised against it, then it will need to be allocated. That is done here. Allocation takes place in a round robin-esq way, whereby the user who was allocated something the longest time ago will be allocated the something.
### Users (/users)
Exposes operations to be preformed on the User table.
