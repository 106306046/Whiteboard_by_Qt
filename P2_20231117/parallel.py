from P2_draw_client import main as whiteboard
from call_api import main as api

import threading

t1 = threading.Thread(target = api)
t2 = threading.Thread(target = whiteboard)

t1.start()
t2.start()
