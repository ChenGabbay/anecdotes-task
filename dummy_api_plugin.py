import json
import requests
from plugin import Plugin

class DummyApiPlugin(Plugin):
    
    # initialize the properties with the values from the configuration file, if the configuration file is invalid,
    # the properties are initialized with default values 
    def __init__(self, configFilePath):
        configFile =self.loadConfigFile(configFilePath)
        self.baseUrl = configFile.get('baseUrl',"https://dummyapi.io/data/v1")
        self.headers = configFile.get('headers',{"app-id": "6425d8adaffcb4c2cef187e3"})
        self.limitUsers = configFile.get('limitUsers', 20)
        self.limitPosts = configFile.get('limitPosts', 50)
        self.endpointUser = configFile.get('endpointUser', '/user')
        self.endpointPost = configFile.get('endpointPost', '/post')
        self.endpointComment = configFile.get('endpointComment','/comment')

    # Check that a connection to the user endpoint is successfully established,
    # and that some user data is retrieved from the connection.
    # return true and print some user data , or return false
    def connectivity_test(self):
        try:
            response = requests.get(self.baseUrl+self.endpointUser, headers=self.headers)
            if response.status_code == 200:
                allUsers = response.json()['data']
                if allUsers:
                    idUser = allUsers[0]['id']
                    responseUser = requests.get(self.baseUrl+self.endpointUser+f"/{idUser}" , headers=self.headers)
                    responseUser.raise_for_status()
                    if responseUser.json():
                        print(f"Connection succeeded and user data retrieved successfully.Example user data: {responseUser.json()}")
                        return True
                    else:
                        print("no user data was returned in Api response")
                        return False
                else:
                    print("no user data was returned in Api response")
                    return False
            else:
                print("connection failed")
                return False
        except Exception as er:
            print("Exception accur:",er)
            return False

    # collect a list of all the users in the system using paginating mechanism and return the list
    def collectAllUsers(self):
        usersList = []
        page = 1
        fetchUsersData = True

        while fetchUsersData:
            params = {'page': page, 'limit': self.limitUsers}
    
            try:
                response = requests.get(self.baseUrl + self.endpointUser , headers=self.headers, params=params)
                response.raise_for_status()
                usersData = response.json()
                if len(usersData['data']) == 0:
                    break

                usersList.extend(usersData['data'])   
                page+=1
            except requests.exceptions.RequestException as exception:
                print(f"error in fetching the data:{exception}")
                break

        return usersList

    # fetching 50 posts ,add to each post the comments on the post and return the them in a list
    def getAllPostsWithComments(self):
        postList=[]
        postParams = {'limit':self.limitPosts}

        try:
            response = requests.get(self.baseUrl + self.endpointPost, headers=self.headers, params=postParams)
            response.raise_for_status()
            allPosts = response.json()['data']
            
            for post in allPosts:
                postId = post['id']
                postDetails = requests.get(self.baseUrl + self.endpointPost+ f"/{postId}",headers=self.headers).json()
                commentsOnPost = requests.get(self.baseUrl + self.endpointPost+ f"/{postId}"+self.endpointComment, headers=self.headers).json()['data']
                postDetails['comments'] = commentsOnPost
                postList.append(postDetails)

        except requests.exceptions.RequestException as exception:
            print(f"error:{exception}")
            return None

        return postList

    # save data in json file
    def SaveDataToFile(self,data,fileName):
        try:
            with open(fileName,'w') as file:
                json.dump(data,file)
                print(f"The file {fileName} was successfully created and updated")
        except Exception as exception:
            print(f"Failed to save data to file {fileName} due to an error: {exception}")

    # load configFilePath
    def loadConfigFile(self,configFilePath):
        try:
            with open(configFilePath,'r') as file:
                configFile = json.load(file)   
                return configFile
        except:
            print("Error in loading configuration file. Set to use default values")
            return {}
        
    #create evidences and 2 json file for each evidence  
    def collect(self):
            user = self.collectAllUsers()
            self.SaveDataToFile(user,'user.json')
            posts = self.getAllPostsWithComments()
            self.SaveDataToFile(posts,'posts.json')