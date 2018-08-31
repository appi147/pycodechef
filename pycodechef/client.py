"""
This is python wrapper for Codechef API v1.0.0
"""
import requests


class Codechef(object):
    '''
    Main class
    '''

    __attrs__ = ['client_id', 'client_secret', 'access_token']

    def __init__(self, client_id, client_secret):
        '''
        :param client_id: client_id is the string obtained from Codechef for the application
        :param client_secret: client_secret is the string obtained from Codechef for the application
        '''
        self.client_id = client_id
        self.client_secret = client_secret
        headers = {
            'content-Type': 'application/json',
        }

        data = '{{"grant_type":"client_credentials" , "scope":"public", "client_id":"{}","client_secret":"{}"}}'.format(client_id, client_secret)

        response = requests.post('https://api.codechef.com/oauth/token', headers=headers, data=data)
        response = response.json()

        if response['status'] == "OK":
            print('Fetching access token...')
            self.access_token = response['result']['data']['access_token']
        else:
            print('Error', response)

    def _refresh(self):
        '''
        refreshes access_token
        currently not tested if it works
        '''
        headers = {
            'content-Type': 'application/json',
        }
        data = '{{"grant_type":"refresh_token" , "refresh_token":"{}", "client_id":"{}","client_secret":"{}"}}'.format(self.access_token, self.client_id, self.client_secret)
        response = requests.post('https://api.codechef.com/oauth/token', headers=headers, data=data)

    def _GET(self, url, params=None):
        '''
        fetch from api
        :param url: String. endpoint to fetch
        :param params: query parameters given
        '''
        token = "Bearer {}".format(self.access_token)
        headers = {
            'Accept': 'application/json',
            'Authorization': token,
        }
        if params:
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.get(url, headers=headers)

        if response.status_code != 200:
            error = 'HTTPError: {}'.format(response.status_code)
            return {'success': False, 'error': error}
        try:
            return response.json()
        except ValueError as err:
            return {'success': False, 'error': err}

    def get_contest_problem(self, contest_code, problem_code):
        '''
        get information about a problem of a contest
        :param contest_code: String. Contest code of the problem.
        :param problem_code: String. Problem code of the problem
        '''
        path = 'https://api.codechef.com/contests/' + contest_code + '/problems/' + problem_code
        response = self._GET(path)

        return response

    def get_contest_details(self, contest_code, fields=[], sortBy='successfulSubmissions', sortOrder='desc'):
        '''
        get information about a contest
        :param contest_code: String. contest code. Only provide this parameter for full details
        :param fields: List. Possible fields are: code, name, startDate, endDate, type, bannerFile, freezingTime, announcements, problemsList. Multiple fields can be entered using comma.
        :param sortBy: String. Possible fields are: problemName, problemCode, successfulSubmissions, accuracy.
        :param sortOrder: String. Possible fields are: asc or desc.
        '''
        url = 'https://api.codechef.com/contests/' + contest_code
        params = (
            ('fields', ','.join(fields)),
            ('sortBy', sortBy),
            ('sortOrder', sortOrder),
        )
        response = self._GET(url, params)

        return response
