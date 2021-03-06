# gradr
Gradr is a Python/Flask web application template developed for personal and commercial projects.

Grades are the number one thing on the minds of any student. The current means of tracking academic standing are often 
outdated, confusing, and difficult to use. Enter Gradr, a modern and fully responsive web-based grade tracking 
application. Gradr will allow users to sign up using their Husky emails, enter their grades, and track their progress 
across any device. We’ll also (time permitting) display deep analytics based on aggregated and anonymized user data to 
allow students to see how they’re stacking up to their peers.
 
### Starting the Web Server:
Dependencies: `Python 3.5.1` or higher
1) Ensure mongodb is running by typing `mongo` and catching the shell
2) Run `pip install -r requirements.txt`
3) Run `python runserver.py`
4) username: `admin` | password: `password ` (these are dummy values for easy testing/demo purposes)
4) Begin by entering assignment categories and corresponding assignments the necessary databases and collections
will be generated on the fly.
5) Visit the 'View Databases' tab to view/update the database in table form
6) Visit Stats tab to see means for each category and final weighted average if applicable

## User features:
* Sign-up via OAUTH (disabled for demo / debugging)
* Add/remove classes and assignment percentage breakdown
* Add/remove assignments and grades
* Add major and year of graduation (not currently available)


## UI features:
* fully responsive and mobile-friendly (device agnostic)
* clean modern design language (fast!)

## Future features:
* peer comparison (the chart is implemented with canned data)
* auto-import from Bottlenose (CCIS grading system)
* deep analytics

## Technologies used:
* `Python 3` installed via Anaconda http://www.continuum.io/downloads
* `Pandas / Numpy` for statistical analysis
* `Flask / Jinja` http://flask.pocoo.org
* `Twitter Bootstrap` http://getbootstrap.com
* `Highcharts` http://www.highcharts.com/download
* `MongoDB` http://www.mongodb.org
* `DigitalOcean` https://www.digitalocean.com

## References:
* Flask for Larger Applications http://flask.pocoo.org/docs/0.12/patterns/packages/
* Modular Applications with Blueprints http://flask.pocoo.org/docs/0.12/blueprints/#blueprints
* Bootstrap Components Reference http://getbootstrap.com/components/
