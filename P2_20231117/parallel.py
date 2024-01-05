from P2_draw_client import main as d
from call_api import main as c

import threading

t1 = threading.Thread(target = c)
t2 = threading.Thread(target = d)

t1.start()
t2.start()
