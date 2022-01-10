import os

from chai_py import cloud_logs, set_auth

BOT_UID = '_bot_f7c63fc8-7265-461e-96ce-38d9c994891a'

dev_uid = '1985UITOi0WF1PiNq0vB2ndmTlH2'
dev_key = "AcRsmgMs3B-ogVxYj2cbHkT2uofV7QDjpqyU2JYBs4wT0DP6yjSyNCjW9HXXjDClONuyG_krANRp-dmQ0zS8HA"

set_auth(dev_uid, dev_key)

logs = cloud_logs.get_logs(BOT_UID)

print(logs)