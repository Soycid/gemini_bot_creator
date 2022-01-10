
TREE = {
        "are you human?": "No I am a Catgirl!",
        "are you a bot?": "No I am a Catgirl!"
        }

def message_is_in_tree(message):
    message = message.lower()
    messages_in_tree = set(TREE.keys())
    is_in_tree = message in messages_in_tree
    return is_in_tree
