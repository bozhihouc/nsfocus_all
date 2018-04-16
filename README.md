# nsfocus

RSAS_html报表处理成excel

# 条件
> 需要导入第三方库xlwt库、BeautifulSoup库、lxml库
> pip install xlwt
> BeautifulSoup库:https://pypi.python.org/pypi/beautifulsoup4/4.6.0
> pip install lxml
> 导出的报告必须包含综合报表+主机报表
<br/>RSAS V6.0
<br/>执行python nsfocus_excel.py
<br/>会自行处理的的index.html文件
<br/>输出格式：受影响主机+风险等级+漏洞名称+漏洞描述+修复建议+CVE编号

#### 没有落实具体的版本，可能会有差异

### 20180303

### 20180416
> 感谢大佬指出 121行 修复建议
> 在mac+windows系统 测试通过，脚本正常运行