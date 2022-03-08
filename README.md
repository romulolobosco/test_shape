# TEST SHAPE

- [TEST SHAPE](#test-shape)
  - [Dependencies](#dependencies)
  - [How to run](#how-to-run)
  - [Process of solving](#process-of-solving)
    - [Processing files](#processing-files)
      - [Log file](#log-file)
      - [Storage](#storage)
    - [Answer](#answer)

## Dependencies
- docker
- docker-compose

## How to run
1. build the spark stand alone image with the command "make build-image"
2. start the infrastructure with the command "make start-infra"

## Process of solving

### Processing files
On a first look at the files I conclude that "equipment.json" and "equipment_sensors.csv" was pretty straight forward and none major process was needed. The log file in the other hand needed some process. Initially my thought was to read the file as text and use regex to split the data into columns, but read the file as csv and set the separator as blank space was actualy easier.

#### Log file
Treating the file log as a csv file leave me with the result bellow:

|_c0|_c1|_c2|_c3|_c4|_c5|_c6|
|-- |-- |-- |-- |-- |-- |-- |
|[2019-12-10 10:46:09]|ERROR|sensor[5]:|(temperature|365.26,|vibration|-6305.32)|
|[2019-12-10 10:46:09]|ERROR|sensor[43]:|(temperature|458.47,|vibration|-58.41)|

By doing that the amount of transform was reduced to:
- Extract date from column _c0
- Extract the sensor id from column _c2
- Remove a single character from columns _c4 and _c6

For the first column, a simple parse from string to timestamp solve the problem. For columns *_c2*, *_c4* and *_c6* I used regex to extract the useful information. Then I assign some meaningful names to the columns.

#### Storage
To store the data processed I created a table and schema named *shape* on a postgres database and the relation beetwen files and table can be found bellow:
|file_name|table_name|
|--|--|
|equipment_failure_sensors|sensors_log|
|equipment_sensors|equipment_sensors|
|equipment|equipment_group|


### Answer
The answers for the questions asked on the challeng can be found on the folder "sql". There on query for each question and the name of the files match the "number" of the question and the question it self.
