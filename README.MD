This is a simple sequential rule based python processor.
Rules can be configured in yaml files, new rules can be added/removed and existing rules can be modified. This enables changing the functionality without touching the code.

###### **Prerequisites:**
1. MongoDb
2. Apache kafka

**Example:**

We shall look at the below example.

1. Read a csv file with employee data (empid,name,designation,etc)
2. Lookup a datasource(mongo in this case) and pull more data about the employee - like vechicle info
3. Create a data containing combined data from the csv and mongo.
4. Send this record to a kafka topic

###### **Building the docker image:**

docker build -t pyrulesdemoimg:latest .

###### **Running the docker image (with mongo only):**

docker run -d -p 27017:27017 -v <your_local_directory_here>:/data pyrulesdemoimg:latest