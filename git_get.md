
### Get Notebook from github.com and other source.
通用的Notebook更新维护的工具。

#### URL地址列表。


```python
from pprint import *
```


```python
url_str = open("url_list.txt").read()
url_s
```




    '# Get Notebook from github.com and other source:\n\n# Pandas tutorial for new user.\nhttps://bitbucket.org/hrojas/learn-pandas.git\n\n# echo Pandas Cookbook.\nhttps://github.com/jvns/pandas-cookbook.git\n\n# Some Files for Finance Analysis.\nclone https://github.com/wy36101299/ipynb-file.git\n\n# Practical data analysis with Python\nhttps://leanpub.com/analyticshandbook\n\n# Mining-the-Social-Web-2nd-Edition\nhttps://github.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition.git\n\n# Biolab\nhttps://github.com/biolab/ipynb.git\n\n# Build a flask server for Jupyter.\nhttps://github.com/yhilpisch/ipynb-docker.git\n\n#\nhttps://github.com/yhilpisch/cloud-python.git\n\n#\nhttps://github.com/yhilpisch/py4fi.git\n\n#\nhttps://github.com/yhilpisch/dawp.git\n\n#\nhttps://github.com/yhilpisch/pydlon15.git\n\n#\nhttps://github.com/yhilpisch/dx.git\n\n# IPython notebooks used in Georgia Tech\'s CSE 6040: Computing for Data Analysis\nhttps://github.com/rvuduc/cse6040-ipynbs.git\n\n# Jupyter Notebook Tools for Sphinx\nhttps://github.com/spatialaudio/nbsphinx.git\n\n# A collection of Notebooks for using IPython effectively\nhttps://github.com/odewahn/ipynb-examples.git\n\n# aka "Bayesian Methods for Hackers"\nhttps://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers.git\n\n# /bokeh-tutorial-ipynb\nhttps://github.com/chdoig/bokeh-tutorial-ipynb.git\n\n# collection all kinds of ipynb\nhttps://github.com/OpenBookProjects/ipynb.git\n\n# Just a shared git repo for Social Graphs & Interaction\nhttps://github.com/timmevandermeer/ipynb.git\n\n# Neural Networks Training Jupyter Notebooks\nhttps://github.com/tmeits/ipynb.git\n\n# tensorflow-ipynb\nhttps://github.com/fujun-liu/tensorflow-ipynb.git\n\n# https://github.com/charlesjhlee/ml_ipynb.git\nhttps://github.com/charlesjhlee/ml_ipynb.git\n\n# Ipython Notebook Visuals\nhttps://github.com/bangadennis/ipynb_visuals.git\n\n# Canvas Widget for IPython Notebook https://github.com/Who8MyLunch/ipynb_widget_canvas\nhttps://github.com/Who8MyLunch/ipynb_widget_canvas.git\nhttps://github.com/Who8MyLunch/ipynb_widget_canvas.git\n\n# Copy of Udacity DL course ipynb files, and maybe some other stuff\nhttps://github.com/damienstanton/tensorflownotes.git\n\n# This is an ipynb in which we use simple logistic regression from Spark MLlib to train a sarcasm detector on comments from reddit.\nhttps://github.com/FranekJemiolo/SarcasmDetector.git\n\n# IPython project\nhttps://github.com/ipython/ipython.git\n\n# Topik project\nhttps://github.com/ContinuumIO/topik.git\n\n# scientific-python-lectures\nhttps://github.com/ContinuumIO/scientific-python-lectures.git\n\n# Continuum work from XDATA January 2016 Hackathon with U. S. Census Bureau\nhttps://github.com/ContinuumIO/xdata-2016-census.git\n\n#Analysis on Each Image\nhttps://github.com/ContinuumIO/image-analyzer.git\n\nhttps://github.com/ContinuumIO/tutorials.git\nhttps://github.com/ContinuumIO/PyDataAcademy.git\n\n'



### 分解字符串到名称和url。


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


### 如果已经存在，则git pull，否则git clone.


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
        print("\t Existed, git pull:",git_name)
        ! cd $git_name && git pull
    else:
        print("Git clone ......")
        ucmd = "git clone " + d["ugit"]
        #print(ucmd)
        ! $ucmd
print("Finished.")
```

    
     1 :	 learn-pandas. 
    	 https://bitbucket.org/hrojas/learn-pandas.git
    	 Existed, git pull: learn-pandas
    Already up-to-date.
    
     2 :	 Pandas Cookbook. 
    	 https://github.com/jvns/pandas-cookbook.git
    	 Existed, git pull: pandas-cookbook
    Already up-to-date.
    
     3 :	 Finance Analysis. 
    	 https://github.com/wy36101299/ipynb-file.git
    	 Existed, git pull: ipynb-file
    Already up-to-date.
    
     4 :	 Practical data analysis with Python 
    	 https://leanpub.com/analytics/handbook.git
    Git clone ......
    正克隆到 'handbook'...
    fatal: repository 'https://leanpub.com/analytics/handbook.git/' not found
    
     5 :	 Mining-the-Social-Web-2nd-Edition 
    	 https://github.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition.git
    	 Existed, git pull: Mining-the-Social-Web-2nd-Edition
    Already up-to-date.
    
     6 :	 Biolab 
    	 https://github.com/biolab/ipynb.git
    	 Existed, git pull: ipynb
    Already up-to-date.
    
     7 :	 Build a flask server for Jupyter. 
    	 https://github.com/yhilpisch/ipynb-docker.git
    	 Existed, git pull: ipynb-docker
    Already up-to-date.
    
     8 :	 IPython notebooks used in Georgia Tech's CSE 6040: Computing for Data Analysis 
    	 https://github.com/rvuduc/cse6040-ipynbs.git
    	 Existed, git pull: cse6040-ipynbs
    Already up-to-date.
    
     9 :	 Jupyter Notebook Tools for Sphinx 
    	 https://github.com/spatialaudio/nbsphinx.git
    Git clone ......
    正克隆到 'nbsphinx'...
    remote: Counting objects: 784, done.[K
    remote: Total 784 (delta 0), reused 0 (delta 0), pack-reused 784[K
    接收对象中: 100% (784/784), 217.71 KiB | 42.00 KiB/s, 完成.
    处理 delta 中: 100% (527/527), 完成.
    检查连接... 完成。
    
     10 :	 A collection of Notebooks for using IPython effectively 
    	 https://github.com/odewahn/ipynb-examples.git
    	 Existed, git pull: ipynb-examples
    Already up-to-date.
    
     11 :	 aka "Bayesian Methods for Hackers" 
    	 https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers.git
    	 Existed, git pull: Probabilistic-Programming-and-Bayesian-Methods-for-Hackers
    Already up-to-date.
    
     12 :	 /bokeh-tutorial-ipynb 
    	 https://github.com/chdoig/bokeh-tutorial-ipynb.git
    Git clone ......
    正克隆到 'bokeh-tutorial-ipynb'...
    remote: Counting objects: 253, done.[K
    remote: Compressing objects: 100% (90/90), done.[K
    ^C
    
     13 :	 collection all kinds of ipynb 
    	 https://github.com/OpenBookProjects/ipynb.git
    	 Existed, git pull: ipynb
    Already up-to-date.
    
     14 :	 Just a shared git repo for Social Graphs & Interaction 
    	 https://github.com/timmevandermeer/ipynb.git
    	 Existed, git pull: ipynb
    Already up-to-date.
    
     15 :	 Neural Networks Training Jupyter Notebooks 
    	 https://github.com/tmeits/ipynb.git
    	 Existed, git pull: ipynb
    Already up-to-date.
    
     16 :	 tensorflow-ipynb 
    	 https://github.com/fujun-liu/tensorflow-ipynb.git
    Git clone ......
    正克隆到 'tensorflow-ipynb'...
    remote: Counting objects: 7, done.[K
    remote: Total 7 (delta 0), reused 0 (delta 0), pack-reused 7[K
    展开对象中: 100% (7/7), 完成.
    检查连接... 完成。
    
     17 :	 https://github.com/charlesjhlee/ml_ipynb.git 
    	 https://github.com/charlesjhlee/ml_ipynb.git
    Git clone ......
    正克隆到 'ml_ipynb'...
    remote: Counting objects: 34, done.[K
    remote: Total 34 (delta 0), reused 0 (delta 0), pack-reused 34[K
    展开对象中: 100% (34/34), 完成.
    检查连接... 完成。
    
     18 :	 Ipython Notebook Visuals 
    	 https://github.com/bangadennis/ipynb_visuals.git
    Git clone ......
    正克隆到 'ipynb_visuals'...
    remote: Counting objects: 23, done.[K
    remote: Total 23 (delta 0), reused 0 (delta 0), pack-reused 23[K
    展开对象中: 100% (23/23), 完成.
    检查连接... 完成。
    
     19 :	 Canvas Widget for IPython Notebook https://github.com/Who8MyLunch/ipynb_widget_canvas 
    	 https://github.com/Who8MyLunch/ipynb_widget_canvas.git
    Git clone ......
    正克隆到 'ipynb_widget_canvas'...
    remote: Counting objects: 1141, done.[K
    remote: Total 1141 (delta 0), reused 0 (delta 0), pack-reused 1141[K
    接收对象中: 100% (1141/1141), 7.58 MiB | 127.00 KiB/s, 完成.
    处理 delta 中: 100% (776/776), 完成.
    检查连接... 完成。
    
     20 :	 Copy of Udacity DL course ipynb files, and maybe some other stuff 
    	 https://github.com/damienstanton/tensorflownotes.git
    Git clone ......
    正克隆到 'tensorflownotes'...
    remote: Counting objects: 24, done.[K
    remote: Total 24 (delta 0), reused 0 (delta 0), pack-reused 24[K
    展开对象中: 100% (24/24), 完成.
    检查连接... 完成。
    
     21 :	 Simple logistic regression from Spark MLlib to train a sarcasm detector on comments from reddit. 
    	 https://github.com/FranekJemiolo/SarcasmDetector.git
    Git clone ......
    正克隆到 'SarcasmDetector'...
    remote: Counting objects: 6, done.[K
    remote: Total 6 (delta 0), reused 0 (delta 0), pack-reused 6[K
    展开对象中: 100% (6/6), 完成.
    检查连接... 完成。
    
     22 :	 IPython project 
    	 https://github.com/ipython/ipython.git
    Git clone ......
    正克隆到 'ipython'...
    remote: Counting objects: 154141, done.[K
    remote: Compressing objects: 100% (37/37), done.[K
    ^C
    
     23 :	 Topik project 
    	 https://github.com/ContinuumIO/topik.git
    Git clone ......
    正克隆到 'topik'...
    remote: Counting objects: 3093, done.[K
    remote: Total 3093 (delta 0), reused 0 (delta 0), pack-reused 3093[K
    接收对象中: 100% (3093/3093), 1.82 MiB | 80.00 KiB/s, 完成.
    处理 delta 中: 100% (2079/2079), 完成.
    检查连接... 完成。
    
     24 :	 scientific-python-lectures 
    	 https://github.com/ContinuumIO/scientific-python-lectures.git
    Git clone ......
    正克隆到 'scientific-python-lectures'...
    remote: Counting objects: 790, done.[K
    remote: Total 790 (delta 0), reused 0 (delta 0), pack-reused 790[K
    接收对象中: 100% (790/790), 28.02 MiB | 34.00 KiB/s, 完成.
    处理 delta 中: 100% (489/489), 完成.
    检查连接... 完成。
    
     25 :	 Continuum work from XDATA January 2016 Hackathon with U. S. Census Bureau 
    	 https://github.com/ContinuumIO/xdata-2016-census.git
    Git clone ......
    正克隆到 'xdata-2016-census'...
    remote: Counting objects: 14, done.[K
    remote: Total 14 (delta 0), reused 0 (delta 0), pack-reused 14[K
    展开对象中: 100% (14/14), 完成.
    检查连接... 完成。
    
     26 :	 Analysis on Each Image 
    	 https://github.com/ContinuumIO/image-analyzer.git
    Git clone ......
    正克隆到 'image-analyzer'...
    remote: Counting objects: 217, done.[K
    remote: Total 217 (delta 0), reused 0 (delta 0), pack-reused 217[K
    接收对象中: 100% (217/217), 5.88 MiB | 219.00 KiB/s, 完成.
    处理 delta 中: 100% (126/126), 完成.
    检查连接... 完成。


### 保存到Markdown文件。


```python
flist = open("url_list.md","w+") 
flist.write(
"""
## IPython Notebook Tutorial and Skills open source...
##### by [openthings@163.com](http://my.oschina.net/u/2306127/blog?catalog=3420733), 2016-04.   
"""
) 
for d in url_list:
    flist.write("### " + d["uname"] + "\n")
    flist.write("[" + d["ugit"] + "]" + "(" + d["ugit"] + ")\n")
flist.close()
print("Writed url list to file: url_list.md")
```

    Writed url list to file: url_list.md


### 使用纯脚本完成。
%%!
echo "Get learn-pandas doc..."
if [ ! -d "learn-pandas" ]; then
    echo "Get new learn-pandas..."
    git clone https://bitbucket.org/hrojas/learn-pandas.git
    cd learn-pandas
else
    echo "pull update..."
    cd learn-pandas
    git pull
fi

```python

```
