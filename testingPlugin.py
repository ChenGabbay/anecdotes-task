from dummy_api_plugin import DummyApiPlugin
import unittest

class Testing(unittest.TestCase):

    #check that the type of the result is list and contains objects of the same type 
    def testGetAllPostWithComment(self):
        instance = DummyApiPlugin("configurationFile.json")
        result = instance.getAllPostsWithComments()

        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(x,dict) for x in result))

    # Check that ConnectivityTEST METHOD return false because the baseUrl in testConfigFile.json is not valid
    def testConnectivityMethod(self):
        instance = DummyApiPlugin("testConfigFile.json")
        boolVal = instance.connectivity_test()
        self.assertFalse(boolVal)
  
        
if __name__ == '__main__':
    unittest.main()

