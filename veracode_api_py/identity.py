#identity.py - API classes for Identity API calls

import json
import logging
from urllib import parse

from .apihelper import APIHelper

logger = logging.getLogger(__name__)

class Users():
   def get_all(self):
      #Gets a list of users using the Veracode Identity API        
      request_params = {'page': 0} #initialize the page request
      return APIHelper()._rest_paged_request("api/authn/v2/users","GET","users",request_params)

   def get_self (self):
      #Gets the user info for the current user, using the Veracode Identity API
      return APIHelper()._rest_request("api/authn/v2/users/self","GET")

   def get(self,user_guid):
      #Gets an individual user provided their GUID, using the Veracode Identity API
      uri = "api/authn/v2/users/{}".format(user_guid)
      return APIHelper()._rest_request(uri,"GET")

   def get_by_name(self,username):
      #Gets all the users who match the provided email address, using the Veracode Identity API
      request_params = {'user_name': parse.quote(username)} #initialize the page request
      return APIHelper()._rest_paged_request("api/authn/v2/users","GET","users",request_params)

   def get_user_search(self,search_term=None, api_id=None, role_id=None, login_status=None, saml_user=None, team_id=None, detailed=False):
      request_params = {'detailed': detailed}
      
      if search_term != None:
         request_params['search_term'] = parse.quote(search_term)

      if api_id != None:
         request_params['api_id'] = api_id

      if role_id != None:
         request_params['role_id'] = role_id
      
      if login_status != None:
         request_params['login_status'] = login_status

      if saml_user != None:
         request_params['saml_user'] = saml_user

      if team_id != None:
         request_params['team_id'] = team_id

      return APIHelper()._rest_paged_request("api/authn/v2/users/search","GET","users",request_params)

   def create(self,email,firstname,lastname,username=None,type="HUMAN",roles=[],teams=[]):
      user_def = { "email_address": email, "first_name": firstname, "last_name": lastname }

      rolelist = []
      if len(roles) > 0:
         for role in roles:
               rolelist.append({"role_name": role})
         user_def.update({"roles":rolelist})

      if type == "API":
         user_def.update({"user_name": username})
         user_def.update({"permissions": [{"permission_name": "apiUser"}]})
         if len(roles) == 0:
            rolelist.append({"role_name": "uploadapi"})
            rolelist.append({"role_name":"apisubmitanyscan"})
      else:
         if len(roles) == 0:
            rolelist.append({"role_name":"submitter"}) 

      if username is not None:
         user_def.update({"user_name": username})
      else:
         user_def.update({"user_name": email})

      teamlist = []
      if len(teams) > 0:
         for team in teams:
               teamlist.append({"team_id": team})
         user_def.update({"teams": teamlist})

      user_def.update({"roles": rolelist})

      payload = json.dumps(user_def)
      return APIHelper()._rest_request('api/authn/v2/users','POST',body=payload)

   def update_roles(self,user_guid,roles):
      request_params = {'partial': 'TRUE',"incremental": 'TRUE'}
      uri = "api/authn/v2/users/{}".format(user_guid)

      rolelist = []
      for role in roles:
            rolelist.append({"role_name": role})

      payload = json.dumps({"roles": rolelist})
      return APIHelper()._rest_request(uri,"PUT",request_params,body=payload)

   def update(self,user_guid,changes):
      request_params = {'partial':'TRUE',"incremental": 'TRUE'}
      uri = "api/authn/v2/users/{}".format(user_guid)
      payload = json.dumps(changes)
      return APIHelper()._rest_request(uri,"PUT",request_params,body=payload)

   def disable(self,user_guid):
      request_params = {'partial':'TRUE'}
      uri = 'api/authn/v2/users/{}'.format(user_guid)
      payload = json.dumps({'active': False})
      return APIHelper()._rest_request(uri,"PUT",request_params,payload)

   def delete(self,user_guid):
      uri = 'api/authn/v2/users/{}'.format(user_guid)
      return APIHelper()._rest_request(uri,"DELETE")

class Teams():
   def get_all(self, all_for_org=False):
      #Gets a list of teams using the Veracode Identity API       
      if all_for_org:
         request_params = {'all_for_org': True}
      else:
         request_params = {'page': 0} #initialize the page request
      return APIHelper()._rest_paged_request("api/authn/v2/teams","GET","teams",request_params)

   def create(self, team_name, business_unit=None, members=[]):        
      team_def = {'team_name': team_name}
      
      if len(members) > 0:
         # optionally pass a list of usernames to add as team members
         users = []
         for member in members:
               users.append({'user_name': member})
         team_def.update({'users': users})

      if business_unit != None:
         bu = {'bu_id': business_unit}
         team_def.update(bu)

      payload = json.dumps(team_def)
      return APIHelper()._rest_request('api/authn/v2/teams','POST',body=payload)

   def update(self, team_guid, team_name="", business_unit=None, members=[]):
      requestbody = {}
      
      if team_name != "":
         requestbody.update({"team_name": team_name})

      if business_unit != None:
         requestbody.update({"business_unit": {"bu_id": business_unit}})

      if len(members) > 0:
         users = []
         for member in members:
               users.append({"user_name": member})
         requestbody.update({"users": users})

      if requestbody == {}:
         logging.error("No update specified for team {}".format(team_guid))

      payload = json.dumps(requestbody)
      params = {"partial":True, "incremental":True}
      uri = 'api/authn/v2/teams/{}'.format(team_guid)
      return APIHelper()._rest_request(uri,'PUT',body=payload,params=params)

   def delete(self, team_guid):
      uri = 'api/authn/v2/teams/{}'.format(team_guid)
      return APIHelper()._rest_request(uri,"DELETE")

class BusinessUnits():
   base_uri = "api/authn/v2/business_units"

   def get_all(self):
      request_params = {'page': 0}
      return APIHelper()._rest_paged_request(self.base_uri,"GET","business_units",request_params)

   def get(self,guid):
      return APIHelper()._rest_request(self.base_uri + "/{}".format(guid),"GET")

   def create(self,name,teams=[]):
      payload = {"bu_name":name}

      if len(teams)>0:
         team_list = []
         for team in teams:
            team_list.append({"team_id": team})
         payload["teams"] = team_list

      return APIHelper()._rest_request(self.base_uri,"POST",body=json.dumps(payload))

   def update(self,guid,name="",teams=[]):
      payload = {}

      if name != "":
         payload["bu_name"] = name
      
      if len(teams)>0:
         team_list = []
         for team in teams:
            team_list.append({"team_id": team})
         payload["teams"] = team_list

      return APIHelper()._rest_request(self.base_uri + "/{}".format(guid),"PUT",body=json.dumps(payload),params={"partial":True, "incremental":True})

   def delete(self,guid):
      return APIHelper()._rest_request(self.base_uri + "/{}".format(guid),"DELETE")

class APICredentials():
   base_uri = "api/authn/v2/api_credentials"
   def get_self (self):
      return APIHelper()._rest_request(self.base_uri,"GET")

   def get (self, api_id):
      return APIHelper()._rest_request(self.base_uri + '/{}'.format(api_id),"GET")

   def renew (self):
      return APIHelper()._rest_request(self.base_uri,"POST",body=json.dumps({}))

   def revoke (self, api_id):
      return APIHelper()._rest_request(self.base_uri + '/{}'.format(api_id), "DELETE")

class Roles():
   def get_all(self):
      return APIHelper()._rest_paged_request("api/authn/v2/roles","GET","roles",{'page':0})