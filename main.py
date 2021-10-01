from shutil import copy
from datetime import date, timedelta, datetime
from time import sleep
from ctypes import *
from os import listdir
from os.path import isfile, join

windll.Kernel32.GetStdHandle.restype = c_ulong
h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
setclr = windll.Kernel32.SetConsoleTextAttribute

def check_archive():
    return [f[29:37]+'.BIL' for f in listdir(src) if isfile(join(src, f))]

def fnc(days_ago):
    '''File Name Constructor.
    Коструктор имени файла.
    1 аргумент - days_ago - количество прошедших дней'''
    filename = (date.today() - timedelta(days=days_ago)).strftime('20%y%m%d.BIL')
    return filename

def copy_day(fn):
    'копиирование файла'
    if fn in all_copied_files:
        setclr(h, 11)
        print('файл '+fn+' уже найден в архиве')
        return True
    else:
        try:
            setclr(h, 14)
            print("попытка скопировать: "+fn+", жди...\nИЗ: "+src+"\nВ: "+dst)
            copy(src + fn, dst + fn)
            setclr(h, 10)
            print("СКОПИРОВАЛ "+fn)
            return True
        except:
            setclr(h, 12)
            print('!НЕ СКОПИРОВАЛОСЬ :-(')
            return False


#src = '\\\\Bam\\D$\\Bill\\Bill\\'
#dst = '\\\\10.149.105.2\\data\\in\\'
archive = 'D:\\' #'\\\\10.149.105.2\\data\\archive\\'
src = 'D:\\'
dst = 'D:\I\\'

setclr(h, 7)
all_copied_files = check_archive()
last_try = True
if all([copy_day(fnc(i)) for i in range(7, 0, -1)]): #попытка скопировать последнюю неделю
    setclr(h, 10)
    print('Файлы за последнюю неделю были проверены. Всё ОК')
else:
    setclr(h, 12)
    print('Файлы за последнюю неделю были проверены. Внимание, не все файлы есть в архиве.')

this_day = datetime.today().day

while True:
    sleep(7200)
    if this_day != datetime.today().day or last_try is False:
        last_try = copy_day(fnc(1))
    setclr(h, 7)