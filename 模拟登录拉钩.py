#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-17,10:07"

# data = {"k1":2,"l2":4,"l5":9,"l4":6}
# data2 = sorted(data.items(),key=lambda asd:asd[0],reverse = True)
import requests
import re

session = requests.session ()
# 获取登录页面,获取X_Anti_Forge_Token，X_Anti_Forge_Code
# url  https://passport.lagou.com/login/login.html
response = session.get (
    "https://passport.lagou.com/login/login.html",
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
)
X_Anti_Forge_Token = re.findall ("X_Anti_Forge_Token = '(.*?)'",response.text,re.S) [0]
X_Anti_Forge_Code = re.findall ("X_Anti_Forge_Code = '(.*?)'",response.text,re.S) [0]

#登录
#url https://passport.lagou.com/login/login.json
#请求方式 POST
#请求头：
# cookie
# Referer https://passport.lagou.com/login/login.html
# user-agent
# "X-Anit-Forge-Code":"X_Anti_Forge_Code"
# "X-Anit-Forge-Token":"X_Anti_Forge_Token"
# "X-Requested-With":"XMLHttpRequest"
#请求体：
# "isValidate":"True"
# "username":"18611453110"
# "password":"70621c64832c4d4d66a47be6150b4a8e"
# "request_form_verifyCode":""
# "submit":""
session.post ("https://passport.lagou.com/login/login.json",
              headers = {
                  'User-Agent':"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                  "Referer":"https://passport.lagou.com/login/login.html",
                  "X-Anit-Forge-Code":X_Anti_Forge_Code,
                  "X-Anit-Forge-Token":X_Anti_Forge_Token,
                  "X-Requested-With":"XMLHttpRequest",
              },
              data = {
                  "isValidate":True,
                  "username":"18611453110",
                  "password":"70621c64832c4d4d66a47be6150b4a8e",
                  "request_form_verifyCode":"",
                  "submit":""
              })
#第三步 授权
# url https://passport.lagou.com/grantServiceTicket/grant.html
# 请求方式 GET
#请求头：
# cookie
# Referer:https://passport.lagou.com/login/login.html
# User-Agent:Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36

session.get ("https://passport.lagou.com/grantServiceTicket/grant.html",headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Referer":"https://passport.lagou.com/login/login.html"
})

# 第四步 验证是否登录成功
# url https://www.lagou.com/resume/myresume.html
#请求方式：GET
#请求头
#User-Agent:Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36

res = session.get ("https://www.lagou.com/resume/myresume.html",headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
})
print ('18611453110' in res.text)

# 第五步 筛选职位信息
# url https://www.lagou.com/jobs/list_PHP%E5%BC%80%E5%8F%91
# 请求方式 GET
# 请求头
#User-Agent:Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
#请求参数
#gj=3年及以下
#px=default
#yx=15k-25k
#city=北京

from urllib.parse import urlencode

position = input ("搜索职位>>>:")
res = urlencode ({"k":position},encoding = "utf-8").split ("=") [-1]
url = "https://www.lagou.com/jobs/list_" + res

# url https://www.lagou.com/jobs/positionAjax.json
# 请求方式 POST
# 请求头：
#Referer:url
# User-Agent:Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
# 请求体
# first:true
# pn:1
# kd:PHP开发
# 请求参数
#params = {
#"gj":"3年及以下",
#"px":"default",
#"yx":"15k-25k",
#"city":"北京",
# "needAddtionalResult":"false",
# "isSchoolJob":"0"
# }
r6 = session.post ('https://www.lagou.com/jobs/positionAjax.json',headers = {
    "Referer":url,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
},
                   data = {
                       "first":True,
                       "pn":1,
                       "kd":"PHP开发"
                   },
                   params = {
                       "gj":"3年及以下",
                       "px":"default",
                       "yx":"15k-25k",
                       "city":"北京",
                       "needAddtionalResult":"false",
                       "isSchoolJob":"0"
                   }
                   )
company_list = r6.json () ['content'] ['positionResult'] ['result']
for company in company_list:
    positionId = company ["positionId"],
    company_link = "https://www.lagou.com/jobs/%s.html" % positionId # 公司详细链接
    companyShortName = company ["companyShortName"], # 公司名
    positionName = company ["positionName"], # 招聘职位
    salary = company ["salary"] # 薪资
    print ("""
    详情链接：%s,
    公司名：%s,
    岗位：%s,
    薪资：%s
    """ % (company_link,companyShortName,positionName,salary))

    # 第七步 访问详情页 获取X_Anti_Forge_Token，X_Anti_Forge_Code
    # url company_link
    # 访问方式 GET
    # 请求头
    session.get (company_link,headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    })
    X_Anti_Forge_Token = re.findall ("X_Anti_Forge_Token = '(.*?)'",response.text,re.S) [0]
    X_Anti_Forge_Code = re.findall ("X_Anti_Forge_Code = '(.*?)'",response.text,re.S) [0]

    #第八步 投递简历
    # 请求url https://www.lagou.com/mycenterDelay/deliverResumeBeforce.json
    # 请求方式 POST
    # 请求头：
    #请求头：
    #Referer:详情页地址
    #User-agent
    #X-Anit-Forge-Code:53165984
    #X-Anit-Forge-Token:3b6a2f62-80f0-428b-8efb-ef72fc100d78
    #X-Requested-With:XMLHttpRequest
    # 请求体
    #请求体：
    # positionId:职位ID
    # type:1
    # force:true
    session.post ("https://www.lagou.com/mycenterDelay/deliverResumeBeforce.json",
                  headers = {
                      "User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                      "X-Anit-Forge-Code":"53165984",
                      "X-Anit-Forge-Token":"3b6a2f62-80f0-428b-8efb-ef72fc100d78",
                      "X-Requested-With":"XMLHttpRequest"
                  },data = {
            "positionId":"职位ID",
            "type":1,
            "force":"true"
        })
    print("%s投递成功"%companyShortName)
