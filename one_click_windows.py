import subprocess
import os
import webbrowser
current_file_path = os.path.abspath(__file__)

superior_path = os.path.dirname(current_file_path)
interface_path = os.path.join(superior_path, "main.py")
server_path = os.path.join(superior_path, "server.js")


# 启动 server.py
print("start server")
subprocess.Popen("start cmd /k node {}".format(server_path), shell=True)

#wait for server to start
import time
time.sleep(1)

# 启动 interface.py
print("start interface")
subprocess.Popen("start cmd /k python {}".format(interface_path), shell=True)


# 打开本地HTML文件
print("open html")
page_path = os.path.join(superior_path, "UIfrontPage/index.html")
webbrowser.open('file://' + page_path)