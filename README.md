# BreedMiddleware
Is an API middleware, which gets a breed_group and returns data of a breed that has the longest life span

To get started,  make sure you've installed:

- the latest stable [Python 3.x](https://www.python.org/downloads/)

Take clone of this project.
Create and activate virtualenv and install requirments.txt as below
```shell
virtualenv <env_name>
source <env_name>/bin/activate (for Linux)
<env_name>\Scripts\activate (for windows)
cd BreedMiddleware
pip install -r requirments.txt
```

To run this project
```shell
python manage.py runserver
```

You can also give the ip and port, below is the syntax,
```shell
python manage.py runserver <ip>:<port>
```

Now the server is up and running, now you can call the api and below is the API ENDPOINT:
```shell
http://<domain>/api/longest-lifespan-breed/?breed_group=Terrier
```
this API accepts breed_group as a query parameter and returns the breed details (as per new schema requirment) with longest life span.
If any of the deatils or keys in new schma doest not exist in previous payloads then, empty string is returned for the key.

# Flow Diagram
``` 
BreedMiddleware\breed_middleware_flow_daigram.pdf 
```
is the path to flow daigarm