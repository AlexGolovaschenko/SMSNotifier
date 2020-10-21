# -*- coding: utf-8 -*-
import json, urllib3, certifi
import logging, pprint


# ----------------------------------------------------------------------------------------
API_URL_RU = 'https://api.owencloud.ru/v1/'
API_URL_UA = 'https://cloudapi.owen.ua/v1/'


# ----------------------------------------------------------------------------------------
def printJson(js):
    '''pretty print json data'''
    pprint.pprint(js)


# ----------------------------------------------------------------------------------------
class OwenCloudConnector():
    def __init__(self, **kwargs):
        self.debug = kwargs.get('debug', False)
        self.Http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()) 
        self.token = kwargs.get('token', 'None')

        self.user_domain = kwargs.get('user_domain', 'RU')
        if self.user_domain == 'UA':
            self.API_URL = API_URL_UA
        else:
            self.API_URL = API_URL_RU

        if self.debug is True:
            logging.basicConfig()
            logging.getLogger("urllib3").setLevel(logging.DEBUG)
            requests_log = logging.getLogger("urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

      
    def login(self, user, password):
        ''' 
        logining on cloud
        you must call it first, before use other methods
        or pass the token whith __init__() 
        WARNING! some time token from owencloud received is invalide 
                ( if user dont set constant token on cloud settings 
                or if user registred on cloud.ua )
                I recomend use constant token unstead login   
        '''
        url = self._get_url('auth/open') 
        data = {'login':user, 'password':password}
        self.token = 'None'
        try:
            responce = self._request('POST', url, data=data)    
        except:
            print('ERROR: Login request error')
            return 

        try:
            self.token = responce['data']['token']
        except:
            print('ERROR: Token is not in responce')
            print(responce['data'])
            return 

        print('SUCCESS: Login succes')


    def getDevicesList(self):
        ''' 
        return list of devices for current user 
        '''
        url = self._get_url('device/index')        
        headers = self._get_autorization_header()
        responce = self._request('POST', url, headers)
        
        status = responce['status']
        if status in ('200', '201'):
            names = []
            for device in responce['data']:
                names.append( '%s: %s' %(device['name'], device['id']) )
            print('SUCCESS: Devices List received: ' + str(names))
        else:
            print('ERROR: Devices List was not received')
            printJson(responce['data'])

        return responce['data']


    def getDeviceConfiguration(self, device_id):
        ''' 
        return device data by device id
        '''
        url = self._get_url('device/' + str(device_id))
        headers = self._get_autorization_header()
        responce = self._request('POST', url, headers)
        print('SUCCESS: Device "id={}" data received'.format(device_id))        
        return responce['data']


    def getReadTagsLastData(self, tags_ids):
        ''' 
        return lasts data of tags
        tags select by id, you shold pass to the function list of ids of target tags
        '''
        url = self._get_url('parameters/last-data')
        headers = self._get_autorization_header()
        data = {"ids": tags_ids}
        responce = self._request('POST', url, headers, data=data)
        print('SUCCESS: Tags last data received')        
        return responce['data']


    def getEventsList(self):
        '''
        Получение списка событий компании - POST event/list
        return list of setted events on all objects for current user 
        '''
        # url = self._get_url('facility-event/list')   
        url = self._get_url('event/list')   
        headers = self._get_autorization_header()
        responce = self._request('POST', url, headers)
        
        status = responce['status']
        if status in ('200', '201'):
            events = []
            for event in responce['data']:
                events.append( str(event['id']) )
            print('SUCCESS: Events List received: ' + str(events))
        else:
            print('ERROR: Events List was not received. Status %s' %(status))
            printJson(responce['data'])

        return responce['data']


    def _get_url(self, path):
        return self.API_URL + path


    def _get_autorization_header(self):
        return {'Authorization': 'Bearer ' + self.token}


    def _request(self, verb, url, headers={}, **kwargs):
        ''' make request to cloud API 
        return parsed dict from response json
        '''
        data = kwargs.get('data', None)
        body = bytes()
        responce = {}
        if data is not None:
            body = json.dumps(data).encode('utf-8')
            headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        try:
            r = self.Http.request(verb, url, headers=headers, body=body)
            responce['status'] = str(r.status)
            responce['data'] = json.loads(r.data.decode('utf-8'))
        except:
            print('ERROR: Request error')
            raise

        if self.debug is True:     
            self._print_request(r)
        return responce       


    def _print_request(self, r):
        '''print request parameters'''
        print('status: ' + str(r.status))
        print('token is: ' + str(self.token))
        print('data: ')
        printJson(json.loads(r.data))
        print('\n')

