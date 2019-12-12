## Overview

This project aims to identify the most important topics of a given time period by analyzing data pulled from the New York Times Archive [API](https://developer.nytimes.com/docs/archive-product/1/overview).

## Getting started

* In order to run the app, install all the requirements stated in requirements.txt and run `python3 app.py` in the main directory.
* To run tests, use `python3 db_tests.py`.
* To delete all the data from the database, run `python3 clear_data.py`.


## Notes on possible deployment

This is a developement (or more like a prototype) version of a project, **not** suitable for a production deployment. This is not a comprehensive list of changes that would need to be changed if one considered actually deploying this app:

* Do not use Flask development server
* Store the API key, and the MongoDB credentials in the envinromental variables
* This project uses the MongoDB hosted by mlab.com, and the (free) storage limit is only 515mb. This is not enough for a good performance because that data from one API call might be as large as 20mb.


## Known bugs

* If the dabatase is full, the app will malfunction and the user will not be informed about the reason of this behaviour. This would not be a real problem without this 512MB limit, because the entire amount of the data offered in the archive API is of order 25GB, which is not a lot.