# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:41:56 2017

@author: Administrator
"""

 
import urllib
import urllib2
import re
import time
 
class Spider:
 
    def __init__(self):
        self.siteURL = 'https://hotornot.com/dating/china/kwantung/guangzhou/page-'
 
    def getPage(self,pageIndex):
        url = self.siteURL + str(pageIndex) +'/'
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    def getimginfo(self,imgurl):
        info=[]
        request1 = urllib2.Request(imgurl)
        response1 = urllib2.urlopen(request1)
        img = response1.read().decode('utf-8')
        pattern1 = re.compile('<div class="score-user.*?<b class="scale.*?>(.*?)</b>.*?<div class="inline score.*?<b>(.*?)</b>.*?<b>(.*?)</b>.*?',re.S)
        pattern2 = re.compile('<meta itemprop="image" content="(.*?)wm_id.*?profile:gender" content="(.*?)"',re.S)
        imgsrc = re.findall(pattern2,img)
        items=re.findall(pattern1,img)
        if items==[]:
            print 'Invalid image...'
            pass
        else:
            info.append(items[0][0])     #分数
            info.append(items[0][1])     #投票人数
            info.append(items[0][2])     #喜欢人数
            info.append(imgsrc[0][1])    #男？女？
            info.append(imgsrc[0][0])    #图像地址
            print 'Scraping...'  
        return info

    def org2saveinfo(self,item,imgurl):
        userid=imgurl.split('/')[4]   #分开url获取图的id
        if item==[]:
            pass
        else:
            item.insert(0,userid)       #用户id
        return item
    
    def save(self,imginfo):
        file=open('imginfo-guangzhou.txt','a')   #保存图像信息
        file.write(str(imginfo))
        file.write("\n")
        file.close()
        
    def getpageContents(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<div class="user-card__img".*?<a href="(.*?)"',re.S)
        imgurls = re.findall(pattern,page)
        print 'The',i,'th page is searching, ',len(imgurls),' images is scraping.'
        for imgurl in imgurls:
            print imgurl
            item=self.getimginfo(imgurl)
            imginfo=self.org2saveinfo(item,imgurl)
            if imginfo==[]:
                pass
            else:
                imgname='F:\hotdata/hotornot-guangzhou/'+str(imginfo[0])+'.jpg'
                urllib.urlretrieve(imginfo[5],imgname)     #下载并保存图片
                self.save(imginfo)

spider = Spider()               
for i in range(4,200):
    spider.getpageContents(i)
    time.sleep(1)
