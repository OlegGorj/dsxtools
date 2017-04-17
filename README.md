# dsxtools
Tools built to help work with Python notebooks in Data Science Experience

### Installation

In a Python 3 DSX notebook:

`!pip install git+https://github.com/gfilla/dsxtools.git`

*Hope to support Python 2 and get into Pypi in the future!*

### Basic Usage

Inside a DSX Notebook, insert your credentials to the notebook using insert to code.  The variable name for the credentials will be used for the methods in this package.

```
creds = {
 'auth_url':'https://identity.open.softlayer.com',
 'project':
 'project_id':
 'region':'dallas',
 'user_id':
 'domain_id':
 'domain_name':
 'username':
 'password':
 'container':
 'tenantId':'undefined',
 'filename':
}
```

### Using Object Storage with dsxtools

#### Getting Data

```
from dsxtools import objectStore

my_os = objectStore(creds)
df = my_os.get_csv(NAME OF FILE IN YOUR CONTAINER)
```

That is how you get a CSV file. The file is returned as a Pandas dataframe. If you are reading in a text file or just want a 
string of the file contents, use `get_string()` instead of `get_csv`

#### Putting Data in Object Store

```
my_os.put_csv(fileName= path+fname, fname= 'testing.csv')
```

Accepts a fileName which is the location of the CSV file stored locally.  In DSX, you accomplish this by using something like `to_csv()` from Pandas on a dataframe.  `fname` in this function is the desired name of the file when it is put in the Object Storage container.

#### Listing Files in the Container

This is a helpful function when working with repositories of data or many CSVs that you need to iterate through for processing.  Returns a list of files in the container that was specified when the credentials were passed to create an instance of the `objectStore` class.

```
my_os.list_files()
```


#### Using Python modules stored in Object Storage

A typical workflow in DSX is to build a large module as a Python script and `import` it for use in a notebok.  To help with this, use `import_python` for Python scripts in your Object Storage container. This function saves the Python script in the working directory so you can import it in your notebook.  Prints a confirmation that the module was saved in the notebook environment.  Usage:

```
my_os.import_python(fileName = 'myModule.py')
```
