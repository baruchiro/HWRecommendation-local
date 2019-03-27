import unittest

from src import retrieve


class TestRetrieve(unittest.TestCase):
    def test_data(self):
        data = retrieve.hardware_json()
        response = retrieve.postData(data)
        self.assertEqual(response.status_code, 201)
        test_CompareRequestResponse(data, response.json())


def test_CompareRequestResponse(expected, actual):
    if type(expected) is dict:
        for key in expected.keys():
            test_CompareRequestResponse(expected[key], actual[key])
    elif type(expected) is list:
        for i in range(len(expected)):
            test_CompareRequestResponse(expected[i], actual[i])
    else:
        assert expected == actual, f"expected: {expected} -- actual: {actual}"


if __name__ == '__main__':
    unittest.main()
