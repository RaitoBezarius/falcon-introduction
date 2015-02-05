import falcon
import json

class MockupDB(object):
    
    def __init__(self):
        self.store = {'pythonparis': 'Paris.py 6', 'c++paris': 'Paris.cpp 1'}
    
    def get(self, language, country):
        if not self.exists(language, country):
            return None
        return {'name': self.store[language.lower() + country.lower()]}
    
    def delete(self, language, country):
        if self.exists(language, country):
            del self.store[language.lower() + country.lower()]
    
    def post(self, language, country, name):
        self.store[language.lower() + country.lower()] = name
    
    def exists(self, language, country):
        return (language.lower() + country.lower()) in self.store

class MeetupResource(object):
    
    def __init__(self, meetup_db):
        self._db = meetup_db
    
    def on_get(self, request, response, language, country):
        meetups = self._db.get(language, country)
        if meetups is None:
            raise falcon.exceptions.HTTPNotFound()
        response.content_type = 'application/json'
        response.body = json.dumps(meetups)
    
    def on_delete(self, request, response, language, country):
        self._db.delete(language, country)
        response.status = falcon.HTTP_204
    
    def on_post(self, request, response, language, country):
        self._db.post(language, country, request.get_param('name'))
        response.status = falcon.HTTP_200
    
    def on_put(self, request, response, language, country):
        if not self._db.exists(language, country):
            raise falcon.exceptions.HTTPNotFound()
        if not (language.lower() == 'python'):
            response.status = falcon.HTTP_799


api = falcon.API()

db = MockupDB()
api.add_route('/meetups/{language}/{country}', MeetupResource(db))