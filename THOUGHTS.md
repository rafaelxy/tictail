- Unicode API: jsonify doesnt support unicode properly - used json.dumps instead

- Unicode API: native csvreader from python does not support unicode, added new library to requirement.txt (unicodecsv==0.13.0)

- CORS: Of course in a production setting I would limit the hosts instead of having "*", however I had ports 5000 and 8000 already being used in my machine so I used "*", so would work here and there for you. :)

- Tried to make CSV access similar to a callback-filtering API that could be reused.

- Radius vs distance using Haversine formula - Loved working with a little bit of GIS again :)

- Sorry about not writing any tests; Had a clutch time/week to implement this.