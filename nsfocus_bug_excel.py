#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/28 13:41
# @Author  : 852782749@qq.com
# @File    : nsfocus_bug_excel.py
# @Software: PyCharm

'''将文件放在要处理的绿盟科技漏洞扫描综合报表内，自动识别index.html文件，会生成三个文件
在当前目录下执行python nsfocus_bug_excel.py
需要导入第三方库xlwt库、BeautifulSoup库、lxml库
'''
import time
'''time.strftime('%Y-%m-%d.xls')'''
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit('\n[!]python html库——BeautifulSoup导入错误;请执行 pip install BeautifulSoup安装!')
import re
import lxml
'''
脚本是用来获取绿盟漏洞扫描设备的html版本报告的漏洞信息的，包括主机，漏洞名称，漏洞描述，修复建议，CVE编号
#buglv = ['high','middle','low']分别对应高中低三种类型的漏洞。
'''
soup = BeautifulSoup(open('index.html'),"lxml")
#print soup.contents
data = str(soup.find_all("div",{"class":'report_content'})).decode('unicode_escape')
#删除空格、换行等特殊字符
data = filter(lambda x:x not in ['\n','\r',' ','\t'],data)
#print data
#共有8个此处DIV，每处对应一章节
#使用split分出每一章节
data_list=data.split("report_content")
#print data_list[4]
data_bug_list = data_list[4]
#print data_bug_list
buglv = ['high','middle','low']
#buglv = ['high']

def bug_level(bug_lv):
    #定义获取漏洞list(漏洞名称,详细信息,解决方案,CVE编号等,)
    # 正则bug_lv为风险等级分为high,middle,low分别对应风险等级高中低;
    # data_bug_list为全局变量，值是漏洞数据;
    #返回bug_r_list为匹配到的漏洞数据list
    bug_r = r'<trclass="\w*?vuln_'+bug_lv+'".*?</td></tr></table></td></tr>'
    bug_r_re = re.compile(bug_r)
    bug_r_list = re.findall(bug_r_re, data_bug_list)
    return bug_r_list
def vnln_hosts(bug_hosts):
    # 匹配受影响主机
    #data_host实参是漏洞信息中受影响主机
    # bug_host_r_list是返回的受影响主机
    bug_host_r = r'host/(.*?).html'
    bug_host_r_re = re.compile(bug_host_r)
    bug_host_r_list = re.findall(bug_host_r_re, bug_hosts)
    return bug_host_r_list
def bug_main(bug_bug):
    index =1
    '''time.strftime('%Y-%m-%d-%h-%s.xls')'''
    file = xlwt.Workbook()
    # excel 第一行数据
    excel_headDatas = [u'受影响主机', u'漏洞等级', u'漏洞名称', u'漏洞描述', u'修复建议', u'CVE编号']
    table = file.add_sheet(u'漏洞数据', cell_overwrite_ok=True)
    fist = 0
    for data in excel_headDatas:
        table.write(0, fist, data)
        fist += 1
    for i in range(len(bug_bug)):
#    for i in range(1):
        #print u'当前进行第%s个' %(i+1)
        bug_n_r = r'trclass=".*?vuln_(.*?)"onclick.*?<spanstyle="color:.*?">(.*?)</span><!--<span'
        bug_n_re = re.compile(bug_n_r)
        bug_n_list = re.findall(bug_n_re, bug_bug[i])

        bug_x_r = u'<!--<span.*?<th>详细描述</th><td>(.*?)</td></tr>'
        bug_x_re = re.compile(bug_x_r)
        bug_x_list = re.findall(bug_x_re,bug_bug[i])

        bug_j_r = u'解决办法</th><td>(.*?)</td></tr>'
        bug_j_re = re.compile(bug_j_r)
        bug_j_list = re.findall(bug_j_re,bug_bug[i])

        bug_c_r = r'target="_blank">(CVE.*?)</a></td></tr>'
        bug_c_re = re.compile(bug_c_r)
        bug_c_list = re.findall(bug_c_re,bug_bug[i])
        for hs in range(len(vnln_hosts(bug_bug[i]))):
            if len(bug_n_list)!=0:
                bug_lv = bug_n_list[0][0]
                bug_name = bug_n_list[0][1]
            else:
                bug_lv = ''
                bug_name = ''
            if len(bug_x_list)!=0:
                bug_xin = bug_x_list[0]
            else:
                bug_xin = u'无'
            if len(bug_j_list)!=0:
                bug_jie = bug_j_list[0]
            else:
                bug_jie = u'无'
            if len(bug_c_list)!=0:
                #print bug_c_list
                if 'blank' in bug_c_list[0]:
                    #print bug_c_list
                    cvem = '>'+bug_c_list[0]+'</a>'
                    #print cvem
                    bug_cve_r = r'>(CVE.*?)</a>'
                    bug_cve_re = re.compile(bug_cve_r)
                    bug_cve_list = re.findall(bug_cve_re,cvem)
                    #print bug_cve_list
                    #print len(bug_cve_list)
                    bug_cve = ','.join(bug_cve_list)
                    #print bug_cve
                else:
                    #print bug_c_list
                    bug_cve = bug_c_list[0]
            else:
                bug_cve = u'无'
            #print vnln_hosts(bug_bug[i])[hs]+'Analogy'+bug_lv+bug_name+'Analogy'+bug_xin+'Analogy'+bug_jie+'Analogy'+bug_cve
            #print(vnln_hosts(bug_bug[i])[hs]+bug_lv+bug_name+bug_xin+bug_jie+bug_cve+'\n')
            test_list = []
            test_list.append(vnln_hosts(bug_bug[i])[hs])
            test_list.append(bug_lv)
            test_list.append(bug_name)
            test_list.append(bug_xin)
            test_list.append(bug_jie)
            test_list.append(bug_cve)
            #print test_list
            for j in range(len(test_list)):
                table.write(index,j,test_list[j])
                print index
            index +=1
    file.save(time.strftime('%Y-%m-%d-%H-%S.xls'))
    time.sleep(2)

def main():
    for bug in range(len(buglv)):
        bug_main(bug_level(buglv[bug]))
if __name__ == '__main__':
    main()
