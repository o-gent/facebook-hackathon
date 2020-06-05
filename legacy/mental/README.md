# Mental

The mental module is the flask app for serving the messenger bot.

## mental __init__.py

create_app() returns the flask app instance

The views are registered to the app here using app.add_url_rule(), this may make more sense than using decorators..

## views

Any function that returns a web response should be stored within views. 
