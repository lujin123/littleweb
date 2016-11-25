import threading

import requests


def test(i):
    print('thread ==> ', i)
    resp = requests.get('http://localhost:8080/index/' + str(i) + '/lujin1233')
    print(resp.content)


def main():
    threadpool = []

    for i in range(10):
        th = threading.Thread(target=test, args=(i,))
        threadpool.append(th)

    for th in threadpool:
        th.start()

    for th in threadpool:
        threading.Thread.join(th)


if __name__ == '__main__':
    main()
