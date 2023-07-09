# AICaller
Streaming Voice Dialogue Based on ASR, LLM, TTS

基于chatgpt的语音交互，支持打断GPT发言，能做到几乎实时无感的延时。

没有精细实现openai对话部分。

- `node server.js`
- open `index.html`

  - `python main.py`

compelete `keys.py` using 

```
openai_APIKEY = "..."
openai_BASE = "..."

kdxf_APPID = '...'
kdxf_APISecret='...'
kdxf_APIKey='...'
SYSTEM_PROMPT = "..."
```

你可以设计的prompt使之实现诸如英语外教等功能，
