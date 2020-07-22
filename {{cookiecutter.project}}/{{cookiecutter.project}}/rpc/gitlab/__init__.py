import logging
import requests
import json
from requests.exceptions import RequestException

from {{cookiecutter.project}} import exception

logger = logging.getLogger(__file__)

gitlab_url = 'http://code.corp.rs.com'

gitlab_username = 'qm_system'
gitlab_password = 'R1d#2@19'
gitlab_access_token = 'Lny11vEY6H4c2b3iiHjD'


class Gitlab(object):
    base_url = "http://code.corp.rs.com/api/v3"
    method = 'get'
    request_params = None
    request_body = None
    path = ""
    headers = {'content-type': 'application/json;charset=UTF-8', "Private-Token": gitlab_access_token}
    timeout = 30
    try_count = 2
    deprecated = False

    def send(self, raise_exception=True):
        url = self.base_url + self.path
        error_msg = ""
        for i in range(self.try_count):
            try:
                resp = requests.request(self.method, url, params=self.request_params, json=self.request_body, headers=self.headers, timeout=self.timeout)
            except RequestException as e:
                logger.error("rpc gitlab request({} {} {}) request error: {}".format(
                    url, json.dumps(self.request_params, sort_keys=True), json.dumps(self.request_body, sort_keys=True), str(e)
                ))
                error_msg = str(e)
                continue
            else:
                logger.info("rpc gitlab request({} {} {}) response({} {})".format(
                    url, json.dumps(self.request_params, sort_keys=True), json.dumps(self.request_body, sort_keys=True), resp.status_code, resp.content.decode('utf-8')
                ))

                resp_json = resp.json()

                if resp.status_code >= 400:
                    error_msg = resp_json.get("message") or resp_json.get("error") or "请求失败，请联系管理员"
                    continue
                return self.process_resp(resp_json)
        if raise_exception:
            exception.raise_system_error(message=error_msg)

    def process_resp(self, resp):
        raise NotImplementedError

