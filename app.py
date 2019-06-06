import time

import redis
from flask import Flask, url_for
from random import randint

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
primeSet = "primes"

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def fastIsPrime(num, k=5): #source code: https://tinyurl.com/millerRabinSourceCode
    from random import randint
    n = int(num)
    if n < 2: return (n, "is not a prime number")
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if n % p == 0: return n == p
    s, d = 0, n-1
    while d % 2 == 0:
        s, d = s+1, d/2
    for i in range(k):
        x = pow(randint(2, n-1), int(d), int(n))
        if x == 1 or x == n-1: continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1: return (n, "is not a prime number") 
            if x == n-1: break
        else: return (n, "is not a prime number")
    cache.sadd(primeSet, n); 
    return (n, "is a prime number") 

@app.route('/')
def hello1():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<num>')
def hello2(num):
    count1 = fastIsPrime(num)
    return 'The number is prime: {}\n'.format(count1)

@app.route('/primesStored')
def hello3():
    count2 = get_hit_count()
    return 'Hello Other World! I have been seen {} times.\n'.format(count2)
