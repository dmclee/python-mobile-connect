import json
import commands
import rauth
import requests
import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django.conf import settings

client_id = settings.MOBILE_CONNECT['client_id']
client_secret = settings.MOBILE_CONNECT['client_secret']
redirect_uri = settings.MOBILE_CONNECT['redirect_uri']
authorize_base_url = settings.MOBILE_CONNECT['authorize_base_url']
api_base_url = settings.MOBILE_CONNECT['api_base_url']
access_token_url = settings.MOBILE_CONNECT['access_token_url']
scope = settings.MOBILE_CONNECT['scope']

service = rauth.OAuth2Service(client_id = client_id,
    client_secret = client_secret,
    access_token_url = access_token_url,
    authorize_url = authorize_base_url,
    base_url = authorize_base_url)

class Index(TemplateView):
    template_name = 'mobile_connect.html'

    def get(self, *args, **kwargs):
        return render_to_response(self.template_name)

class GetProfilePage(TemplateView):
    template_name = 'get_profile.html'

    def get(self, request, *args, **kwargs):
        requester = requests.post
        get_requester = requests.get
        code = request.GET['code']
        params = {'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri}
        
        profile_uri = api_base_url + "/profile/me"

        json_decoder = json.loads
        session = service.get_auth_session(
            decoder=json_decoder, 
            data=params, 
            auth=(client_id, client_secret), 
            verify=False)
        print session
        response = session.get(profile_uri, verify=False)
        profile_details = response.json()
        msisdn_details = profile_details['msisdn']
        email_details = profile_details['email']

        return render_to_response(self.template_name, {'msisdn_details': msisdn_details, 'email_details': email_details})

def send_request(request):
    state = uuid.uuid4().hex
    requester = requests.get
    params = {'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': state,
        'scope': scope,
        'acr_values': '2',
        'prompt': ''}
    url = service.get_authorize_url(**params)
    return HttpResponseRedirect(url)