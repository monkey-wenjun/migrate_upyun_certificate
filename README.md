# migrate_upyun_certificate

## 脚本介绍

又拍最新推出的let's encrypt 通配符证书需要 999 元，无疑是比较贵的。

![](https://file.awen.me/blog/20201027131046.png)

通过本脚本可以实现将你将本地签发的 let's encrypt 通配符证书， 通过配置计划任务的方式定期上传到又拍云并自动进行迁移后删除旧的证书

## 使用说明

1.首先，通过 https://github.com/acmesh-official/acme.sh  项目创建证书并配置自动更新证书

2.假设你的证书在/usr/local/nginx/conf/ssl/

配置脚本certificate_path 和private_key_path 为你的证书公钥和私钥路径

```
certificate_path = "/usr/local/nginx/conf/ssl/awen.me/fullchain.cer"
private_key_path = "/usr/local/nginx/conf/ssl/awen.me/awen.me.key"
```
并配置又拍云的登录用户名和密码

```
username = "xxxxx"
password = "xxxx"
```

3.linux 配置计划任务，比如每2个月执行一次这个脚本（前提执行脚本前，证书需要更新）

```
30 03 01 */2 * /usr/bin/python3 /opt/migrate_upyun_certificate/migrate_upyun_certificate.py
```