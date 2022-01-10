import requests
URL = 'chai.devcmls.com:8000'


def credentials():
    dev_uid = '1985UITOi0WF1PiNq0vB2ndmTlH2'
    dev_key = "AcRsmgMs3B-ogVxYj2cbHkT2uofV7QDjpqyU2JYBs4wT0DP6yjSyNCjW9HXXjDClONuyG_krANRp-dmQ0zS8HA"
    return requests.auth.HTTPBasicAuth(dev_uid, dev_key)


def ping_get_conversations(bot_uid):
    """
    Returns a list of all the conversations had with a paritcular bot.
    """
    resp = requests.get(
        'http://{}/conversations/list'.format(URL),
        json={'bot_uid': bot_uid},
        auth=credentials()
    )

    assert resp.status_code == 200, resp.text
    return resp.json()


def ping_get_stats(bot_uid):
    """
    Return summary statistics for the bot over the previous 24 hours.
    """
    resp = requests.get(
        'http://{}/bots/stats'.format(URL),
        params={'bot_uid': bot_uid},
        auth=credentials()
    )

    assert resp.status_code == 200, resp.text
    return resp.json()


def ping_get_bots():
    """
    Return a list of all the bots deployed by the user.

    e.g [{'bot_uid': '_bot_abc', 'name': 'AI Girlfriend', 'status': 'inactive'}]

    """
    resp = requests.get('http://{}/bots/list'.format(URL), auth=credentials())
    assert resp.status_code == 200, resp.text
    return resp.json()


def ping_leaderboard():
    """
    Returns a ranking of the active bots over the previous day.
    """
    resp = requests.get('http://{}/leaderboard'.format(URL), auth=credentials())
    assert resp.status_code == 200, resp.text
    return resp.json()


def activate_bot(bot_uid):
    """
    Make a bot discoverable by other users.
    """
    data = {'bot_uid': bot_uid}
    url = 'http://{}/bots/activate'.format(URL)
    resp = requests.post(url, params=data, auth=credentials())
    assert resp.status_code == 200, resp.text
    return resp.json()


def deactivate_bot(bot_uid):
    """
    Suspend a bot from public discovery.
    """
    data = {'bot_uid': bot_uid}
    url = 'http://{}/bots/deactivate'.format(URL)
    resp = requests.post(url, params=data, auth=credentials())
    assert resp.status_code == 200, resp.text
    return resp.json()


def print_conversation(conversation):
    print(conversation['conversation_id'])
    users = conversation['participants']
    for message in conversation['messages']:
        timestamp = message['timestamp']
        user = users[message['sender_uid']]
        message = message['message']
        print('{} {}: {}'.format(timestamp, user, message))


def replay_conversations(conversations):
    for conversation in conversations:
        if len(conversation['messages']) == 1:
            continue
        print_conversation(conversation)
        input('Press enter to continue...')
        print()


if __name__ == '__main__':
    leaderboard = ping_leaderboard()
    my_bots = ping_get_bots()

    bot_uid = '_bot_d94c3983-60d1-48c2-9cfc-e81aa2620fae'
    conversations = ping_get_conversations(bot_uid)
    replay_conversations(conversations)