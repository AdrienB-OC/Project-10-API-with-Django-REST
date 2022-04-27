"SoftDesk" 
# How to run the API in a local environment (Example of Python 3) :


Extract the repository's files in a folder of your choosing

### Setup the virtual environment :


In your command bash/shell go in the folder containing the files

Type :  
Windows :
```
py -m venv env
```
Unix/mac :
```
python3 -m venv env
```


You then need to activate the virtual environment :  
Windows :
```
.\env\Scripts\activate
```
Unix/mac :  
```
source env/bin/activate
```
(venv) should now be displayed to the left of your command line :
```
(venv) C:\>
```

### Install the libraries required to run the API :

In the virtual environment (command bash/shell) type : 
```
pip(3) install -r requirements.txt
```



You can now run the server to access the API (still in the virtual environment) :  

```
(python3) manage.py runserver

```

For instructions on how to use the API with postman refer to :
```
https://documenter.getpostman.com/view/20548393/UyrDDb42
```