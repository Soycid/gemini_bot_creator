import npu
import retry
import requests

class neuroAPI(object):

    def __init__(self, temp=.4, rep_penalty=.15):
        API_TOKEN='A9v8UUQuCAUic9nBj4RTSkl8lGMClVu5Jd5hHl3LMWY'
        npu.api(API_TOKEN, deployed=True)
        self.temp = temp
        self.rep_penalty = rep_penalty

    @retry.retry(tries=3, backoff=2)
    def request(self, data):
        data = data[-2048:]
        kwargs = {
            'remove_input': True,  # whether to return your input
            'do_sample': True, # important to get realistic sentences and not just MLE
            'temperature': self.temp,
            'response_length': 32,  # how many response tokens to generate
            'repetition_penalty': self.rep_penalty, # 1 is the default
            #'eos_token_id':12982, # this is User
            'eos_token_id':198, # this is \n
        }
        model_id = '60ca2a1e54f6ecb69867c72c'
        output = npu.predict(model_id, [data], kwargs)
        resp = output[0]['generated_text']
        return resp
    
class hffAPI(object):
    url = 'https://5730289d-chai.forefront.link'

    def __init__(self, temp, rep_penalty, response_length=80):
        self.s = requests.Session()
        self.temp = temp
        self.rep_penalty = rep_penalty
        self.response_length = response_length

    @retry.retry(tries=10, backoff=9)
    def request(self, data):
        data = data[-2048:]
        print(data[-100:])
        body = {
            "text": data,
            "top_p": 1,
            "top_k": 1000,
            "temperature": self.temp,  # 0.375
            "repetition_penalty": self.rep_penalty,  # 1.2
            "length": self.response_length,
            "stop_sequences": ["\n"],
        }
        headers = {"Authorization": "Bearer de5cd678a1464dd69c954ffd"}
        res = self.s.post(self.url, json=body, headers=headers)

        res = res.json()
        if "completion" in res:
            res = res["completion"]
        else:
            res = res["result"][0]["completion"]
        return res
