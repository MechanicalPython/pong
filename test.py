#! /usr/bin/python3


import read_paddle as rp
import time
import statistics as stats

def test_paddle_speed(paddle, iters=10):
    paddle = rp.PaddleMove(paddle)
    times = []
    for x in range(100):
        t = time.time()
        paddle.position(iters=iters)
        times.append(time.time() - t)
    avg = sum(times)/len(times)
    print('Avg time for ',iters, 'over 100 runs:', avg)
    return avg

def test_paddle_stability(paddle, iters=10):
    paddle = rp.PaddleMove(paddle)
    position = []
    for x in range(100):
        pos = paddle.position(iters=iters)
        position.append(pos)
    sd = stats.stdev(position)
    mi, ma = min(position), max(position)
    mean = stats.mean(position)
    print('SD, range and mean for ', iters, 'over 100 runs:', sd, mi, ma, mean)
    return sd, mi, ma, mean

test_paddle_speed('l')
test_paddle_speed('r')


test_paddle_stability('l')
test_paddle_stability('r')
