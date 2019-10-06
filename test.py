#! /usr/bin/python3


import read_paddle as rp
import pong.c_read_paddle as crp
import time
import statistics as stats
import sys


def test_paddle_speed(paddle, iters):
    paddle = rp.PaddleMove(paddle)
    times = []
    for x in range(100):
        t = time.time()
        paddle.position(iters=iters)
        times.append(time.time() - t)
    avg = sum(times)/len(times)
    print('Avg time for ',iters, 'over 100 runs:', avg)
    return avg


def test_cpaddle_speed(paddle, iters):
    paddle = crp.PaddleMove(paddle)
    times = []
    for x in range(100):
        t = time.time()
        paddle.position(iters=iters)
        times.append(time.time() - t)
    avg = sum(times)/len(times)
    print('Avg time for cread ', iters, 'over 100 runs:', avg)
    return avg


def test_paddle_stability(paddle, iters):
    paddle = rp.PaddleMove(paddle)
    position = []
    for x in range(100):
        pos = paddle.position(iters=iters)
        position.append(pos)
    sd = stats.stdev(position)
    mean = stats.mean(position)
    _min = min(position)
    _max = max(position)
    print('SD (min, max) and mean for ', iters, 'over 100 runs:', sd, _min, _max, mean)
    return sd, mean, _min, _max

if len(sys.argv) > 1:
    iters = int(sys.argv[1])
else:
    iters = 10

test_paddle_speed('l', iters)
test_paddle_speed('r', iters)

test_cpaddle_speed('l', iters)
test_cpaddle_speed('r', iters)


