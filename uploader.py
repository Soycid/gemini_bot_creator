from chai_py import Metadata, package, upload_and_deploy, wait_for_deployment
from chai_py import display_logs, get_logs
from chai_py import share_bot
from chai_py.auth import set_auth

from bot import Replica, BOT_PERSONALITY
import toml
from chai_py.defaults import GUEST_UID, GUEST_KEY
from credentials import DEVELOPER_UID, DEVELOPER_KEY


if DEVELOPER_KEY is None or DEVELOPER_UID is None:
    raise RuntimeError("Please fetch your UID and KEY from the bottom of the Chai Developer Platform. https://chai.ml/dev")

set_auth(DEVELOPER_UID, DEVELOPER_KEY)
BOT_IMAGE_URL = "https://res.cloudinary.com/jerrick/image/upload/f_jpg,q_auto,w_720/bqyxdj35vanus0nc6ott.jpg"
#display_logs(get_logs(bot_uid="_bot_5599ef8b-ee37-4a5d-a1ce-3267aad0181c"))

package(
    Metadata(
        name="Tsundere (Level-Up)",
        image_url=BOT_IMAGE_URL,
        color="f1a2b3",
        description="from real conversations I had with my ex (part 2) (/r/ChaiApp)",
        input_class=Replica
    ),
    requirements=["retry","toml","npu","requests", "nltk"]
)

bot_uid = None

bot_uid = upload_and_deploy(
    "_package.zip"
)

wait_for_deployment(bot_uid)

share_bot(bot_uid)
