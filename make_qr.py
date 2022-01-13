import segno
import os
def make_qr(bot_uid: str) -> str:
    """Displays the url, a QR code, along with additional guidance.
    :param bot_uid:
    :return: The url for the bot.
    """
    url = f"chai://chai.ml/{bot_uid}"
    qr_code = segno.make_qr(url)
    print("Scan the QR code with your phone to start a chat in the app!")
    print(f"Or check it out at {url}")
    qr_code.save("qr.png", scale = 10)
    return url

