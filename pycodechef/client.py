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

        data = '{{"grant_type":"client_credentials" , "scope":"public set todo submission", "client_id":"{}","client_secret":"{}"}}'.format(client_id, client_secret)

        response = requests.post('https://api.codechef.com/oauth/token', headers=headers, data=data)
        response = response.json()

        if response['status'] == "OK":
            # print('Fetching access token...')
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

        try:
            return response.json()
        except ValueError as err:
            return {'success': False, 'error': err}

    def _POST(self, url, params=None, data=None):
        '''
        post to api
        :param url: String. endpoint to fetch
        :param params: query parameters given
        '''
        token = "Bearer {}".format(self.access_token)
        headers = {
            'Accept': 'application/json',
            'Authorization': token,
        }
        if params and data:
            response = requests.post(url, headers=headers, params=params, data=data)
        elif params:
            response = requests.post(url, headers=headers, params=params)
        elif data:
            response = requests.post(url, headers=headers, data=data)
        else:
            response = requests.post(url, headers=headers)

        try:
            return response.json()
        except ValueError as err:
            return {'success': False, 'error': err}

    def _DELETE(self, url, params=None):
        '''
        delete api
        :param url: String. endpoint to fetch
        :param params: query parameters given
        '''
        token = "Bearer {}".format(self.access_token)
        headers = {
            'Accept': 'application/json',
            'Authorization': token,
        }
        if params:
            response = requests.delete(url, headers=headers, params=params)
        else:
            response = requests.delete(url, headers=headers)

        try:
            return response.json()
        except ValueError as err:
            return {'success': False, 'error': err}

    def _PUT(self, url, params=None, data=None):
        '''
        put api
        :param url: String. endpoint to fetch
        :param params: query parameters given
        '''
        token = "Bearer {}".format(self.access_token)
        headers = {
            'Accept': 'application/json',
            'Authorization': token,
        }
        if params and data:
            response = requests.put(url, headers=headers, params=params, data=data)
        elif params:
            response = requests.put(url, headers=headers, params=params)
        elif data:
            response = requests.put(url, headers=headers, data=data)
        else:
            response = requests.put(url, headers=headers)

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
        response = self._POST(url, params)

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
        url = 'https://api.codechef.com/institution'
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
        url = 'https://api.codechef.com/language'
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

    def add_set(self, set_name, description):
        '''
        adds the set to user's account
        :param set_name: String. Set name in the form of string
        :param description: String. Enter the description of the set
        '''
        url = 'https://api.codechef.com/sets/add'
        data = (
            ('setName', set_name),
            ('description', description),
        )
        response = self._POST(url, data=data)

        return response

    def delete_set(self, set_name):
        '''
        delete the set from the user's account
        :param set_name: String. Enter the name of the set you want to delete
        '''
        url = 'https://api.codechef.com/sets/delete'
        params = (
            ('setName', set_name),
        )
        response = self._DELETE(url, params)

        return response

    def get_set_details(self, fields=[]):
        '''
        shows all sets created by user
        :param fields: List. Possible fields are: setName, description.
        '''
        url = 'https://api.codechef.com/sets/'
        params = (
            ('fields', ','.join(fields)),
        )
        response = self._GET(url, params)

        return response

    def add_member_set(self, set_name, member_handle):
        '''
        adds set members to an existing set
        :param set_name: String. Set name.
        :param member_handle: String. Enter the username.
        '''
        url = 'https://api.codechef.com/sets/members/add'
        data = (
            ('setName', set_name),
            ('memberHandle', member_handle),
        )
        response = self._POST(url, data=data)

        return response

    def delete_member_set(self, set_name, member_handle):
        '''
        removes members belonging to a set
        :param set_name: String. Set name whose set member you want to delete.
        :param member_handle: String. Enter the username of the set member you want to remove from set.
        '''
        url = 'https://api.codechef.com/sets/members/delete'
        params = (
            ('setName', set_name),
            ('memberHandle', member_handle),
        )
        response = self._DELETE(url, params)

        return response

    def get_member_set(self, set_name, fields=[]):
        '''
        get set details
        :param set_name: String. Set name
        :param fields: List. Possible fields are: setName, memberName, country, allContestRating,longContestRating, shortContestRating, lTimeContestRating, allSchoolContestRating, longSchoolContestRating, shortSchoolContestRating, lTimeSchoolContestRating. Multiple fields can be entered using comma.
        '''
        url = 'https://api.codechef.com/sets/members/get'
        params = (
            ('setName', set_name),
            ('fields', ','.join(fields)),
        )
        response = self._GET(url, params)

        return response

    def update_set(self, set_name, set_name_new, description):
        '''
        updates set
        :param set_name: String. Set name
        :param set_name_new: String. New set name
        :param description: String. Description
        '''
        url = 'https://api.codechef.com/sets/update'
        data = (
            ('setName', set_name),
            ('setNameNew', set_name_new),
            ('description', description),
        )
        response = self._PUT(url, data=data)

        return response

    def get_submissions(self, result='', year='', username='', language='', problem_code='', contest_code='', fields=[]):
        '''
        get submissions
        :param result: String. Search submission by result, eg. AC, WA, RE etc.
        :param year: Integer. Search submission by year, eg. 2012
        :param username: String. Search submission by username, eg. arpit147
        :param language: String. Search submission by language, eg. C++ 4.3.2
        :param problem_code: String. Code for problem, eg. SALARY
        :param contest_code: String. Code of contest, eg. JAN13
        :param fields: List. Possible fields are: id, date, username, problemCode, language, contestCode, result, time, memory. Multiple fields can be entered using comma.
        '''
        url = 'https://api.codechef.com/submissions/'
        params = (
            ('result', result),
            ('year', year),
            ('username', username),
            ('language', language),
            ('problemCode', problem_code),
            ('contestCode', contest_code),
            ('fields', ','.join(fields)),
        )
        response = self._GET(url, params)

        return response

    def get_submission_details(self, submission_id, fields=[]):
        '''
        fetches details of a submission.
        :param submission_id: Integer. submission id
        :param fields: List. Possible fields are: id, date, username, problemCode, language, contestCode, result, time, memory. Multiple fields can be entered using comma.
        '''
        url = 'https://api.codechef.com/submissions/' + str(submission_id)
        params = (
            ('fields', ','.join(fields)),
        )
        response = self._GET(url, params)

        return response

    def add_problem_todo(self, problem_code, contest_code):
        '''
        adds a problem to todo list
        :param problem_code: String.
        :param contest_code: String.
        '''
        url = 'https://api.codechef.com/todo/add'
        data = (
            ('problemCode', problem_code),
            ('contestCode', contest_code),
        )
        response = self._POST(url, data=data)

        return response

    def delete_todo_all(self):
        '''
        deletes all the problems added to todo list
        '''
        url = 'https://api.codechef.com/todo/delete/all'
        response = self._DELETE(url)

        return response

    def delete_problem_todo(self, problem_code):
        '''
        '''
        url = 'https://api.codechef.com/todo/delete/'
        params = (
            ('problemCode', problem_code),
        )
        response = self._DELETE(url, params)

        return response

    def get_todo_list(self, fields=[]):
        '''
        gets problems listed in todo
        '''
        url = 'https://api.codechef.com/todo/problems'
        params = (
            ('fields', ','.join(fields)),
        )
        response = self._GET(url, params)

        return response

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
