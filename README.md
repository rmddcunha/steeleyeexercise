# SteelEyeExercise

Prepare a data set using the foll. 2 files

http://api.nobelprize.org/v1/laureate.json
http://api.nobelprize.org/v1/country.json

The first file contains information about Nobel prize winners, while the second file is a lookup file for the country.
Read the files, inspect them, and then perform the following tasks.

Note: In file 1, the 'prizes' field contains info about individual prizes

Write an output CSV file containing the foll columns:

1. id
2. name (firstname + ' ' + surname). If it is an org, firstname is the org name and surname is null (field doesn't exist in the json). Handle this case.
3. dob (from field 'born')
4. unique_prize_years (concat all unique years in the 'prizes' field using ;)
5. unique_prize_categories (concat all unique categories in the 'prizes' field using ;)
6. gender
7. Use the bornCountryCode field to do a lookup on another file http://api.nobelprize.org/v1/country.json. Read this file in the same way as file 1 and do a lookup based on country code and get the country name. Note: the root element is called 'countries' If there are multiple countries with the same symbol, just take any of them.

Notes:
Remember to handle nulls for all fields in a suitable way.
Use any libraries you like. But make sure the code is modularised, uses suitable logging, exception handling, coding style, formatting, docstrings, comments. Imagine that you're writing code that will go to production.
