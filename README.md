
### windows系统环境下直接运行8001startup.bat
### 启动成功后浏览器打开 （运行窗口不要关闭）
http://127.0.0.1:8001/generate
http://localhost:8001/generate
http://本机ip地址:8001/generate 例如：http://192.168.1.156:8001/generate
-  查看本机ip【win键 + R】 输入 cmd ，输入指令 ipconfig 。
   看到 IPv4 地址·····192.168.1.156
### 手机打开该网址
- #### 手机与电脑在同一局域网下
- #### 只能通过 http://本机ip地址:8001/generate 打开
### --------------------------------------------------------------------------
### 如果需要修改程序，需要重新进行打包才能运行。

### 打包需要修改manage.spec
- #### 将下面的【pathex】【datas】属性改为当前项目的绝对地址,即manage.spec所在的地址
```
pathex=['E:\\PythonCode\\survivalmodel'], 

datas=[(r'E:\PythonCode\survivalmodel\generateapp\templates', r'.\generateapp\templates'),
             (r'E:\PythonCode\survivalmodel\static\static_root', r'.\static\static_root'),
             (r'E:\PythonCode\survivalmodel\generateapp\data', r'./generateapp\data')],
             
```
- #### 若没有新增文件，则修改后在manage.spec所在目录下运行命令
<p style="color: red">注意：.\manage.spec 其中.\为Powershell窗口，cmd窗口不加.\ </p>
```
pyinstaller .\manage.spec --noconfirm
```
- #### 提示pyinstall 不是可识别命令则，去搜索一下，安装一下这个命令。如果有pip命令则直接运行
```
pip install pyinstaller==3.6
```

- #### 成功安装命令后再进行 pyinstaller ./manage.spec 进行打包。
- #### 打包成功后还需要复制【dist\manage\lib\site-packages\sklearn】下的.libs文件复制到【dist\manage\sklearn】下

- #### 然后重新点击运行8001startup.bat

- ### 新增静态文件
- #### 将静态文件新增在项目项目【非dist】目录内的【static】执行
```
python manage.py collectstatic
```
然后再执行打包命令
```
pyinstaller .\manage.spec --noconfirm
```




# 在linux系统上配置部署django

- 需要python和pip
  这里用的阿里云轻量服务器包含python3.6，pip9.0.1
  **默认命令为python3和pip3**
<p>

- 将django项目压缩成zip放置在linux上自定义路径
  **/project/survivalmodel/survivalmodel.zip**
  进行解压
```sh
[survivalmodel]# unzip survivalmodel.zip
```


- 在 **manage.py**所在路径下运行命令，若不能启动，缺啥补啥
```sh
python3 manage.py runserver --noreload 0.0.0.0:8001
```

- 补充 **django**
```sh
pip3 install Django==2.0.0
```

- 补充 **pandas**
```sh
pip3 install pandas==0.24.2
```

- 补充 **tensorflow**
```sh
pip3 install tensorflow==1.14.0
```

- 如果 **tensorflow** 下载失败，出现 **Command “python setup.py egg_info” failed** ，先升级 **setuptools** 然后再补充 **tensorflow** 
```sh
python3 -m pip install --upgrade --force pip
pip install setuptools==33.1.1
pip3 install tensorflow==1.14.0
```

- 补充 **matplotlib**
```sh
pip3 install matplotlib==3.0.3
```

- 补充 **lifelines**
```sh
pip3 install lifelines==0.14.6
```

- 补充 **supersmoother**
```sh
pip3 install supersmoother==0.4
```

- 补充 **sklearn** 
```sh
pip3 install sklearn==1.0.2
```

- ## 最后重新启动前需要先配置一下 settings.py

  ALLOWED_HOSTS = ['127.0.0.1','localhost',<span style="color: red;">'服务器ip'</span>]

- ### 直接启动
```sh
python3 manage.py runserver --noreload 0.0.0.0:8001
```

- ### 隐形启动
```sh
nohup python3 manage.py runserver --noreload 0.0.0.0:8001 >nohup.out 2>&1 &
tail -f nohup.out
```

- ### 可以编辑两个shell脚本start 和 stop 进行控制
start.sh  
```sh
ps -aux | grep python|xargs kill -9
```
stop.sh
```sh
nohup python3 manage.py runserver --noreload 0.0.0.0:8001 >nohup.out 2>&1 &

tail -f nohup.out
```


### 依赖的版本
```sh
setup(name=pkg_name,
    version=__version__,
    description='Deep cox proportional hazards model implemented by tensorflow framework and survival analysis.',
    keywords = "survival analysis, deep learning, cox regression, tensorflow",
    url='https://github.com/liupei101/TFDeepSurv',
    author='Pei Liu',
    author_email='yuukilp@163.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
    ],
    packages = find_packages(),
    python_requires=">=3.5",
    install_requires=[
        'tensorflow>=1.14.0, <2.0.0',
        'pandas>=0.24.2',
        'numpy>=1.14.5',
        'matplotlib>=3.0.3',
        'lifelines>=0.14.6',
        'scikit-learn'
    ],
    include_package_data=True,
)
```

# 在windows上部署django

- 部署上跟**linux**一模一样，使用对应的**python3.6**版本，**pip9.0.1**版本，安装对应依赖。

- 启动命令也一样。
启动脚本：start.bat
```bat
python manage.py runserver --noreload 0.0.0.0:8001
```

- 也可以使用 **pyinstaller** 命令打包成exe文件运行。
打包脚本: package.bat
```bat
python manage.py collectstatic --noconfirm

pyinstaller .\manage.spec --noconfirm

md .\dist\manage\sklearn\.libs
## 最后一个copy在可能不需要使用，有些打包会包括其内容
copy .\dist\manage\lib\site-packages\sklearn\.libs\* .\dist\manage\sklearn\.libs
```

启动脚本：start.bat
```bat
cd ./dist/manage/

manage.exe runserver --noreload 0.0.0.0:8001
```

