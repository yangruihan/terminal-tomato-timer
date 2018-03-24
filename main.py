#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import threading
import time
import sys

class TimeThread(threading.Thread):
    def __init__(self, thread_id, name, remain_time):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.remain_time = remain_time
        self.total_time = remain_time

    def run(self):
        print('开始倒计时')
        while self.remain_time > 0:
            self.remain_time -= 1
            progress_log(time_format(self.remain_time), self.remain_time, self.total_time)
            time.sleep(1)

        print('\n倒计时结束')


LOG_WIDTH = 35
CLEAR_TO_END = "\033[K"
UP_ONE_LINE = "\033[F"

def progress_log(s, current, total):
    # sys.stdout.write(UP_ONE_LINE * 1)
    # sys.stdout.write('\r' + CLEAR_TO_END)
    # sys.stdout.write('\r' + s)
    # sys.stdout.write('\n')
    sys.stdout.write('\r' + CLEAR_TO_END)
    progress = 1 - current / total
    hashes = '#' * int(progress * LOG_WIDTH)
    spaces = ' ' * int(LOG_WIDTH - len(hashes))
    sys.stdout.write('\r%s/%s [%s] %d%%' % (time_format(current), time_format(total), hashes + spaces, progress * 100))

def time_format(seconds):
    return time.strftime("%M:%S", time.localtime(seconds))

def print_category():
    print("\n\n--- 命令行番茄钟 ---")
    print("1. Pomodoro（25分钟）")
    print("2. Short break（5分钟）")
    print("3. Long break（10分钟）")
    print("4. 退出")
    print("> ", end='')
    input_s = input()
    while input_s not in ['1', '2', '3', '4']:
        print("输入有误，请重新输入")
        print("> ", end='')
        input_s = input()
    return input_s

def main():
    while True:
        input_s = print_category()
        if input_s == '1':
            thread = TimeThread(1, 'time_thread', 15)
            thread.start()
        elif input_s == '2':
            thread = TimeThread(1, 'time_thread', 3)
            thread.start()
        elif input_s == '3':
            thread = TimeThread(1, 'time_thread', 6)
            thread.start()
        else:
            return
        thread.join()


if __name__ == '__main__':
    main()
