# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 22:31:48 2020

@author: Hoang Anh
"""

def fizz(n):
    for i in range(n+1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)