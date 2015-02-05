import meetup
import falcon.testing
import unittest

class MeetupTests(unittest.TestCase):
    
    def setUp(self):
        self.app = meetup.api
        self.mock = falcon.testing.StartResponseMock()
        self.paris_py_path = '/meetups/python/paris'
        self.paris_cpp_path = '/meetups/c++/paris'
        self.simulate_request(self.paris_py_path,
        method='POST', body='name=Paris.py 6')
        self.simulate_request(self.paris_cpp_path,
        method='POST', body='name=Paris.cpp 1')
    
    def simulate_request(self, path, **kwargs):
        env = falcon.testing.create_environ(
            path=path, **kwargs)
        return self.app(env, self.mock)
    
    def test_meetup_existence(self):
        self.simulate_request(self.paris_py_path,
        method='GET')
        self.assertEqual(self.mock.status, falcon.HTTP_200)
    
    def test_meetup_inexistence(self):
        self.simulate_request('/meetups/php/paris',
        method='GET')
        self.assertEqual(self.mock.status, falcon.HTTP_404)
    
    def test_meetup_delete(self):
        self.simulate_request(self.paris_cpp_path,
        method='DELETE')
        self.assertEqual(self.mock.status, falcon.HTTP_204)
    
    def test_method_not_allowed(self):
        self.simulate_request(self.paris_py_path,
        method='PATCH')
        self.assertEqual(self.mock.status, falcon.HTTP_405)
    
    def tearDown(self):
        self.simulate_request(self.paris_py_path,
        method='DELETE')
        self.simulate_request(self.paris_cpp_path,
        method='DELETE')
    