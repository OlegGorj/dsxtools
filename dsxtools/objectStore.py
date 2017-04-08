
class objectStore:


    def __init__(self, credentials):
        self.credentials = credentials


    def get_string(self, fileName, return_values = True):
        """Get's a file from the object storage container for the credentials used to create the OS object.  Returns as a ByteIO Object"""
        import requests
        import json
        from io import BytesIO
        import pandas as pd
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
                                url2 = ''.join([e2['url'],'/', credentials['container'], '/', fileName])
        s_subject_token = resp1.headers['x-subject-token']
        headers2 = {'X-Auth-Token': s_subject_token, 'accept': 'application/json'}
        resp2 = requests.get(url=url2, headers=headers2)
        if return_values:
            return StringIO(resp2.text).getvalue()
        else:
            return StringIO(resp2.text)

    def get_csv(self, fileNamex):
        """Get's a file from the object storage container for the credentials used to create the OS object.  Returns as a ByteIO Object"""
        import requests
        import json
        from io import BytesIO
        import pandas as pd
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
                                url2 = ''.join([e2['url'],'/', credentials['container'], '/', fileName])
        s_subject_token = resp1.headers['x-subject-token']
        headers2 = {'X-Auth-Token': s_subject_token, 'accept': 'application/json'}
        resp2 = requests.get(url=url2, headers=headers2)
        if return_values:
            return StringIO(resp2.text).getvalue()
        else:
            return StringIO(resp2.text)

    def put_csv(self, fileName, fname = None):
        """Puts a csv file in object storage with default same name as existing file. The file needs to be saved to the local file system before using this method """
        import requests
        import json
        from io import BytesIO
        import pandas as pd
        credentials = self.credentials

        if not fname: #handling the name of the file
            fname = fileName.split('/')[-1]

        f = open(fileName,'r')
        my_data = f.read()
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
                                url2 = ''.join([e2['url'],'/', credentials['container'], '/', fname])
        s_subject_token = resp1.headers['x-subject-token']
        headers2 = {'X-Auth-Token': s_subject_token, 'accept': 'application/json'}
        resp2 = requests.put(url=url2, headers=headers2, data = my_data )
        if str(resp2)[0] == '2': # success http response
            print("{} was successfully added to the {} container. \n Refresh the DSX notebook to see the data in the right data panel.".format(fname, credentials['container']))
        else:
            print("There was a problem with your upload!")
