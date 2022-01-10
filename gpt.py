import re
import time
import retry
import requests
import toml
from finetuned_api import neuroAPI, hffAPI
import nltk

class ChatAI(object):
    def __init__(self, personality="personality/neko.toml", api="hff"):
        self._load_personality(personality)
        self._load_model(api=api)
        self.message_number = 0
        nltk.download("punkt")

    def get_response(self, input_message):
        self._update_chat_history(input_message, self.user_name)
        raw_response = self._get_response()
        clean_response = self._clean_response(raw_response)
        self._update_chat_history(clean_response, self.bot_name)
        return clean_response

    def _get_response(self):
        chat_history = self.chat_history[-self.memory:]
        chat_history = "\n".join(chat_history)
        # tail = "\n{bot_name}: ".format(bot_name=self.bot_name)
        tail = "\n"
        request = self.prompt + chat_history + tail
        #request = request.format(
        #    bot_name=self.bot_name,
        #    user_name=self.user_name,
        #    primer_name=self.primer_name,
        #)
        self._adjust_model_parameters()
        return self.model.request(request)

    def _load_model(self, api="neuro"):
        if api == "neuro":
            self.model = neuroAPI(temp=self.temp, rep_penalty=self.rep_penalty)
        elif api == "hff":
            self.model = hffAPI(temp=self.temp, rep_penalty=self.rep_penalty)
            self.model.url = self.personality["url"]

    def _load_personality(self, personality):
        self.personality = toml.load(personality)
        self.bot_name = self.personality["bot_name"]
        self.user_name = self.personality["user_name"]
        self.primer_name = self.personality["primer_name"]
        self.chat_history = self.personality["primer"]
        self.prompt = self.personality["prompt"].format(
            bot_name=self.bot_name, user_name=self.user_name
        )
        self.temp = float(self.personality["temp"])
        self.rep_penalty = float(self.personality["rep_penalty"])
        self.memory = int(self.personality["memory"])
        self.response_length = int(self.personality["response_length"])
        self.image_url = self.personality["image_url"]

    def _adjust_model_parameters(self, model_function="spike2"):
        #self = utils.adjusters[model_adjuster](self)
        #rewrite using dict 
        if model_function == "linear":
            if self.model.temp < 0.65:
                self.model.temp += 0.005
        elif model_function == "spike":
            if self.message_number % 6 == 0:
                self.model.temp = 0.6
            else:
                self.model.temp = 0.2
            if self.rep_penalty > .1:
                self.rep_penalty -= 0.01
        elif model_function == "spike2":
            if self.message_number % 3 == 0:
                self.model.temp = 0.7
            else:
                self.model.temp = 0.3
            if self.rep_penalty > .1:
                self.rep_penalty -= 0.02
        else:
            print("ERROR: invalid function")  # todo use acutal error handling
        self.message_number += 1
        

    def _update_chat_history(self, message, name):
        self.chat_history += [
            "{name}: {message}".format(name=name, message=message.strip(" "))
        ]

    def _clean_response(self, raw_response):
        clean_response = raw_response.strip(" ")
        default_names = ["{user_name}","{bot_name}"]
        names_to_remove = [self.user_name, self.bot_name, self.primer_name] + default_names
        names_to_remove_lower = [x.lower() for x in names_to_remove]
        names_to_remove += names_to_remove_lower
        for name in names_to_remove:
            clean_response = self._remove_messenger_name(clean_response, name)

        if len(clean_response) == 0:
            clean_response = "..."
        clean_response = self._clean_incomplete_sentence(clean_response)
        return clean_response
    
    def _clean_incomplete_sentence(self, raw_response):
        sentences = nltk.sent_tokenize(raw_response)
        if len(sentences) > 1 and sentences[-1][-1] != ".":
            return " ".join(sentences[:-1])
        else:
            return raw_response
        
    def _remove_messenger_name(self, response, messenger_name):
        prefix = "{messenger_name}: ".format(messenger_name=messenger_name)
        
        if response.startswith(prefix):
            response_new = response[len(prefix):]
        else:
            response_new = response
        return response_new
    
    def _search_memory(self, message):
        out = -1
        for i in range(len(self.chat_history) - 1, -1, -1):
            if message in self.chat_history[i]:
                out = i
        return out
