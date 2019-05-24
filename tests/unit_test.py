import unittest

from src import retrieve


class TestRetrieve(unittest.TestCase):
    def test_data(self):
        data = retrieve.hardware_json()
        response = retrieve.post_data(data)
        self.assertEqual(response.status_code, 201)
        test_compare_request_response(data, response.json())


def test_compare_request_response(expected, actual):
    if type(expected) is dict:
        for key in expected.keys():
            test_compare_request_response(expected[key], actual[key])
    elif type(expected) is list:
        for i in range(len(expected)):
            test_compare_request_response(expected[i], actual[i])
    else:
        assert expected == actual, f"expected: {expected} -- actual: {actual}"


if __name__ == '__main__':
    unittest.main()
