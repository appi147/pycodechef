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

    def get_contest_list(self, fields=[], status='', offset=0, limit=10, sortBy='startDate', sortOrder='desc'):
        '''
        get list of contests
        :param fields: List. Possible fields are: code, name, startDate, endDate. Multiple fields can be entered using comma.
        :param status: String. Possible values: past, present, future
        :param offset: Integer. Starting index of the list eg.4
        :param limit: Integer. Number of contests in a list(max 100), e.g. 10
        :param sortBy: String. Possible fields are: name, startDate, endDate.
        :param sortOrder: String. Possible fields are: asc, desc
        '''
        url = 'https://api.codechef.com/contests/'
        params = (
            ('fields', ','.join(fields)),
            ('status', status),
            ('offset', offset),
            ('limit', limit),
            ('sortBy', sortBy),
            ('sortOrder', sortOrder),
        )
        response = self._GET(url, params)

        return response

    def get_country_list(self, search='', offset=0, limit=10):
        '''
        get country list
        :param search: String. Search string for country by prefix, eg. search by 'jap' will return Japan.
        :param offset: Integer. Starting index of the list eg.4
        :param limit: Integer. Number of countries in a list(max 100), e.g. 10
        '''
        url = 'https://api.codechef.com/country'
        params = (
            ('search', search),
            ('offset', offset),
            ('limit', limit),
        )
        response = self._GET(url, params)

        return response

    def run_code(self, source_code, language, sample_input):
        '''
        takes input, language and source code and runs on codechef ide
        :param source_code: String. Source code of submission
        :param language: String. language of submission
        :param input: String. input of submission
        '''
        url = 'https://api.codechef.com/ide/run'
        params = (
            ('sourceCode', source_code),
            ('language', language),
            ('input', sample_input),
        )
        response = self._GET(url, params)

        return response

    def get_status_code(self, link):
        '''
        get status of submitted code
        :param link: String. Enter status code recieved after code execution. eg. VGQUp0
        '''
        url = 'https://api.codechef.com/ide/status'
        params = (
            ('link', link),
        )
        response = self._GET(url, params)

        return response

    def get_institutions(self, search, offset=0, limit=10):
        '''
        get list of institutions
        :param search: String. Search string for institution. eg. jaypee
        :param offset: Integer. Starting index of list
        :param limit: Integer. Number of entities to be fetched, max 100
        '''
        url = 'https://api.codechef.com/ide/institution'
        params = (
            ('search', search),
            ('offset', offset),
            ('limit', limit),
        )
        response = self._GET(url, params)

        return response

    def get_languages(self, search='', offset=0, limit=10):
        '''
        get list of languages on codechef
        :param search: String. Search string for lnguage. eg. c
        :param offset: Integer. Starting index of list
        :param limit: Integer. Number of languages to be fetched, max 100
        '''
        url = 'https://api.codechef.com/ide/language'
        params = (
            ('search', search),
            ('offset', offset),
            ('limit', limit),
        )
        response = self._GET(url, params)

        return response

    def get_problems_by_category(self, category_name, fields=[], offset=0, limit=10, sortBy='successfulSubmissions', sortOrder='asc'):
        '''
        get list of problems by category name provided
        :param category_name: String. Possible categories are: school, easy, medium, hard, challenge, extcontest
        :param fields: List. Possible fields are: problemCode, problemName, successfulSubmissions, accuracy. Multiple fields can be entered using comma.
        :param offset: Integer. Starting index of the list eg.4
        :param limit: Integer. Number of problems in a list(max 100), e.g. 10
        :param sortBy: String. Possible fields are: problemCode, problemName, successfulSubmissions, accuracy.
        :param sortOrder: String. Possible fields are: asc, desc
        '''
        url = 'https://api.codechef.com/problems/' + category_name
        params = (
            ('fields', ','.join(fields)),
            ('offset', offset),
            ('limit', limit),
            ('sortBy', sortBy),
            ('sortOrder', sortOrder),
        )
        response = self._GET(url, params)

        return response

    def get_problems_by_tags(self, tags=[], fields=[], limit=10, offset=0):
        '''
        get problems by given tags
        :param tags: List. Takes comma separated tags/authors. eg: jan13,kingofnumbers
        :param fields: List. Possible fields are: code, tags, author, solved, attempted, partiallySolved. Multiple fields can be entered using comma.
        :param limit: Integer. Limit of list(max 20)
        :param offset: Integer. Starting index of list
        '''
        url = 'https://api.codechef.com/tags/problems'
        params = (
            ('filter', ','.join(tags)),
            ('fields', ','.join(fields)),
            ('limit', limit),
            ('offset', offset),
        )
        response = self._GET(url, params)

        return response

    def get_rankings(self, contest_code, fields=[], country='', institution='', institutionType='', offset=0, limit=10, sortBy='rank', sortOrder='asc'):
        '''
        get rankings for a particular contest
        :param contest_code: String. Contest code eg. JAN17
        :param fields: List. Possible fields are: rank, username, totalTime, penalty, country, countryCode, institution, rating, institutionType, contestId, contestCode, totalScore, problemScore. Multiple fields can be entered using comma.
        :param country: String. Country to which the user belongs, eg. India
        :param institution: String. Institution to which the user belongs, eg. Jaypee Institute of Information Technology
        :param institutionType: String. Possible values: school, college or organization.
        :param offset: Integer. Starting index of the list eg.4
        :param limit: Integer. Number of rankings in a list(max 100), e.g. 10
        :param sortBy: String. Possible fields are: rank.
        :param sortOrder: String. Possible fields are: asc, desc
        '''
        url = 'https://api.codechef.com/rankings/' + contest_code
        params = (
            ('fields', ','.join(fields)),
            ('country', country),
            ('institution', institution),
            ('institutionType', institutionType),
            ('offset', offset),
            ('limit', limit),
            ('sortBy', sortBy),
            ('sortOrder', sortOrder),
        )
        response = self._GET(url, params)

        return response

    def get_ratings(self, contest_type, fields=[], country='', institution='', institutionType='', offset=0, limit=10, sortBy='globalRank', sortOrder='asc'):
        '''
        get rankings for a particular contest
        :param contest_type: String. enter contest type for which you want to fetch the ranklist: all, cookOff, longChallenge, lunchTime, cookOffSchool, longChallengeSchool, lunchTimeSchool, allSchool.
        :param fields: List. Possible fields are: username, globalRank, countryCode, countryRank, country, institution, institutionType, rating, diff.  Multiple fields can be entered using comma.
        :param country: String. Country to which the user belongs, eg. India
        :param institution: String. Institution to which the user belongs, eg. Jaypee Institute of Information Technology
        :param institutionType: String. Possible values: school, college or organization.
        :param offset: Integer. Starting index of the list eg.4
        :param limit: Integer. Number of rankings in a list(max 100), e.g. 10
        :param sortBy: String. Possible fields are: username, globalRank, rating, diff.
        :param sortOrder: String. Possible fields are: asc, desc
        '''
        url = 'https://api.codechef.com/ratings/' + contest_type
        params = (
            ('fields', ','.join(fields)),
            ('country', country),
            ('institution', institution),
            ('institutionType', institutionType),
            ('offset', offset),
            ('limit', limit),
            ('sortBy', sortBy),
            ('sortOrder', sortOrder),
        )
        response = self._GET(url, params)

        return response

    def add_set(self):
        '''
        '''
        pass

    def delete__set(self):
        '''
        '''
        pass

    def get_set_details(self):
        '''
        '''
        pass

    def add_member_set(self):
        '''
        '''
        pass

    def delete_member_set(self):
        '''
        '''
        pass

    def get_member_set(self):
        '''
        '''
        pass

    def update_set(self):
        '''
        '''
        pass

    def get_submissions(self):
        '''
        '''
        pass

    def get_submission_details(self):
        '''
        '''
        pass

    def add_problem_todo(self):
        '''
        '''
        pass

    def delete_todo_all(self):
        '''
        '''
        pass

    def delete_problem_todo(self):
        '''
        '''
        pass

    def get_todo_list(self):
        '''
        '''
        pass

    def get_user_list(self, search, fields=[], offset=0, limit=10):
        '''
        get users list
        :param search: String. Search user by prefix
        :param fields: List. Possible fields are: username, fullname, country, state, city, rankings, ratings, occupation, organization, language. Multiple fields can be entered using comma.
        :param offset: Integer. Starting index of list
        :param limit: Integer. Number of users to be fetched, max 20
        '''
        url = 'https://api.codechef.com/users'

        params = (
            ('fields', ','.join(fields)),
            ('offset', offset),
            ('limit', limit),
            ('search', search),
        )
        response = self._GET(url, params)

        return response

    def whoami(self):
        '''
        fetch details of login user
        '''
        url = 'https://api.codechef.com/users/me'
        response = self._GET(url)

        return response

    def get_user(self, user_name, fields=[]):
        '''
        get details of a user
        :param user_name: String. username of user eg. arpit147
        :param fields: List. Possible fields are: username, fullname, country, state, city, rankings, ratings, occupation, language, organization, problemStats, submissionStats. Multiple fields can be entered using comma.
        '''
        url = 'https://api.codechef.com/users/' + user_name
        params = (
            ('fields', ','.join(fields)),
        )
        response = self._GET(url, params)

        return response
