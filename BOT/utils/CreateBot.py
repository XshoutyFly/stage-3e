from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.utils import generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData

class Application(SparkData):

    def __init__(self, json):
        super(Application, self).__init__(json)

    @property
    def id(self):
        return self._json['id']

    @property
    def logo(self):
        return self._json['logo']

    @property
    def botEmail(self):
        return self._json['botEmail']

    @property
    def name(self):
        return self._json['name']

    @property
    def botToken(self):
        return self._json['botToken']

    @property
    def type(self):
        return self._json['type']


class ApplicationAPI(object):
    def __init__(self,session):
        assert isinstance(session, RestSession)
        super(ApplicationAPI, self).__init__()
        self._session = session

    def create(self,name,botEmail,type,logo):
        post_data={}
        post_data['name']=name
        post_data['botEmail']=botEmail
        post_data['type']=type
        post_data['logo']=logo
        json_obj = self._session.post('applications', json=post_data)
        return Application(json_obj)

    @generator_container
    def list(self,createdBy="me",type="bot"):

        params={"createdBy": createdBy, "type":type}
        json_obj = self._session.get_items('applications',params=params)
        for item in json_obj:
            yield Application(item)

    def get(self,id):
        json_obj = self._session.get('applications/' + id)
        return Application(json_obj)

    def delete(self,id):
        self._session.delete('applications/' + id)