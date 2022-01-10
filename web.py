from pywebio.input import *
from pywebio.output import *
import toml
from sample_resources import primer, first_message, prompt, image_url
import random
from bot import Replica, BOT_PERSONALITY
# get inputs from user  
data = input_group(
    "Elrich Bot Creator",
    [
        input("bot name:", name="bot_name", value="Steven", type=TEXT),
        input("bot type:", name="bot_type", value="vanilla", type=TEXT),
        input("temp:", name="temp", value=0.7, type=FLOAT),
        input("rep penalty:", name="rep_penalty", value=1.2, type=FLOAT),
        input("first message", name="first_message",value=first_message, type=TEXT),
        textarea("prompt:", rows=5, name="prompt", value=prompt, type=TEXT),
        textarea("primer:", rows=20, name="primer", value=primer, type=TEXT),
        input("image url:", name="image_url", value=image_url, type=TEXT),
    ],
)
id = random.randrange(10000)
path = f"generated/personality_{id}.toml"
# load personality file
f = open(path, "w")
data["primer"] = eval(data["primer"])
data["user_name"] = "User"
data["primer_name"] = "User"
data["memory"] = 25
data["api"] = "neuro"
data["response_length"] = 80

def t(eng, chinese):
    """return English or Chinese text according to the user's browser language"""
    return eng

toml.dump(data, f)

BOT_PERSONALITY = path

b = Replica()

b.load_personality(personality=path)
message_box = output()
put_scrollable(message_box, height=200, keep_bottom=True)
first_message = data["bot_name"] + ": " + b.respond("__first")
message_box.append(put_markdown(first_message))
print(path)
while True:
    
    response_box = input_group('Send message', [
                input(name='msg', help_text=('Message content supports Markdown')),
                actions(name='cmd', buttons=['Send', {'label': 'Exit', 'type': 'cancel'}])
            ], validate=lambda d: ('msg', 'Message content cannot be empty') if d['cmd'] == ('Send') and not d['msg'] else None)
    your_response = "You: " + response_box['msg']
    message_box.append(put_markdown(your_response))
    bot_response = data["bot_name"] + ": " + b.respond(response_box['msg'])
    message_box.append(put_markdown(bot_response))
    #chat room

put_text("The output in a table:")
put_table(
    [
        ["Name", data["bot_name"]],
        ["Type", data["bot_type"]],
        ["Temp", data["temp"]],
    ]
)
