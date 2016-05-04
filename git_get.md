
# Get Notebook from github.com and other source.
by [openthings@163.com](http://my.oschina.net/u/2306127/blog?catalog=3420733), 2016-04.  

### 通用的Notebook更新维护的工具。
* 原始URL列表保存在文本文件git_list.txt中。
* git_list.txt转为git_list.md，在GitBook中使用。
* git_list.txt转为git_list.ipynb，在Jupyter中使用。


```python
from pprint import *
```

#### URL地址列表读入字符串变量中。
#### <font color="red">注意，为了避免太长，只显示了前面指定个数的字符。</font>


```python
url_str = open("git_list.txt").read()
print(url_str[0:300] + "\n\n......")
```

    # Get Notebook from github.com and other source:
    
    # Pandas tutorial for new user.
    https://bitbucket.org/hrojas/learn-pandas.git
    
    # echo Pandas Cookbook.
    https://github.com/jvns/pandas-cookbook.git
    
    # Some Files for Finance Analysis.
    clone https://github.com/wy36101299/ipynb-file.git
    
    # Practical dat
    
    ......


#### 分解字符串到名称和url。


```python
url_line = url_str.split("#")

url_list = []
for url in url_line:
    url2 = url.strip().split("\n")
    if len(url2)>1:
        uname = url2[0]
        ugit = url2[1]
        url_dict = {"uname":uname,"ugit":ugit}
        url_list.append(url_dict)
        
print("Total:",len(url_list))
pprint(url_list[0:3])
        #print(uname,"\n",ugit)
```

    Total: 26
    [{'ugit': 'https://bitbucket.org/hrojas/learn-pandas.git',
      'uname': 'Pandas tutorial for new user.'},
     {'ugit': 'https://github.com/jvns/pandas-cookbook.git',
      'uname': 'echo Pandas Cookbook.'},
     {'ugit': 'clone https://github.com/wy36101299/ipynb-file.git',
      'uname': 'Some Files for Finance Analysis.'}]


## 保存到Markdown文件。


```python
flist = open("git_list.md","w+") 
flist.write(
"""
## IPython Notebook Tutorial and Skills open source...
##### by [openthings@163.com](http://my.oschina.net/u/2306127/blog?catalog=3420733), 2016-04.   
"""
) 
for d in url_list:
    flist.write("##### " + d["uname"] + "\n")
    flist.write("[" + d["ugit"] + "]" + "(" + d["ugit"] + ")\n")
flist.close()
print("Writed url list to file: url_list.md")
```

    Writed url list to file: url_list.md


## 抓取git库中文件到本地。如果已经存在，则git pull，否则git clone.
** <font color="red">使用了IPython的！魔法操作符来执行shell操作。</font>**


```python
import os
import os.path

index = 0
for d in url_list:
    index += 1
    print("\n",index,":\t",d["uname"],"\n==>>\t",d["ugit"])

    git_path = os.path.split(d["ugit"])
    git_name = git_path[1].split(".")[0]
    #print(git_name)
    
    if os.path.exists(git_name):
        print("\t Existed, git pull:",git_name," ...")
        ! cd $git_name && git pull
    else:
        print("Git clone ......")
        ucmd = "git clone " + d["ugit"]
        #print(ucmd)
        ! $ucmd
print("Finished.")
```

    
     1 :	 Pandas tutorial for new user. 
    ==>>	 https://bitbucket.org/hrojas/learn-pandas.git
    	 Existed, git pull: learn-pandas
    Already up-to-date.
    
     2 :	 echo Pandas Cookbook. 
    ==>>	 https://github.com/jvns/pandas-cookbook.git
    	 Existed, git pull: pandas-cookbook
    Already up-to-date.
    
     3 :	 Some Files for Finance Analysis. 
    ==>>	 clone https://github.com/wy36101299/ipynb-file.git
    	 Existed, git pull: ipynb-file
    Already up-to-date.
    
     4 :	 Practical data analysis with Python 
    ==>>	 https://leanpub.com/analyticshandbook
    Git clone ......
    正克隆到 'analyticshandbook'...
    fatal: repository 'https://leanpub.com/analyticshandbook/' not found
    
     5 :	 Mining-the-Social-Web-2nd-Edition 
    ==>>	 https://github.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition.git
    	 Existed, git pull: Mining-the-Social-Web-2nd-Edition
    Already up-to-date.
    
     6 :	 Biolab 
    ==>>	 https://github.com/biolab/ipynb.git
    	 Existed, git pull: ipynb
    Already up-to-date.
    
     7 :	 Build a flask server for Jupyter. 
    ==>>	 https://github.com/yhilpisch/ipynb-docker.git
    	 Existed, git pull: ipynb-docker
    Already up-to-date.
    
     8 :	 IPython notebooks used in Georgia Tech's CSE 6040: Computing for Data Analysis 
    ==>>	 https://github.com/rvuduc/cse6040-ipynbs.git
    	 Existed, git pull: cse6040-ipynbs
    Already up-to-date.
    
     9 :	 Jupyter Notebook Tools for Sphinx 
    ==>>	 https://github.com/spatialaudio/nbsphinx.git
    	 Existed, git pull: nbsphinx
    Already up-to-date.
    
     10 :	 A collection of Notebooks for using IPython effectively 
    ==>>	 https://github.com/odewahn/ipynb-examples.git
    	 Existed, git pull: ipynb-examples
    Already up-to-date.
    
     11 :	 aka "Bayesian Methods for Hackers" 
    ==>>	 https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers.git
    	 Existed, git pull: Probabilistic-Programming-and-Bayesian-Methods-for-Hackers
    Already up-to-date.
    
     12 :	 /bokeh-tutorial-ipynb 
    ==>>	 https://github.com/chdoig/bokeh-tutorial-ipynb.git
    Git clone ......
    正克隆到 'bokeh-tutorial-ipynb'...
    remote: Counting objects: 253, done.[K
    remote: Compressing objects: 100% (90/90), done.[K
    remote: Total 253 (delta 161), reused 253 (delta 161), pack-reused 0[K
    接收对象中: 100% (253/253), 49.82 MiB | 599.00 KiB/s, 完成.
    处理 delta 中: 100% (161/161), 完成.
    检查连接... 完成。
    
     13 :	 collection all kinds of ipynb 
    ==>>	 https://github.com/OpenBookProjects/ipynb.git
    	 Existed, git pull: ipynb
    Already up-to-date.
    
     14 :	 Just a shared git repo for Social Graphs & Interaction 
    ==>>	 https://github.com/timmevandermeer/ipynb.git
    	 Existed, git pull: ipynb
    Already up-to-date.
    
     15 :	 Neural Networks Training Jupyter Notebooks 
    ==>>	 https://github.com/tmeits/ipynb.git
    	 Existed, git pull: ipynb
    Already up-to-date.
    
     16 :	 tensorflow-ipynb 
    ==>>	 https://github.com/fujun-liu/tensorflow-ipynb.git
    	 Existed, git pull: tensorflow-ipynb
    Already up-to-date.
    
     17 :	 https://github.com/charlesjhlee/ml_ipynb.git 
    ==>>	 https://github.com/charlesjhlee/ml_ipynb.git
    	 Existed, git pull: ml_ipynb
    Already up-to-date.
    
     18 :	 Ipython Notebook Visuals 
    ==>>	 https://github.com/bangadennis/ipynb_visuals.git
    	 Existed, git pull: ipynb_visuals
    Already up-to-date.
    
     19 :	 Canvas Widget for IPython Notebook https://github.com/Who8MyLunch/ipynb_widget_canvas 
    ==>>	 https://github.com/Who8MyLunch/ipynb_widget_canvas.git
    	 Existed, git pull: ipynb_widget_canvas
    Already up-to-date.
    
     20 :	 Copy of Udacity DL course ipynb files, and maybe some other stuff 
    ==>>	 https://github.com/damienstanton/tensorflownotes.git
    	 Existed, git pull: tensorflownotes
    Already up-to-date.
    
     21 :	 This is an ipynb in which we use simple logistic regression from Spark MLlib to train a sarcasm detector on comments from reddit. 
    ==>>	 https://github.com/FranekJemiolo/SarcasmDetector.git
    	 Existed, git pull: SarcasmDetector
    Already up-to-date.
    
     22 :	 IPython project 
    ==>>	 https://github.com/ipython/ipython.git
    Git clone ......
    正克隆到 'ipython'...
    remote: Counting objects: 154141, done.[K
    remote: Compressing objects: 100% (37/37), done.[K
    error: RPC failed; curl 56 GnuTLS recv error (-9): A TLS packet with unexpected length was received.
    fatal: The remote end hung up unexpectedly
    fatal: 过早的文件结束符（EOF）
    fatal: index-pack failed
    
     23 :	 Topik project 
    ==>>	 https://github.com/ContinuumIO/topik.git
    	 Existed, git pull: topik
    Already up-to-date.
    
     24 :	 scientific-python-lectures 
    ==>>	 https://github.com/ContinuumIO/scientific-python-lectures.git
    	 Existed, git pull: scientific-python-lectures
    Already up-to-date.
    
     25 :	 Continuum work from XDATA January 2016 Hackathon with U. S. Census Bureau 
    ==>>	 https://github.com/ContinuumIO/xdata-2016-census.git
    	 Existed, git pull: xdata-2016-census
    Already up-to-date.
    
     26 :	 Analysis on Each Image 
    ==>>	 https://github.com/ContinuumIO/image-analyzer.git
    	 Existed, git pull: image-analyzer
    Already up-to-date.
    Finished.



```python

```
