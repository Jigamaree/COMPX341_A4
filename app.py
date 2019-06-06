import time

import redis
from flask import Flask, url_for

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

def get_if_prime(num):
# If given number is greater than 1 
# Iterate from 2 to n / 2
# If num is divisible by any number between 
# 2 and n / 2, it is not prime./ source: https://tinyurl.com/soucrecode
#cashe.sadd(primeSet - set numbers, primes)

    number = int(num)
    if number > 1:      
        for i in range(2, number//2): 
            if (number % i) == 0: 
                returnString = ""
                return(number, "is not a prime number") 
                break
        else: 
            return (number, "is a prime number")
            cache.sadd(primeSet, number);
    else: 
        return (num, "is not a prime number") 


@app.route('/')
def hello1():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<num>')
def hello2(num):
    count1 = get_if_prime(num)
    return 'The number {}\n'.format(count1)

@app.route('/primesStored')
def hello3():
    count2 = get_hit_count()
    return 'Hello Other World! I have been seen {} times.\n'.format(count2)
