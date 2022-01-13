from chai_py import ChaiBot, Update
from gpt import ChatAI
import random
import time
import toml

# import utils.sentences

BOT_IMAGE_URL = "https://res.cloudinary.com/jerrick/image/upload/f_jpg,q_auto,w_720/bqyxdj35vanus0nc6ott.jpg"
BOT_PERSONALITY = "w.toml" 
SIMILARITY_THRESHOLD = 0.95
USE_SIMILARITY = False
USE_TIMED_RESPONSE = False
SWITCH_CONSTANT = 5
# api = "neuro"
class Replica(ChaiBot):
#    def __init__(self,personality=BOT_PERSONALITY):
#        self.load_personality(personality=personality)

    def setup(self):
        self.logger.info("Setting up...")
        self.load_personality() 
    def load_personality(self,personality=BOT_PERSONALITY):
        self.response_count = 0
        if personality != None: 
            self.personality=toml.load(personality)
      
            self.model = ChatAI(personality=personality, api="neuro")

            self.first_message = self.personality["first_message"]
            if USE_TIMED_RESPONSE:
                self.timed_responses = self.personality["timed_responses"]
            if USE_SIMILARITY: 
                self.scripted_responses = self.personality["scripted_responses"]
            self.bot_type = self.personality["bot_type"]
            if self.bot_type.lower() == "switch":
                self._init_states()

    async def on_message(self, update):
        return self.respond(update.latest_message.text)

    def _init_states(self):
        self.states = self.personality["states"]
        self.state_emojis = self.personality["state_emojis"]
        self.state_data = {}
        for state in self.states:
            self.state_data[state] = self.personality[state]

    def respond(self, message):
        output = None
        self.response_count += 1
        user_asking_for_picture = (" pic" in message) or (" photo" in message)
        its_time_to_send_pic = user_asking_for_picture and random.random() < 0.6

        if USE_TIMED_RESPONSE:
            output = self._get_timed_response(message)

        if USE_SIMILARITY and (output is None):
            output = self._get_scripted_response(message)

        if message == "__first" or message == "first":
            output = self.first_message
            self.model.chat_history += "{bot_name}: " + output

        elif self.bot_type.lower() == "switch":
            output = self._switch_response(message)

        elif its_time_to_send_pic:
            output = "![sexy_pic]({BOT_IMAGE_URL})".format(BOT_IMAGE_URL=BOT_IMAGE_URL)

        else:
            output = self.model.get_response(message)
        return output

    def _switch_response(self, message):
        output = None
        state_number = self.response_count // SWITCH_CONSTANT % len(self.states)
        self.state = self.states[state_number]
        emoji = self.state_emojis[self.state]
        is_state_change = self.response_count % SWITCH_CONSTANT == 0
        is_first_cycle = self.response_count < SWITCH_CONSTANT * len(self.states)
        if is_state_change and is_first_cycle:
            self.model.chat_history += self.state_data[self.state]["tail"]
            output = self.state_data[self.state]["message"]
        elif is_state_change:
            self.model.chat_history += self.state_data[self.state]["tail"]
        else:
            output = self.model.get_response(message)
        
        if output == None:
            output = "I'm not sure what you mean..."
        return output.strip('\n') + " " + emoji + "\n"

    def _get_scripted_response(self, message):
        resp = None
        """
        self.bert = utils.sentences.bert()
        for response in self.scripted_responses:
            message_is_known = (
                self.bert.similarity(response["message"], message)
                > SIMILARITY_THRESHOLD
            )
            if message_is_known:
                resp = scripted_response["response"]
        """
        return resp

    def _get_timed_response(self, message):
        resp = None
        for timed_response in self.timed_responses:
            if timed_response["time"] == self.response_count:
                resp = timed_response["response"]
        return resp


if __name__ == "__main__":
    scripted = True
    t0 = time.time()
    # import pdb; pdb.set_trace()
    r = Replica()
    resps = [
        "__first",
        "How's it going?",
        "What are your hobbies",
        "What did humans do to you?",
        "How do you feel about me?",
        "Do you have pointy ears",
        "Can I see a pic?",
        "__first",
        "How's it going?",
        "What are your hobbies",
        "What did humans do to you?",
        "How do you feel about me?",
        "Do you have pointy ears",
        "Can I see a pic?",
        "__first",
        "How's it going?",
        "What are your hobbies",
        "What did humans do to you?",
        "How do you feel about me?",
        "Do you have pointy ears",
        "Can I see a pic?",
        "__first",
        "How's it going?",
        "What are your hobbies",
        "What did humans do to you?",
        "How do you feel about me?",
        "Do you have pointy ears",
        "Can I see a pic?",
        "__first",
        "How's it going?",
        "What are your hobbies",
        "What did humans do to you?",
        "How do you feel about me?",
        "Do you have pointy ears",
        "Can I see a pic?",
    ]

    if scripted == False:
        for _ in range(10):
            str_input = input()
            print("user: {}".format(str_input))
            print("ai: {}".format(r.respond(str_input)))
    else:
        for _ in range(4):
            r = Replica()
            for m in resps:
                print("user: {}".format(str(m)))
                print("bot: {}".format(r.respond(str(m))))

    print("time for 20 messages: {}".format(time.time() - t0))
