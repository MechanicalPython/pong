import pigpio
import pot_cap
import time
pi = pigpio.pi()
pl = pot_cap.reader(pi, 23, timeout_s=0.02)
pr = pot_cap.reader(pi, 24, timeout_s=0.02)

while True:
    t = time.time()
    print(round((pl.read()[1]-10)/300, 2), round((pr.read()[1]-10)/300, 2))
    # print(time.time() -t)
