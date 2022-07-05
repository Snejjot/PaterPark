To start the app: docker-compose up

App starts on port 5000 by default

Tests run before start

SQLite db added with some initial data
POST accept both json and form-data

pandas used for filtering. search-plate example in the task contain duplicate numbers with different timestamp. This means that in some time there will be really big amount of records in DB, and pandas works faster in this case.


