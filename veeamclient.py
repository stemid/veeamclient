import xml.etree.ElementTree as ET
from pprint import pprint as pp
from base64 import b64decode
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class VeeamSession(object):
    
    def __init__(self, **args):
        self.api_hostname = args.get('hostname', 'localhost')
        self.api_username = args.get('username')
        self.api_password = args.get('password')
        self.api_ssl = args.get('use_tls', False)
        self.api_verify_ssl = args.get('verify_tls', True)
        self.api_namespace = {
            'veeam': args.get(
                'namespace',
                'http://www.veeam.com/ent/v1.0'
            )
        }

        # Shortcut to namespace
        self._ns = self.api_namespace

        if self.api_ssl:
            self.api_port = args.get('port', 9398)
            self.api_url = 'https://{hostname}:{port}/api/'.format(
                hostname=self.api_hostname,
                port=self.api_port
            )
        else:
            self.api_port = args.get('port', 9399)
            self.api_url = 'http://{hostname}:{port}/api/'.format(
                hostname=self.api_hostname,
                port=self.api_port
            )

        self.api_session_headers = {
            'Content-type': 'text/xml',
            'X-Requested-With': 'VeeamClient'
        }

        self.api_auth_url = self._get_auth_url()

        (self.session_id, self.session_id_plain) = self._login()


    def _get_auth_url(self):
        result = requests.get(
            self.api_url,
            headers=self.api_session_headers,
            verify=self.api_verify_ssl
        )

        xml_result = ET.fromstring(result.text)
        links = xml_result.find('veeam:Links', self._ns)
        for link in links:
            if link.attrib.get('Rel') == 'Create':
                return link.attrib.get('Href')
        else:
            raise StandardError('Could not find Create URL from API')


    def _login(self):
        auth_data = (self.api_username, self.api_password)

        result = requests.post(
            self.api_auth_url,
            auth=auth_data,
            headers=self.api_session_headers,
            verify=self.api_verify_ssl
        )

        if result.status_code != 201:
            raise StandardError('Could not login: {error}'.format(
                error=str(result.text)
            ))

        session_id = result.headers['X-RestSvcSessionId']
        session_id_plain = b64decode(session_id)

        self.api_session_headers['X-RestSvcSessionId'] = session_id

        return session_id, session_id_plain


    def post_path(self, path, payload=None):
        req_url = '{url}/{path}'.format(
            url=self.api_url,
            path=path
        )

        result = requests.post(
            req_url,
            headers=self.api_session_headers,
            verify=self.api_verify_ssl,
            data=payload
        )

        return result


    def get_path(self, path):
        req_url = '{url}/{path}'.format(
            url=self.api_url,
            path=path
        )

        result = requests.get(
            req_url,
            headers=self.api_session_headers,
            verify=self.api_verify_ssl
        )

        return result


    def _check_login(self):
        result = self.get_path('/logonSessions/{session_id}'.format(
            session_id=self.api_session_id_plain
        ))
        
        if result.status_code == 401:
            return False
        
        return True


    def get_logonSessions(self):
        result = self.get_path('/logonSessions')
        return ET.fromstring(result.text)


    def get_logonSession(self, session_id):
        result = self.get_path('/logonSessions/{id}'.format(
            id=session_id
        ))
        return ET.fromstring(result.text)


    def get_capabilities(self):
        session = self.get_logonSession(self.session_id_plain)
        links = session.find('veeam:Links', self._ns)
        return links


    @property
    def logged_in(self):
        return self._check_login()
    

    @property
    def logonSessions(self):
        return self.get_logonSessions()


    @property
    def logonSession(self):
        return self.get_logonSession(self.session_id_plain)


    @property
    def namespace(self):
        return self.api_namespace

    @namespace.setter
    def namespace(self, namespace={}):
        self.api_namespace = namespace
        self._ns = self.api_namespace


    @property
    def logon_paths(self):
        links = self.get_capabilities()
        paths = []

        for link in links:
            url = link.attrib.get('Href')
            paths.append(
                '/{path}'.format(
                    path=url.split(self.api_url, 2)[-1]
                )
            )
        return paths


class BaseVeeam(object):

    def __init__(self, session):
        if session.logged_in:
            self._s = session
        else:
            raise StandardError('Must log in with VeeamSession first')


class VeeamReports(BaseVeeam):

    def _get_summary_job_statistics(self):
        statistics = self._s.get_path('/reports/summary/job_statistics')
        return ET.fromstring(statistics.text)


    def _get_summary_overview(self):
        overview = self._s.get_path('/reports/summary/overview')
        return ET.fromstring(overview.text)


    @property
    def job_statistics(self):
        return self._get_summary_job_statistics()
