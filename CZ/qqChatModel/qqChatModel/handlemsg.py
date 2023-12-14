import requests
from revChatGPT.V3 import Chatbot

url = 'http://127.0.0.1:5700'



#存放每个群聊对应的对话id
all_convo = {}


def send(id_, type, msg):
    if type == 'group':
        params = {
            'message_type': 'group',
            'group_id': id_,
            'message': msg
        }
    requests.post(url + '/send_msg', params=params)

class HandleMsg:
    def initialize(self, gid):
        """初次聊天时获取对话id"""
        all_convo[gid] = str(gid)

    def gro_msg(self, gid, msg, nick,model,tokenizer,history):
        print(msg)
        print('收到消息开始回复')
        """获取回答并发送群聊消息"""
        self.message = ''
        try:
            try:
                response, history = model.chat(tokenizer, msg, history=history)
                self.message += response
                print(response)
            except KeyError:
                self.initialize(gid)
                response, history = model.chat(tokenizer, msg, history=history)
                self.message += response
                print(response)
        except requests.exceptions.ProxyError:
            send(gid, 'group', '请检查代理配置')
        print()
        send(gid, 'group', nick+self.message)
        return  history
