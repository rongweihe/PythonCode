
### **0、程序思路**

要实现把 md 格式的文件转换成 pdf，需要用到以下两个库。



1. markdown
2. wkhtmltopdf



直接把 md 转换成 pdf 的效果是非常不好的，所以我们可以先把 md 文件转换成 html 文件，然后在把 html 文件转换成 pdf。这样整体的效果就非常的好。



而上方的两个库就对应着把 md 转成 html，把 html 转成 pdf。所以我们首先要把这两个库进行安装。



### **1、md2html**

为了将 md 格式转换成 html 文件，我们需要用到 markdown 和 codecs 这两个库。

**1.1 Python-Markdown**

Python-Markdown 是 John Gruber 的 Markdown 的 Python 实现。利用这个库我们就可以很容易把 md 格式的文件转换成 html 文件。

安装方式「**pip install markdown**」

随后我们使用 markdown.markdown() 函数就可以读取 md 文件里的内容了。



**1.2 codecs**

在 md2html 函数中还用到了 codecs 这个库，这个库是用来保证文件读取的过程中，不出现编码的问题。你也可以把它理解成 open 函数，用来读取创建文件用的。



**1.3 完整代码**

```python
import markdown
import os
import codecs

head = """<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<style type="text/css">
code {
  color: inherit;
  background-color: rgba(0, 0, 0, 0.05);
}
</style>
</head>
<body>
"""

foot = """
</body>
</html>
"""
filepath = "E:/RZF/RenZhengfei-masterALL"
savepath = "E:/RZF/RenZhengfei-masterALL-html"
if not os.path.isdir(savepath):
    os.mkdir(savepath)
os.chdir(savepath)

i = 0
pathDir = os.listdir(filepath)
for allDir in pathDir:
    if (allDir == "pdf"):
        continue
    name = allDir
    print(name)

    os.chdir(filepath)
    fp1 = codecs.open(name, mode="r", encoding="utf-8")
    text = fp1.read()
    html = markdown.markdown(text)
    fp1.close()
    #print(html)

    fname = name.replace('md', 'html')

    #f2 = '%s.html' % (fname)
    os.chdir(savepath)
    fp2 = codecs.open(fname, "w", encoding="utf-8", errors="xmlcharrefreplace")
    fp2.write(head + html + foot)
    fp2.close()

print(i)
```



**整个代码的逻辑：**

利用 markdown 读取 md 文件，然后在用 codeces 创建新的 html 文件。最后注意的是：在开头定义好 html 头部和尾部的 css 代码，中间的内容用读取到的 md 内容进行填充。



### **2、 html2pdf**

**2.1 wkhtmltopdf**

wkhtmltopdf 是一个开源、简单而有效的命令行 shell 程序，它可以将任何 HTML （网页）转换为 PDF 文档或图像（jpg、png 等）。

我们首先需要去官网去下载对应的程序到本地环境中。

https://wkhtmltopdf.org/downloads.html

而在 Python 中我们要通过 pdfkit 这个库来调用 wkhtmltopdf，所以我们还要安装下 pdfkit 库。

直接使用「**pip install pdfkit**」即可安装。

**2.2 完整代码**

```python
import time
import pdfkit
import os

wk_path = 'E:/data/wkhtmltox/bin/wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=wk_path)

filepath = "E:/RZF/RenZhengfei-masterALL-html"
savepath = "E:/RZF/RenZhengfei-masterALL-pdf"
time1 = time.time()
pathDir = os.listdir(filepath)
for allDir in pathDir:
    if (allDir == "pdf"):
        continue
    name = allDir
    print(name)
    htmlpath=filepath+"\\"+name
    print(htmlpath)
    name = name.replace('html', 'pdf')
    os.chdir(savepath)
    pdfkit.from_url(htmlpath, name, configuration=config)

time2 = time.time()
print(str(time2 - time1)+" s")
```



### **3、合并多个pdf文件**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
   本脚本用来合并pdf文件，支持带一级子目录的
   每章内容分别放在不同的目录下，目录名为章节名
   最终生成的pdf，按章节名生成书签
'''
import os, sys, codecs
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import glob

def getFileName(filepath):
    '''获取当前目录下的所有pdf文件'''
    file_list = glob.glob(filepath+"/*.pdf")
    # 默认安装字典序排序，也可以安装自定义的方式排序
    # file_list.sort()
    return file_list

def get_dirs(filepath='', dirlist_out=[], dirpathlist_out=[]):
    # 遍历filepath下的所有目录
    for dir in os.listdir(filepath):
        dirpathlist_out.append(filepath + '\\' + dir)
    return dirpathlist_out

def merge_childdir_files(path):
    '''每个子目录下合并生成一个pdf'''
    dirpathlist = get_dirs(path)
    if len(dirpathlist) == 0:
        print("当前目录不存在子目录")
        sys.exit()
    for dir in dirpathlist:
        mergefiles(dir, dir)

def mergefiles(path, output_filename, import_bookmarks=False):
#遍历目录下的所有pdf将其合并输出到一个pdf文件中，输出的pdf文件默认带书签，书签名为之前的文件名
#默认情况下原始文件的书签不会导入，使用import_bookmarks=True可以将原文件所带的书签也导入到输出的pdf文件中
    merger=PdfFileMerger()
    filelist=getFileName(path)
    if len(filelist)==0:
        print("当前目录及子目录下不存在pdf文件")
        sys.exit()
    for filename in filelist:
        f=codecs.open(filename,'rb')
        file_rd=PdfFileReader(f)
        short_filename=os.path.basename(os.path.splitext(filename)[0])
        if file_rd.isEncrypted==True:
            print('不支持的加密文件：%s'%(filename))
            continue
       merger.append(file_rd,bookmark=short_filename,import_bookmarks=import_bookmarks)
        print('合并文件：%s'%(filename))
        f.close()
    #out_filename=os.path.join(os.path.abspath(path),output_filename)
    merger.write(output_filename+".pdf")
    print('合并后的输出文件：%s'%(output_filename))
    merger.close()

if __name__ == "__main__":
    # 每个章节一个子目录，先分别合并每个子目录文件为一个pdf，然后再将这些pdf合并为一个大的pdf，这样做目的是想生成每个章节的书签
    # 1.指定目录
    # 原始pdf所在目录
    path = "E:\RZF\RenZhengfei-master\ALL-pdf"
    # 输出pdf路径和文件名
    output_filename = "E:\RZF\RenZhengfei-master"

    # 2.生成子目录的pdf
    # merge_childdir_files(path)

    # 3.子目录pdf合并为总的pdf
    mergefiles(path, output_filename)
```



整个程序一目了然，把 wk_path 修改成你自己的 wkhtmltopdf 安装路径。file_path 是你的 html 文件路径，而 save_path 就是你 pdf 文件保存的地方。



### **4、总结**

整个过程用到了两个函数文件，文章已经把所有的源码全部贴了出来，大家复制到本地就可以使用了，记得把相应的库安装好。



参考：<https://www.cnblogs.com/hankleo/p/10911810.html>
