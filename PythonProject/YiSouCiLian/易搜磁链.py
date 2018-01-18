# -*- coding: utf-8 -*-
#功能:根据输入的关键字搜索下载磁力链接
#技术相关:wxPython+BeautifulSoup+request
#Author:水山
#联系方式:shui_shan@foxmail.com


import wx
import threading
import base64,os,time
from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup



#程序基本信息
AboutStr="易搜磁链\n\nVersion  :  1.0\n\n联系方式 :  shui_shan@foxmail.com\n\n                                                            by水山"


class SSCLFrame(wx.Frame):
    
    #创建界面
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,"易搜磁链",pos=(1920/2-200,1080/2-150),size=(400,300),style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX))
        self.panel=wx.Panel(self)
        #self.icon=wx.Icon('wm.ico',wx.BITMAP_TYPE_ICO)
        #self.SetIcon(self.icon)
        self.effectText=wx.StaticText(self.panel,-1,"搜索并下载您想要的影视资源磁力链接",(70,12),(250,-1),wx.ALIGN_CENTER)
        self.AboutBtn=wx.Button(self.panel,label="关于",pos=(296,232))
        self.button=wx.Button(self.panel,label="搜索下载",pos=(250,47))
        self.textCrtl=wx.TextCtrl(self.panel,-1,"输入关键词",pos=(50,50),size=(175,-1))
        self.log1=wx.StaticText(self.panel,-1,"",(40,110),(300,-1),wx.ALIGN_CENTER)
        self.log2=wx.StaticText(self.panel,-1,"",(40,145),(300,-1),wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON,self.GetAndUse,self.button)
        self.Bind(wx.EVT_BUTTON,self.About,self.AboutBtn)

    #通过弹出对话框来展示基本信息
    def About(self,event):
        global AboutStr
        dlg=wx.MessageDialog(None,AboutStr,'易搜磁链',style=wx.OK,pos=wx.DefaultPosition)
        dlg.ShowModal()
        dlg.Destroy()

    #响应按钮事件,利用多线程解决GUI无响应
    def GetAndUse(self,event):
        global t1
        EnterStr=self.textCrtl.GetValue()
        if not t1.is_alive():
            t1=threading.Thread(target=self.main,args=(EnterStr,))
            t1.start()
    #输出简单的LOG
    def PLog1(self,_Str):
        self.log1.SetLabel(_Str)
    
    def PLog2(self,_Str):
        self.log2.SetLabel(_Str)


    #爬虫部分
    def UseKeySearchCLLJ(self,key):
        key=str(key)
        if not key:
            self.PLog1("请输入点什么!")
            self.PLog2("")
            return 
        uniKey=key.encode('utf-8')
        keyBase64=base64.b64encode(uniKey)
        keyStr=self.BToStrANDRemoveTrust(keyBase64)
        keyStr=keyStr.replace("=",'')
        keyStr=keyStr.replace("+","-")
        keyStr=keyStr.replace("/","_")
        baseUrl="http://btdiggs.com/search/"+keyStr+"/1/0/0.html"
        bsObj=self.UseBeauSoup(baseUrl)
        if not bsObj:
            return
        forlinks=bsObj.find("div",{"class":"list"})
        if not forlinks:
            self.PLog1("")
            self.PLog2("抱歉，没有找到与关键词<"+key+">相关的结果!")
            return
        fortext=forlinks.findAll("dt")
        if not fortext:
            self.PLog1("")
            self.PLog2("抱歉，没有找到与关键词"+key+"相关的结果!")
            return
        links=forlinks.findAll("a",{"style":"color:#777;"})
        file=open(key+'磁力链接.txt','w')
        file.write(key+"的磁力链接已经全部找到,只需要复制其中一条然后打开迅雷就可以开始下载了\n\n")
        file.write("排序规则:关键字相关性\n\n")
        i=0
        try:
            for link in links:
                _name=fortext[i].get_text()
                _name=''.join(_name.split())
                file.write("片名:\n"+_name+"\n")
                file.write("磁力链接:\n")
                _href=link.attrs['href']
                _href=_href.strip()
                file.write(_href+"\n\n\n\n");
                i=i+1
            self.PLog1("")
            self.PLog2("磁力链接下载完毕,保存在当前目录的txt文件中")
        finally:
            file.close()
            return
    
    #使用BeauifulSoup的简单封装
    def UseBeauSoup(self,url):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        req=Request(url,headers=headers)
        try:
            html = urlopen(req,timeout=5)
        except :
            self.PLog1("")
            self.PLog2("此次网络请求失败,请重试!")
            return None
        bsObj = BeautifulSoup(html,"html.parser")
        return bsObj
    
    #清洗字符串
    def BToStrANDRemoveTrust(self,b):
        b=str(b)
        b=b.replace('b\'','')
        b=b.replace('\'','')
        return b

    def main(self,key=''):
        if  key : 
            self.PLog1("下载中...")
            #self.PLog2("(如果等待时间过长,可能是此次请求未响应,请重新启动)")
            self.PLog2("")
        self.UseKeySearchCLLJ(key)


if __name__=='__main__':
    t1=threading.Thread(target=None,args=())
    app=wx.App(redirect=False)
    frame=SSCLFrame(parent=None,id=-1)
    frame.Show()
    app.MainLoop()