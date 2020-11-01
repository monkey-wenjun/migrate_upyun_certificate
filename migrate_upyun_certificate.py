#!/usr/bin/env python
# -*-coding:utf-8-*-
from requests import Session
from time import time, sleep

"""
@ author:wenjun
@ E-mail: hi@awen.me
@ datetime:2020/10/27 6:34 上午
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
        :param check_domain:
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
        :param by_time:
        :param certificate_id:
        :return:
        """
        if by_time < 0:
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
            print("证书删除失败，连接异常")
        resp_json = response.json()
        try:
            if resp_json["data"]["status"]:
                print("证书删除成功")
        except KeyError:
            print("证书删除失败")

    @staticmethod
    def read_acme_conf(conf_path, unix_time):
        with open(conf_path) as f:
            for i in (f.readlines()):
                key = i.strip().split("=")
                if key[0] == "Le_CertCreateTime":
                    le_cert_create_time = str(key[1]).replace("'", "")
                    return int(le_cert_create_time) - unix_time

    def main(self):

        """############# 配置信息段 #############"""
        username = "upyun_username"  # 又拍云用户名，必填
        password = "upyun_password"  # 又拍云密码，必填
        check_domain = "awen.me"  # 要配置的证书，避免误删其他过期证书，必填
        certificate_path = "/usr/local/nginx/conf/ssl/awen.me/fullchain.cer"  # 证书公钥，建议配置待根证书的证书内容，否则在部分浏览器可能会出现问题。必填
        private_key_path = "/usr/local/nginx/conf/ssl/awen.me/awen.me.key"  # 证书私钥，必填
        domain_conf_path = "/usr/local/nginx/conf/ssl/awen.me/awen.me.conf"  # 证书更新配置文件，用户读取下一次更新时间
        """############# 配置信息段 #############"""
        unix_time = int(time())
        update_time = int(self.read_acme_conf(domain_conf_path, unix_time))
        print(update_time)
        print("距离下一次更新还有 {} 天".format(update_time))
        if 0 < update_time < -86400:
            print("还早，不要这么急嘛！")
            return
        print("开始登录又拍云")
        self.login(username=username, password=password)
        print("开始获取证书列表")
        result_json = self.get_ssl_list()
        cer_list = self.format_result_info(result_json, check_domain)
        old_cer_id = cer_list[-1]["cer_id"]
        validity_end = cer_list[-1]["validity_end"]
        unix_time = unix_time * 1000
        by_time = unix_time - int(validity_end)
        print("开始读取本地证书公钥和私钥信息")
        print("开始上传证书")
        upload_cerfile_info = self.upload_cerfile(certificate_path=certificate_path,
                                                  private_key_path=private_key_path)
        new_cer_id = upload_cerfile_info["certificate_id"]
        print("开始迁移证书")
        self.migrate_certificate(new_cer_id=new_cer_id, old_cer_id=old_cer_id)
        sleep(20)
        print(by_time)
        print("开始删除已过期的 {} 证书".format(check_domain))
        self.delete_certificate(old_cer_id, by_time)


if __name__ == '__main__':
    migrate_upyun_certificate = MigrateUpyunCertificate()
    migrate_upyun_certificate.main()