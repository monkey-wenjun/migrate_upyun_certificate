#!/usr/bin/env python
# -*-coding:utf-8-*-

from requests import Session
from time import time

"""
@ author:wenjun
@ E-mail: hi@awen.me
@ datetime:2020/10/27 9:34 上午
@ software: PyCharm
@ filename: migrate_upyun_certificate.py
"""


class MigrateUpyunCertificate:

    def __init__(self):
        self.session = Session()

    def login(self, username, password):
        """
        登录又拍云
        :param username:
        :param password:
        :return:
        """
        url = "https://console.upyun.com/accounts/signin/"

        payload = {"username": username, "password": password}
        headers = {
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Content-Length': "56",
            'Content-Type': "application/json",
            'DNT': "1",
            'Host': "console.upyun.com",
            'Origin': "https://console.upyun.com",
            'Pragma': "no-cache",
            'Referer': "https://console.upyun.com/login/",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            'cache-control': "no-cache",
            'Postman-Token': "2d9bd080-b549-4c41-89ce-0b011f344a3f"
        }

        response = self.session.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.cookies

    def get_ssl_list(self):
        """
        获取SSL 列表
        :return:
        """
        url = "https://console.upyun.com/api/https/certificate/list/?limit=10"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'console.upyun.com',
            'Pragma': 'no-cache',
            'Referer': 'https://console.upyun.com/toolbox/ssl/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'ame-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                          '(KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }

        response = self.session.get(url, headers=headers)
        if response.status_code == 200:
            resp_json = response.json()
            result = resp_json["data"]["result"]
            return result

    @staticmethod
    def format_result_info(result_json, check_domain):
        """
        格式化输出cer_id 以及到期时间等信息
        :param result_json:
        :return:
        """
        cer_list = []
        for key, value in result_json.items():
            cer_id = key
            if len(key) != 32:
                continue
            common_name = value["commonName"]
            validity_end = value["validity"]["end"]
            if common_name != check_domain:
                continue
            data = {
                "cer_id": cer_id,
                "domain": common_name,
                "validity_end": validity_end
            }
            cer_list.append(data)
        return cer_list

    def upload_cerfile(self, certificate_path, private_key_path):
        """
        上传证书
        :param private_key_path:
        :param certificate_path:
        :return:
        """
        with open(certificate_path) as f:
            certificate_str = f.read()
        with open(private_key_path) as k:
            private_key_str = k.read()
        url = "https://console.upyun.com/api/https/certificate/"

        payload = {"certificate": certificate_str.strip("\n"),
                   "private_key": private_key_str.strip("\n")
                   }
        headers = {

            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'zip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'DNT': '1',
            'Host': 'console.upyun.com',
            'Origin': 'https://console.upyun.com',
            'Pragma': 'no-cache',
            'Referer': 'https://console.upyun.com/toolbox/ssl/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
        response = self.session.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            resp_json = response.json()
            common_name = resp_json["data"]["result"]["commonName"]
            certificate_id = resp_json["data"]["result"]["certificate_id"]
            validity_start = resp_json["data"]["result"]["validity"]["start"]
            validity_end = resp_json["data"]["result"]["validity"]["end"]
            data = {
                "common_name": common_name,
                "certificate_id": certificate_id,
                "validity_start": validity_start,
                "validity_end": validity_end

            }
            return data

    def migrate_certificate(self, new_cer_id, old_cer_id):
        """
        证书迁移
        :param new_cer_id:
        :param old_cer_id:
        :return:
        """
        url = "https://console.upyun.com/api/https/migrate/certificate"

        payload = {"old_crt_id": old_cer_id, "new_crt_id": new_cer_id}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'DNT': '1',
            'Host': 'console.upyun.com',
            'Origin': 'https://console.upyun.com',
            'Pragma': 'no-cache',
            'Referer': 'https://console.upyun.com/toolbox/ssl/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }

        response = self.session.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return False
        resp_json = response.json()
        if resp_json["data"]["result"]:
            print("证书迁移结果 {}".format(resp_json["data"]["result"]))
            return True

    def delete_certificate(self, certificate_id, by_time):

        """
        删除旧的证书
        :param certificate_id:
        :return:
        """
        if by_time > 0:
            return
        url = "https://console.upyun.com/api/https/certificate/?certificate_id={}".format(certificate_id)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'console.upyun.com',
            'Origin': 'https://console.upyun.com',
            'Pragma': 'no-cache',
            'Referer': 'https://console.upyun.com/toolbox/ssl/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }

        response = self.session.delete(url, headers=headers)
        if response.status_code != 200:
            return False
        resp_json = response.json()
        print("证书删除结果 {}".format(resp_json))
        return True

    def main(self):

        ############# 配置信息段 #############
        username = "upyun"  # 又拍云用户名，必填
        password = "upyun"  # 又拍云密码，必填
        check_domain = "baidu.com"  # 要配置的证书，避免误删其他过期证书，必填
        certificate_path = "/usr/local/nginx/conf/ssl/awen.me/fullchain.cer"  # 证书公钥，建议配置待根证书的证书内容，否则在部分浏览器可能会出现问题。必填
        private_key_path = "/usr/local/nginx/conf/ssl/awen.me/awen.me.key"  # 证书私钥，必填

        ############# 配置信息结束 #############

        print("开始登录又拍云")
        self.login(username=username, password=password)
        print("开始获取证书列表")
        result_json = self.get_ssl_list()
        cer_list = self.format_result_info(result_json, check_domain)
        old_cer_id = cer_list[-1]["cer_id"]
        validity_end = cer_list[-1]["validity_end"]
        unix_time = int(time()) * 1000
        by_time = unix_time - int(validity_end)
        print("开始读取本地证书公钥和私钥信息")
        print("开始上传证书")
        upload_cerfile_info = self.upload_cerfile(certificate_path=certificate_path,
                                                  private_key_path=private_key_path)
        new_cer_id = upload_cerfile_info["certificate_id"]
        print("开始迁移证书")
        self.migrate_certificate(new_cer_id=new_cer_id, old_cer_id=old_cer_id)
        print("开始删除证书")
        self.delete_certificate(old_cer_id, by_time)


if __name__ == '__main__':
    migrate_upyun_certificate = MigrateUpyunCertificate()
    migrate_upyun_certificate.main()
