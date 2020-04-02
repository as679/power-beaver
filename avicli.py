#!/usr/bin/env python3
import argparse
import yaml
import json
import logging
import requests
​
import urllib3
urllib3.disable_warnings()
​
​
class AviSession(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._load_auth()
        self._build_session()
        self._setup()
        self._parse_params()
        self._parse_cmd()
​
    def _load_auth(self):
        with open(self.auth_file) as fh:
            yml = yaml.load(fh, Loader=yaml.FullLoader)
            self._auth = yml['controllers'][self.controller]['auth']
​
    def _build_session(self):
        auth = {'username': self._auth['username'], 'password': self._auth['password']}
        login = 'https://%s/login' % self._auth['cluster_ip']
​
        self._api = requests.session()
        self._api.verify = False
        r = self._api.post(login, json=auth)
        r.raise_for_status()
        self._login = r
​
    def _setup(self):
        prefix = 'https://%s/' % self._auth['cluster_ip']
        self._prefix = prefix + 'api/'
        hdr = {'X-Avi-Version': self._login.json()['version']['Version']}
        hdr['X-CSRFToken'] = self._login.cookies['csrftoken']
        hdr['Referer'] = prefix
        hdr['X-Avi-Tenant'] = self._auth['tenant_name']
        if self.tenant is not None:
            hdr['X-Avi-Tenant'] = self.tenant
        self.headers = hdr
​
    def _parse_params(self):
        params = {'include_name': 'true'}
        if self.param is not None:
            for p in self.param:
                k, v = p.split('=', 1)
                params[k] = v
        self.params = params
​
    def _parse_cmd(self):
        path = self._cmd.pop(0)
        getattr(self, self._cmd.pop(0))(path)
​
    def list(self, path):
        results = []
        response = self._api.get(self._prefix + path, headers=self.headers, params=self.params)
        response.raise_for_status()
        for i in response.json()['results']:
            results.append(i)
        while 'next' in response.json():
            response = self._api.get(response.json()['next'])
            response.raise_for_status()
            for i in response.json()['results']:
                results.append(i)
        print(json.dumps(results))
​
    def show(self, path):
        params = self.params
        params['name'] = self._cmd.pop(0)
        response = self._api.get(self._prefix + path, headers=self.headers, params=self.params)
        response.raise_for_status()
        print(json.dumps(response.json()['results']))
​
​
parser = argparse.ArgumentParser()
parser.add_argument('--controller', required=True)
parser.add_argument('--auth_file', default='avi.yml')
parser.add_argument('--tenant')
parser.add_argument('--param', action='append')
parser.add_argument('--debug', action='store_true')
parser.add_argument('_cmd', nargs=argparse.REMAINDER)
args = parser.parse_args()
​
if args.debug:
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1
​
session = AviSession(**args.__dict__)