#!/usr/bin/env python
# -*- coding: utf-8 -*-#!/usr/bin/env python


from bs4 import BeautifulSoup as bs
import mechanize
import re
import os
import time
import string
import gevent
from gevent.pool import Pool


groupID=raw_input("输入小组ID或名字:")

mgroup_url="http://m.douban.com/group/%s/"%groupID
group_url="http://www.douban.com/group/%s/"%groupID

try:
    os.mkdir("c:/doubanData/group/%s/"%groupID)
except :
    pass



def removeOldData():
    try:
        os.remove("c:/doubanData/group/%s/allPages.txt"%groupID)
    except:
        pass   
    try:
        os.remove("c:/doubanData/group/%s/topic_ID.txt"%groupID)
    except:
        pass

def redial_router():
    print "Redialing"
    import urllib2,cookielib,base64
    upas = base64.b64encode('admin:admin')
    #print upas
    ip = "192.168.1.1"
    url= "http://192.168.1.1/userRpm/StatusRpm.htm?Disconnect=%B6%CF%20%CF%DF&wan=1"
    url2="http://192.168.1.1/userRpm/StatusRpm.htm?Connect=%C1%AC%20%BD%D3&wan=1"
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))   
    urllib2.install_opener(opener)
    #print 'ready to reboot%s' %ip
    #print 'fake login name'
    opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1)'),('Accept-Encoding','gzip, deflate'),('Authorization',' Basic '+upas),('Referer','http://192.168.1.1/userRpm/StatusRpm.htm')] 
    #print 'open page'
    req = urllib2.Request(url)
    req2=urllib2.Request(url2)
    #print 'sending requests'
    u = urllib2.urlopen(req)
    u2=urllib2.urlopen(req2)
    time.sleep(2)
    print '%sREDIAL COMPLETE'%ip
    print '-------------------------------------------'



def Max_Page_number(url=mgroup_url):
    br = mechanize.Browser()
    fisrtpage=br.open(url)
    soup=bs(fisrtpage.read())

    s=soup.find_all(class_=("paginator"))    #beautiful找到最后一页的标签

    for t in s:
        n=str(t.span.string)

    m=int(n[3:])                                 #提取出最后一页的页码
    max_number=m
    print "max_number=",m
    return max_number

def source_pages_download(Max_Page_number=Max_Page_number(),group_url=group_url):  #下载所有小组话题页面
    br = mechanize.Browser()
    page=""
    for i in range(Max_Page_number):
        url=group_url+"discussion?start="+str(i*20)
        print url
        page+=br.open(url).read()
        P=br.open(url).read()
        f=open("c:/doubanData/group/%s/allPages.txt"%groupID,"a+")            #永久本地化
        f.write(P)
        f.close()
                
    return page       #内存直接返回所有页面



def get_topic_ID():
    try:
        source_pages_download()
    except:
        redial_router()
        source_pages_download()

    f=open("c:/doubanData/group/%s/allPages.txt"%groupID,"a+") 
    f.close()
    o=open("c:/doubanData/group/%s/allPages.txt"%groupID,"r")   #打开页面文件 读取
    page=o.read()
    o.close()

    topic_ID=re.findall("(?<=topic\/)\d+",page)#从页面文件查找ID
    global topic_ID
    IDstr="" 
    print topic_ID
    for each in topic_ID: 
        IDstr=IDstr+"\n"+each
    t=open("c:/doubanData/group/%s/topic_ID.txt"%groupID,"a+")  #存储所有小组话题ID
    t.write(IDstr) 
    t.close()
    return topic_ID






def single_topic_download(ID):
    br=mechanize.Browser()
    mtopic_url="http://m.douban.com/group/topic/%s/"%ID                      #得到每个话题的标题
    mPage=br.open(mtopic_url).read()
    soup=bs(mPage)

    title=soup.title.string.strip()
    title=title.encode("utf-8")
    title=str(title)
    path="c:/doubanData/group/%s/%s.html"%(groupID,title)
    upath=unicode(path,"utf-8", errors="ignore")                   #转化为unicode 写入路径 这里很麻烦
    IDpath="c:/doubanData/group/%s/%s.html"%(groupID,str(ID))
    print title
    # name=re.findall("(.|\n)*(?=\()",title)
    # print name
    # name=name[0]
    # print name
    # #name=name.decode("utf-8")
    topic_url="http://www.douban.com/group/topic/%s/"%ID
    Page=br.open(topic_url).read()
    try:
        t=open(upath,"a")
    except :
        t=open(IDpath,"a")
      #存储所有小组话题ID
    t.write(Page)
    t.close()



def single_topic_download_with_retry(ID):
    try:
        return single_topic_download(ID)
    except:
        print "Need to Redial"
        print "Try Auto redial"
        redial_router()


        return single_topic_download_with_retry(ID)


    try:
        t=open(upath,"a")
    except :
        t=open(IDpath,"a")
      #存储所有小组话题ID
    t.write(Page)
    t.close()

removeOldData()
get_topic_ID()


pool=Pool(100)

pool.map(single_topic_download_with_retry,topic_ID)







# def all_topic_download(IDs=get_topic_ID()):

#     for i in IDs:
#         single_topic_download(i)
#         time.sleep(1)
        



# def main():
#     #removeOldData()
#     all_topic_download()


# if __name__ == '__main__':

#     main()

