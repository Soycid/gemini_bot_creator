import requests

URL = "chaiserver.cmlsml.com:8000"


def ping_get_conversations(bot_uid):
    """
    Returns a list of all the conversations had with a paritcular bot.
    """
    resp = requests.get(
        "http://{}/conversations/list".format(URL),
        json={"bot_uid": bot_uid},
        auth=credentials(),
    )
    assert_resp_is_good(resp)
    list_of_all_conversations_bot_had = resp.json()
    return list_of_all_conversations_bot_had


def ping_get_bots():
    """
    Return a list of all the bots deployed by the user.
    e.g [{'bot_uid': '_bot_abc', 'name': 'AI Girlfriend', 'status': 'inactive'}]
    """
    resp = requests.get("http://{}/bots/list".format(URL), auth=credentials())
    assert_resp_is_good(resp)
    return resp.json()


def ping_get_active_bots():
    """
    Return a list of all the active bots deployed by the user.
    e.g [{'bot_uid': '_bot_abc', 'name': 'AI Girlfriend', 'status': 'inactive'}]
    """
    bots = ping_get_bots()
    active_bots = [x for x in bots if x["status"] == "active"]
    return active_bots.json()


def activate_bot(bot_uid):
    """
    Make a bot discoverable by other users.
    """
    data = {"bot_uid": bot_uid}
    url = "http://{}/bots/activate".format(URL)
    resp = requests.post(url, params=data, auth=credentials())
    assert resp.status_code == 200, resp.text
    return resp.json()


def deactivate_bot(bot_uid):
    """
    Suspend a bot from public discovery.
    """
    data = {"bot_uid": bot_uid}
    url = "http://{}/bots/deactivate".format(URL)
    resp = requests.post(url, params=data, auth=credentials())
    assert resp.status_code == 200, resp.text
    return resp.json()


def credentials():
    dev_uid = "1985UITOi0WF1PiNq0vB2ndmTlH2"
    dev_key = "AcRsmgMs3B-ogVxYj2cbHkT2uofV7QDjpqyU2JYBs4wT0DP6yjSyNCjW9HXXjDClONuyG_krANRp-dmQ0zS8HA"
    return requests.auth.HTTPBasicAuth(dev_uid, dev_key)


def print_conversation(conversation):
    print(conversation["conversation_id"])
    users = conversation["participants"]
    for message in conversation["messages"]:
        timestamp = message["timestamp"]
        user = users[message["sender_uid"]]
        message = message["message"]
        print("{} {}: {}".format(timestamp, user, message))


def replay_conversations(conversations):
    for conversation in conversations:
        if len(conversation["messages"]) == 1:
            continue
        print_conversation(conversation)
        input("Press enter to continue...")
        print()


def assert_resp_is_good(resp):
    assert resp.status_code == 200, resp.text


if __name__ == "__main__":
    bot_uid = "_bot_d94c3983-60d1-48c2-9cfc-e81aa2620fae"
    my_bots = ping_get_bots()
    conversations = ping_get_conversations(bot_uid)
    replay_conversations(conversations)
