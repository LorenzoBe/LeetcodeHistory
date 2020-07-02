# LeetcodeHistory
This is a project to generate the users contest history of LeetCode platform.  
LeetCode doesn't allow users to visualise a meaningful history of the contests which they joined. Without this history it's difficult to keep track of the learning progresses and quickly navigate back to the difficult contests.  
The target is to acquire the data from LeetCode site and present a "nice to see" and "easy to use" graph to fill the gap.  

## Solution design
### Data size
The final design need to consider these numbers:
- Number of LeetCode users: ~110K, growing
- Number of contests: 195 weekly + 28 bi-weekly
- Number of users per contest: < 15K
- Data to be stored for each contest partecipation: contest ID (4 bytes), timestamp (4 bytes), rank (4 bytes), score (1 byte), finish time (< 2 hours, 2 bytes expressing it in seconds) -> 15 bytes

We can consider in average that each user joined 50 contests:  
key = 255B * 110K ~ 29 MB  
values = 15B * 50 * 110K ~ 83 MB  
The total is about 120 MB, not so huge.  

### Bandwidth
The backend service will be a read heavy service. The data can be updated once a week by an administration script. We can estimate a spike of 15K users in the hour just after a contest. To find the QPS:  
READ QPS = 15K / 60 minutes / 60 seconds = 4.2 QPS  

The data retrieved by each user is the complete contest history, so:  
READ BW = 4.2 QPS * 15B * 50 = 3150 B/s = 26 Kbit/sec  

### Storage
We could use an RDBMS database, maybe in master-slave configuration to improve read capabilities and availability. We don't need strict consistency between the two nodes. We could have just two tables: User and Contest. Contest could contain about 5 millions of records.  
On the other hand, we don't need to do complex queries on data, we just need the contests results of a single user to visulise them into a graph. A key-value storage with possibility of setting complex values structure (multicolumn, nested types) is probably enough.  
Since there are no additional constrains, the availability of the storage types on Cloud providers, the costs, the integration effort and the "it's cool :D" factor will be taken into consideration.  

#### Redis storage
Some preliminary tests can be executed on Redis storage. It is available on Azure and it can be easily integrate with Python scripts. This is a good starting point to learn more: https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-python-get-started  
The VisualStudioProfessional Azure subscription includes 50 CHF/months. A Redis Cache instance with 250 MB on Azure is below this cost and it should be enought for the initial tests.  
I think to start with a simple configuration where the LeetCode UserID will be the key and the single contests results will be stored into a **list** data type. More information about the Pythonic way to manage Redis lists here: https://pythontic.com/database/redis/list
Since Redis doesn't support nested types, the single contest results will be encoded in JSON format, like:
```
user:1: [{"contestId": "1", "timestamp": "1111111111", "finishTime": "666", "score": "12", "rank": "888" },
         {"contestId": "2", "timestamp": "2222222222", "finishTime": "777", "score": "23", "rank": "999"}]
```

### Application
To efficiently write data to the Redis storage, the crawler script that will get data from LeetCode need to be as near as possible to the storage.
I chose to create an Azure WebApp, written in Python 3. Inside it I can have two rest endpoints: one public to present the data and one private (password protected) to manage the updates on Redis.  
It's very easy to create a Python app on Azure, here is an example: https://docs.microsoft.com/en-us/azure/app-service/containers/quickstart-python?tabs=bash
I started from this example and extended for my purposes. The required Python package are listed in **requirements.txt** file, while the REST server is defined into **application.py** file (it uses Flask as WebService).  
It is very easy to test it on localhost using the following commands:  
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=application.py
flask run
```
The Redis storage need to be manually created using an Azure subscription.  
There are also some parameters that need to be set in a config file: Redis hostname and key, administrator user and password (will be used for the basic authentication of the private part of WebApp). I created the **config-sample.ini** file, it needs to be populated and renamed to **config.ini**.  
Once locally tested, the WebApp can be deplyed on Azure. the easiest way to start is using the [Azure Command-Line Interface](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest):
```
az login
az webapp up --sku F1 -n <app-name>
```

There is one important notice about how the Flask service is deplyed on Azure Web App. For production deployement, it's recommended to deploy Flask with just a single working thread. This means that it must serialise all requests. This is particulary bad in this project because the request which updates the storage with a new contest takes a lot of time (~1 min).  
On Azure Flask is deployed using [Gunicorn]{https://docs.gunicorn.org/en/stable/settings.html}, which should support multiple workers, but I observed that it was not possible to execute requests in parallel.  
After a lot of investigations I found that we can specify the Gunicorn starting parameters simply uploading a **startup.txt** file aside the others adn referring to it in the Azure Web App configuration, as described in [Configure a custom startup file for Python apps on Azure App Service]{https://docs.microsoft.com/en-us/azure/developer/python/tutorial-deploy-app-service-on-linux-04}.  
I logged into the Azure Portal, opened the SSH console of the Web App, found the script which is starting Gunicorn and extended the parameters with the **workers** option. This is the content of my **startup.txt** file:
```
GUNICORN_CMD_ARGS="--timeout 600 --access-logfile '-' --error-logfile '-' --bind=0.0.0.0:8000 --chdir=/home/site/wwwroot --workers=4" gunicorn application:app
```
