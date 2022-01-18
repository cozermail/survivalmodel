
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

