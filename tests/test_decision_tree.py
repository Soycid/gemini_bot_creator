import GEMINI.decision_tree as tree

def test_if_a_message_is_in_tree():
    message = "are you human?"
    assert tree.message_is_in_tree(message)
    message = "random"
    assert not tree.message_is_in_tree(message)
    message = "are you a man?"
    assert tree.message_is_in_tree(message)
