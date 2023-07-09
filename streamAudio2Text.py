# -*- coding:utf-8 -*-
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import sys

import pyaudio
import requests
import json
import queue

import gevent
from gevent import Greenlet

flag = 0
result = ""
before = "EMPTY"
timer = None

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

# 配置PyAudio
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
rate = 16000
record_seconds = 5

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo":1,"vad_eos":60000, "ptt":0}


    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


from keys import kdxf_APPID, kdxf_APISecret, kdxf_APIKey
wsParam = Ws_Param(kdxf_APPID, kdxf_APIKey, kdxf_APISecret)
    
import threading
import json

flag = 0
result = ""
timer = None

def on_message_wrapper(on_message_func):
    def para(dealerchain):
        def wrapper(ws, message):
            on_message_func(ws, message, dealerchain)
        return wrapper
    return para

nlpjob,ttsjob,audiojob,textstream,audioQueue = None,None,None,None,None
@on_message_wrapper
def on_message(ws, message , dealerchain):
    print("on_message", message , type(message) , len(message) )
    global flag, result, timer
    global nlpjob,ttsjob,audiojob,textstream,audioQueue
    try:
        code = json.loads(message)["code"]
        sid = json.loads(message)["sid"]
        if code != 0:
            errMsg = json.loads(message)["message"]
            print(f"sid:{sid} call error:{errMsg} code is:{code}")

        else:
            data = json.loads(message)["data"]["result"]["ws"]
            str_tmp = ""
            for i in data:
                for w in i["cw"]:
                    str_tmp += w["w"]
            if str_tmp == "":
                result = ""
            if str_tmp != "":
                result += str_tmp
                print("str_tmp = ", str_tmp)
                if len(result) > 3:
                    print('result = ', result)
                    print('time = ', time.time())
                    dealerchain.put(result)
                    result = ""
            


    except Exception as e:
        print(f"receive msg, but parse exception: {e}")


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,a,b):
    print("### closed ###")


# 收到websocket连接建立的处理，开始录音
def on_open(ws):
    def run(*args):
        frameSize = 1280  # 每一帧的音频大小
        intervel = 0.04  # 发送音频间隔(单位:s)
        status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

        #录音开始
        # 创建PyAudio对象
        p = pyaudio.PyAudio()

        # 打开麦克风输入流
        stream = p.open(format=sample_format,
                channels=channels,
                rate=rate,
                frames_per_buffer=chunk,
                input=True)

        print("正在录音...")
        # 开始录音并发送音频数据到语音识别API
        # 从麦克风读取音频数据
        data = stream.read(chunk)
        # 将音频数据转换为Base64编码的字符串
        audio_data = base64.b64encode(data)

        while True:
            import numpy as np
            data = stream.read(chunk)
            audio_data = base64.b64encode(data)
    # 文件结束（录音时间到达record_seconds秒），注意需要添加sys.exit()，否则线程可能无法正常退出
            if not data:
                sys.exit()
    # 第一帧处理
    # 发送第一帧音频，带business 参数
    # appid 必须带上，只需第一帧发送
            if status == STATUS_FIRST_FRAME:
                    d = {"common": wsParam.CommonArgs, "business": wsParam.BusinessArgs, "data": {"status": 0, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(data), 'utf-8'),
                                      "encoding": "raw"}}
                    d = json.dumps(d)
                    try:
                        ws.send(d)
                    except Exception as e:
                        print("WebSocket error. Reconnecting..")
                        sys.exit()
                        
                        
                        
                    status = STATUS_CONTINUE_FRAME
    # 中间帧处理
            elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                 "audio": str(base64.b64encode(data), 'utf-8'),
                                  "encoding": "raw"}}
                    try:
                        ws.send(json.dumps(d))
                    except Exception as e:
                        print("WebSocket error. Reconnecting...")

                        sys.exit()
                        
                        
    # 最后一帧处理
            elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(data), 'utf-8'),
                                      "encoding": "raw"}}
                    try:
                        ws.send(json.dumps(d))
                    except Exception as e:
                        print("WebSocket error. Reconnecting...")
                        sys.exit()
                        
                       
                    #time.sleep(1)
                    #break
    # 模拟音频采样间隔 ??? 
        ws.close()

    thread.start_new_thread(run, ())








def startAudioInput(dealerchain):
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = None
    while ws is None:
        try:
            ws = websocket.WebSocketApp(wsUrl, on_message=on_message(dealerchain),
                                            on_error=on_error,
                                            on_close=on_close)
            ws.on_open = on_open
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_timeout=600)
        except:
            print('try again??????????????????????') #好像没执行
            ws = None



if __name__ == "__main__":
    # 测试时候在此处正确填写相关信息即可运行
    startAudioInput(None)
