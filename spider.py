#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup as bs
import mechanize
import re
import os
import time
def get50cent(pageMax):

    removeOldData()              #删除旧数据
    Dict={}

    for i in range(pageMax):
        t=i+1
        time.sleep(2)
        Dict.update(get5starList(pageSearch(t)))
        print "已搜索第%d页"%t

    t=open("c:/doubanData/50centDict.txt","a")  #组装成字典
    t.write(str(Dict))
    t.close()
    getAllID()
    return Dict

def getAllID():
    pagesoup=open("c:/doubanData/allPage.txt").read()
   
    allID=re.findall("(?<=people\/)\d+",pagesoup)
   
    IDstr=""
    print allID
    for each in allID:
        IDstr=IDstr+"\n"+each
        print IDstr
    t=open("c:/doubanData/allID.txt","a")  #存储所有评论者ID
    t.write(IDstr)
    t.close()

def removeOldData():
    try:
        os.remove("c:/doubanData/allID.txt")
    except:
        pass   
    try:
        os.remove("c:/doubanData/allPage.txt")
    except:
        pass
    try:                               #删除旧数据
        os.remove("c:/doubanData/50centID.txt")
    except:
        pass
    try:
        os.remove("c:/doubanData/50centName.txt")
    except:
        pass
    try:
        os.remove("c:/doubanData/50centDict.txt")
    except:
        pass

    try:
        os.remove("c:/doubanData/50centDemo.txt")
    except:
        pass

  

def get5starList(page):          #获取5星评论者名单
    soup=bs(page)             #用beautifulsoup读取页面
    ppl=soup.find_all(class_=re.compile("author")) #找到所有评论者信息的标签                 
    Dict={}

    for each in ppl:                            #对每个评论者判定 是否打5星，并输出评论者ID                                       
        star=each.find(text=re.compile("\(5"))
      
        if star is not None:
            IDtag=str(star.findPreviousSiblings(href=re.compile("people"))) #找到people的标签，输出ID
            ID=re.findall("(?<=people\/)\d+",IDtag)                     #用正则表达式输出ID
            ID=ID[0]
            IDn=ID+"\n"
            Name=re.findall("(?<=\>)(.*?)(?=\<)",IDtag)                   #输出名字
            Name=Name[0]
            Namen=Name+"\n"
            Name=Name.decode("utf-8")
            Dict[ID]=Name
            url="http://www.douban.com/people/"+ID
            Demo=Namen+url+"\n"
            t=open("c:/doubanData/50centID.txt","a")  #存储评论者标签到文件
            t.write(IDn)
            t.close()
            t=open("c:/doubanData/50centName.txt","a")  #存储评论者名字到文件
            t.write(Namen)
            t.close
            t=open("c:/doubanData/50centDemo.txt","a")  #存储评论者名字和URL到文件
            t.write(Demo)
            t.close
    print Dict
    return Dict
                              
def pageSearch(i):    #获取评论页面
    url="http://m.douban.com/movie/subject/24756984/comments?page=%d"%i
    br = mechanize.Browser()
    web=br.open(url)
    page=web.read()
    # soup=BeautifulSoup(page,fromEncoding="utf-8")
    # soup2=str(soup)          
    # StarTag=soup.find_all(text="5&#x661F;")

    f=open("c:/doubanData/allPage.txt","a")
    f.write(page)
    f.close()
    return page
  
  



#get50cent(500)

def savePuppetID():   
    f=open("c:/doubanData/50centID.txt","r")
   
    puppetList=[]
    IDstr=""
    for line in f.readlines():
        print line
        ID=line.strip()  
        puppetID=judgePuppet(ID)
        time.sleep(0)
        if puppetID is not 0:
            puppetList.append(puppetID)
    for each in puppetList:
        print each
        IDstr=IDstr+"\n"+str(each)
        t=open("c:/doubanData/puppetList.txt","a")
        t.write(IDstr)
        t.close()
    return puppetList


def judgePuppet(ID):
    url="http://m.douban.com/movie/people/"+ID+"/"
    br = mechanize.Browser()
    web=br.open(url)
    page=web.read()
    wish=re.findall("(?<=想看的电影.\()\d+",page)
    watched=re.findall("(?<=看过的电影.\()\d+",page)
    watching=re.findall("(?<=看的电视剧.\()\d+",page)
    reviews=re.findall("(?<=的影评.\()\d+",page)
    
    a=int(wish[0])
    b=int(watched[0])
    c=int(watching[0])
    d=int(reviews[0])
    total=a+b+c+d
    print total
    if total<=5:
        print "puppet detected"
        return ID
    elif total>5:
        return 0

savePuppetID()