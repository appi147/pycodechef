"""
This is python wrapper for Codechef API
"""
import json
import requests


class Codechef(object):
	"""A codechef api wrapper"""
	
	__attrs__ = ['client_id', 'client_secret', 'access_token']

	def __init__(self, id, secret):
		self.client_id = id
		self.client_secret = secret
		headers = {
		    'content-Type': 'application/json',
		}

		data = '{{"grant_type":"client_credentials" , "scope":"public", "client_id":"{}","client_secret":"{}"}}'.format(id, secret)

		response = 
		response = response.json()

		if response['status'] == "OK":
			print('Fetching access token...')
			self.access_token = response['result']['data']['access_token']
		else:
			print('Error', response)

	def _refresh(self):
		headers = {
		    'content-Type': 'application/json',
		}
		data = '{{"grant_type":"refresh_token" , "refresh_token":"{}", "client_id":"{}","client_secret":"{}"}}'.format(self.access_token, self.client_id, self.client_secret)
		response = requests.post('https://api.codechef.com/oauth/token', headers=headers, data=data)
		print('Token successfully refreshed!!')

	def _GET(self, url):
		token = "Bearer {}".format(self.access_token)
		headers = {
		    'Accept': 'application/json',
	    	'Authorization': token,
		}
		response = requests.get(url, headers=headers)

		if response.status_code != 200:
			error = 'HTTPError: {}'.format(response.status_code)
			return {'success': False, 'error': error}
		try:
			return response.json()
		except ValueError as err:
			return {'success': False, 'error': err}


	def get_contest_problem(self, contest_code, problem_code):

		url = 'https://api.codechef.com/contests/'
		path = url + contest_code + '/problems/' + problem_code
		response = self._GET(path)

		return response

