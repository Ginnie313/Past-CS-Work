#!/bin/python3
'''
Sock merchant challenge from hackerrank
'''

# Complete the sockMerchant function below.
def sockMerchant(n, ar):
    sock_dict = {}
    for item in ar:
        if item in sock_dict:
            sock_dict[item] += 1
        else:
            sock_dict[item] = 1
    sock_score = 0
    for key in sock_dict:
        sock_score += (sock_dict.get(key) // 2)

    return sock_score

if __name__ == '__main__':
    print(sockMerchant(9, [9,10,20, 20, 10, 10, 30, 50, 10, 20]))
