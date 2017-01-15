# Temperature & Humidity REST API
REST API to be used in cojunction with the temp_hum-uploader I've written for 
my Beaglebone Black (BBB).
It is based on [Flask](http://flask.pocoo.org/),
[Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.5/) and
[Flask-MySQL](https://flask-mysql.readthedocs.io/en/latest/)

There also is a webinterface that show a graph for temperature and humidity, 
based on [MetricsGraphics.js](http://metricsgraphicsjs.org/).

## Usage
Setup the application in a virtualenv, using pip
```
virtualenv env  
pip install -r requirements.txt
```

Set the Flask configruation & Start the application
```
export FLASK_CONFIGURATION=testing  
python api.py
```

Now you can access the application at http://127.0.0.1:5000/

## FAQ
* Can I use an external database?
> It's possible to configure all database settings (Host, Port, Username, 
Password, Database), in either the config.py or the config.cfg.  
> I recommend to use the config.cfg since it's excluded using .gitignore  
* What endpoints exist?
> At /temp-hum-list/ you can get a list of all data recorded.  
> At /temp-hum/<record_id> you can get a single record, or update it (not 
recommended)  
> Currently POST is also done to /temp-hum-list/ but I need to change that, 
since it's just wrong...
