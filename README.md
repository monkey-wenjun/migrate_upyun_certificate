# migrate_upyun_certificate

## 脚本介绍

又拍最新推出的 Let's encrypt 通配符证书自动续签需要 999 元， 对于个人建站使用CDN加速希望使用通配符证书，无疑是比较贵的。

![](https://file.awen.me/blog/20201027131046.png)

但是我又希望只签发一个通配符证书，这样可以配置多个二级域名进行 CDN 加速，好在又拍云除了提供收费自动续签通配符证书的方式，还提供了自动上传证书的方式。 
不过这种方式有一个缺陷，那就是由于我使用的 Let's encrypt 证书需要 2 个月续签一次， 不过好在 Let's encrypt 支持自动续签.

通过 [acme.sh](https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E) 这个 Shell 脚本配置 DNS API 的方式进行自动续签证书。 

这样证书会在 60 天以后会自动更新, 无需任何操作. 整个过程都是自动的, 用户不需要关心。

那么有了这个功能之后，要解决的就是我将自动续签完的证书内容上传到又拍云并替换掉旧的证书就可以了。

本脚本可以实现将你将本地或服务器上签发的 Let's encrypt 通配符证书， 通过配置 Linux 计划任务的方式定期上传到又拍云并自动进行迁移后删除旧的证书。

## 使用说明

1.首先，假设你已经通过acme.sh 使用 DNS API 的方式申请好了通配符证书。

2.执行
```
git clone git@github.com:monkey-wenjun/migrate_upyun_certificate.git
```


3.打开 migrate_upyun_certificate.py ，找到如下配置

```
############# 配置信息段 #############
username = "upyun"  # 又拍云用户名，必填
password = "upyun"  # 又拍云密码，必填
check_domain = "awen.me"  # 要配置的证书，避免误删其他过期证书，必填
certificate_path = "/usr/local/nginx/conf/ssl/awen.me/fullchain.cer"  # 证书公钥，建议配置待根证书的证书内容，否则在部分浏览器可能会出现问题。必填
private_key_path = "/usr/local/nginx/conf/ssl/awen.me/awen.me.key"  # 证书私钥，必填
domain_conf_path = "/usr/local/nginx/conf/ssl/awen.me/awen.me.conf"  # 证书更新配置文件，用户读取下一次更新时间
############# 配置信息结束 #############
```

假设你的证书在/usr/local/nginx/conf/ssl/

配置又拍云的登录用户名和密码
配置 certificate_path 和 private_key_path 为你的证书公钥和私钥路径；
配置 check_domain 为要替换的通配符域名，此选项可以在替换完成证书后，帮助你删除又拍云中已经过期的旧证书；
配置 domain_conf_path， 该选项会读取 acme.sh 生成的证书配置文件，获取 Le_CertCreateTime 字段，该字段为最近一次更新证书的时间，脚本会在该时间点左右进行自动更新证书；
该文件内容如下

```
[root@VM-0-12-centos ~]# cat /usr/local/nginx/conf/ssl/awen.me/awen.me.conf 
Le_Domain='awen.me'
Le_Alt='*.awen.me'
Le_Webroot='dns_cf'
Le_PreHook=''
Le_PostHook=''
Le_RenewHook=''
Le_API='https://acme-v02.api.letsencrypt.org/directory'
Le_Keylength=''
Le_OrderFinalize='https://acme-v02.api.letsencrypt.org/acme/finalize/XX/XXX'
Le_LinkOrder='https://acme-v02.api.letsencrypt.org/acme/order/XX/XXX'
Le_LinkCert='https://acme-v02.api.letsencrypt.org/acme/cert/XXXX'
Le_CertCreateTime='1603763751'
Le_CertCreateTimeStr='2020年 10月 27日 星期二 01:55:51 UTC'
Le_NextRenewTimeStr='2020年 12月 26日 星期六 01:55:51 UTC'
Le_NextRenewTime='1608861351'

```

4.在本地或 Linux 配置计划任务，每天执行一次这个脚本

```
30 03 * * * /usr/bin/python3 /opt/migrate_upyun_certificate/migrate_upyun_certificate.py
```
