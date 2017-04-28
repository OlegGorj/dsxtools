
class objectStore:


    def __init__(self, credentials):

        self.credentials = credentials

    def get_api_header(self, fileName = None, verb = None, fname = None):
        '''Makes API call and returns the headers and url including token needed to work with os API'''
        import requests
        import json
        from io import BytesIO, StringIO
        credentials = self.credentials
        url1 = ''.join(['https://identity.open.softlayer.com', '/v3/auth/tokens'])
        data = {'auth': {'identity': {'methods': ['password'],
                'password': {'user': {'name': credentials['username'],'domain': {'id': credentials['domain_id']},
                'password': credentials['password']}}}}}
        headers1 = {'Content-Type': 'application/json'}
        resp1 = requests.post(url=url1, data=json.dumps(data), headers=headers1)
        resp1_body = resp1.json()
        for e1 in resp1_body['token']['catalog']:
            if(e1['type']=='object-store'):
                for e2 in e1['endpoints']:
                            if(e2['interface']=='public'and e2['region']=='dallas'):
                                if verb == 'get':
                                    url2 = ''.join([e2['url'],'/', credentials['container'], '/', fileName])
                                elif verb == 'put':
                                    url2 = ''.join([e2['url'],'/', credentials['container'], '/', fname])
                                elif verb == 'list':
                                    url2 = ''.join([e2['url'],'/', credentials['container']])
        s_subject_token = resp1.headers['x-subject-token']
        return({'X-Auth-Token': s_subject_token, 'accept': 'application/json'}, url2)


    def get_string(self, fileName, return_values = True):
        """Get's a file from the object storage container for the credentials used to create the OS object.  Returns as a ByteIO Object"""
        import requests
        from io import BytesIO, StringIO

        verb = 'get'
        header, url2 = self.get_api_header(fileName, verb)
        resp = requests.get(url= url2, headers= header)
        resp2.raise_for_status()
        if return_values:
            return StringIO(resp.text).getvalue()
        else:
            return StringIO(resp.text)

    def import_python(self, fileName, return_values= True):
        '''Use when retrieving python scripts from object storage.  This saves the file in the notebook container and can be imported as a Python Module'''
        f = open(fileName,'w')
        f.write(self.get_string(fileName))
        f.close()
        print(fileName+ " has been saved in the current directory.  You can import or move as needed.")

    def get_csv(self, fileName, return_values=True):
        """Get's a file from the object storage container for the credentials used to create the OS object.  Returns as a ByteIO Object"""
        import requests
        import pandas as pd
        from io import BytesIO, StringIO
        verb = 'get'
        header, url2 = self.get_api_header(fileName,verb)
        resp2 = requests.get(url=url2, headers=header)
        resp2.raise_for_status()
        if return_values:
            return pd.read_csv(StringIO(resp2.text))
        else:
            return StringIO(resp2.text)


    def list_files(self):
        """This functions returns a StringIO object containing
        the file content from Bluemix Object Storage V3."""
        import requests
        verb = "list"
        header, url2 = self.get_api_header(verb=verb)
        resp2 = requests.get(url=url2, headers=header)
        return [x['name'] for x in eval(resp2.content)]


    def put_csv(self, fileName, fname = None):
        """Puts a csv file in object storage with default same name as existing file. The file needs to be saved to the local file system before using this method """
        import requests
        import json
        from io import BytesIO, StringIO
        import pandas as pd
        credentials = self.credentials
        verb = 'put'
        if not fname: #handling the name of the file
            fname = fileName.split('/')[-1]

        f = open(fileName,'r')
        my_data = f.read()
        f.close()

        header, url2 = self.get_api_header(fileName,verb, fname)
        resp2 = requests.put(url=url2, headers=header, data = my_data)
        resp2.raise_for_status()
        print("{} was successfully added to the {} container. \n To view in data panel, go to main project page and add from right sidebar.".format(fname, credentials['container']))
