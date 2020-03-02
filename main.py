#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import threading
import time
import sys
import os


class TimeThread(threading.Thread):
    def __init__(self, thread_id, name, remain_time, target):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.remain_time = remain_time
        self.total_time = remain_time
        self.target = target
        self.start_time = time.time()

    def run(self):
        with open('log.txt', 'a') as f:
            f.write(
                f"{time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(self.start_time))} {self.target} $X$\n")

        terminal_notifier("倒计时开始", "剩余时间" + (time_format(self.remain_time)))

        while self.remain_time > 0:
            self.remain_time -= 1
            progress_log(time_format(self.remain_time),
                         self.remain_time, self.total_time)
            time.sleep(1)

        lines = []

        with open('log.txt', 'r') as f:
            lines = f.readlines()

            while '' in lines:
                lines.remove('')

        with open('log.txt', 'w') as f:
            if len(lines) > 0:
                if lines[-1].split(' ')[0] == time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(self.start_time)):
                    lines[-1] = f"{time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(self.start_time))} {self.target} $D$\n"
            f.writelines(lines)

        terminal_notifier("倒计时结束", "请选择下一项任务")


def terminal_notifier(title, content, sound=True):
    if sound:
        os.system('terminal-notifier -message %s -title %s -sound default' %
                  (content, title))
    else:
        os.system('terminal-notifier -message %s -title %s' % (content, title))


LOG_WIDTH = 35
CLEAR_TO_END = "\033[K"
UP_ONE_LINE = "\033[F"


def progress_log(s, current, total):
    sys.stdout.write('\r' + CLEAR_TO_END)
    progress = 1 - current / total
    hashes = '#' * int(progress * LOG_WIDTH)
    spaces = ' ' * int(LOG_WIDTH - len(hashes))
    sys.stdout.write('\r%s/%s [%s] %d%%' % (time_format(current),
                                            time_format(total), hashes + spaces, progress * 100))


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

    if input_s in '23':
        return input_s, '休息'
    elif input_s == '4':
        return input_s, ''

    print("请输入目标（可为空）")
    print("> ", end='')

    input_target = input()
    input_target = "未说明" if input_target == "" else input_target

    return input_s, input_target


def main():
    while True:
        input_s, input_target = print_category()

        if input_s == '1':
            thread = TimeThread(1, 'time_thread', 1500, input_target)
            thread.start()
        elif input_s == '2':
            thread = TimeThread(1, 'time_thread', 300, input_target)
            thread.start()
        elif input_s == '3':
            thread = TimeThread(1, 'time_thread', 600, input_target)
            thread.start()
        else:
            return
        thread.join()


if __name__ == '__main__':
    main()
