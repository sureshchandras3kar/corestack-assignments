# importing package UnitTest and json


import unittest
import json


# creating class APITest

class APITest(unittest.TestCase):
    import flask_main

    def setUp(self):
        self.flask_main.app.testing = True

        self.client = self.flask_main.app.test_client()
        # declare json content-type
        self.header = {
            'Content-Type': 'application/json'
        }
        # declare variable testdata  to be passed as value in unittest
        self.testdata = {"name": "Test",
                         "age": 21}

        # declare variable putdata as update value
        self.putdata = {"$set": {
            "age": 20
        }}
        # converting update value to json format store in variable jsndata
        self.jsndata = json.dumps(self.putdata)

        # converting  to json format
        self.jdata = json.dumps(self.testdata)

        # print type(self.jdata)

    def test_postquery(self):
        # post method
        res = self.client.post('/postdata', headers=self.header, data=self.jdata)

        #  res.status_code
        self.assertEqual(200, res.status_code)

    def test_getquery(self):
        # get method
        res = self.client.get('/getdata', headers=self.header, data=self.jdata)

        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        strdata = json.dumps(result_in_json)

        print type(strdata)
        dictdata = json.loads(strdata)

        #  get data test_case
        #self.assertEqual(dictdata["name"], self.testdata["name"])
        #   status code test_case
        self.assertEqual(200, res.status_code)

    def test_putquery(self):
        # declare variable path get value to be updated

        path = "http://127.0.0.1:5000/putdata?search_query=%s" % self.jdata
        # put method

        res = self.client.put(path, headers=self.header, data=self.jsndata)
        # test case

        self.assertEqual(200, res.status_code)
        self.assertEqual("data updated.........///", res.data)

    def test_deletequery(self):
        # delete method
        res = self.client.delete('/deletedata', headers=self.header, data=self.jdata)
        # test case
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
