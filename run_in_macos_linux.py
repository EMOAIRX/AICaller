import subprocess
import os
import webbrowser

current_file_path = os.path.abspath(__file__)

superior_path = os.path.dirname(current_file_path)
interface_path = os.path.join(superior_path, "main.py")
server_path = os.path.join(superior_path, "server.js")
page_path = os.path.join(superior_path, "UIfrontPage/index.html")

print(interface_path)
print(server_path)
import time
subprocess.Popen(['osascript', '-e', 'tell app "Terminal" to do script "node \'{}\'"'.format(server_path)])
time.sleep(1)
webbrowser.open('file://' + page_path)
subprocess.Popen(['osascript', '-e', 'tell app "Terminal" to do script "python \'{}\'"'.format(interface_path)])

# 打开本地HTML文件

