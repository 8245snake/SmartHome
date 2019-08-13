
#!/usr/bin/python3
# -*- Coding: utf-8 -*-
import time
import json
import os
import pigpio
import argparse

def openCodes():
    filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'codes')
    try:
        f = open(filePath, "r")
    except:
        print("Can't open: {}".format(filePath))
        exit(0)

    records = json.load(f)
    f.close()
    return records

def carrier(gpio, frequency, micros):
   """
   Generate carrier square wave.
   """
   wf = []
   cycle = 1000.0 / frequency
   cycles = int(round(micros/cycle))
   on = int(round(cycle / 2.0))
   sofar = 0
   for c in range(cycles):
      target = int(round((c+1)*cycle))
      sofar += on
      off = target - sofar
      sofar += off
      wf.append(pigpio.pulse(1<<gpio, 0, on))
      wf.append(pigpio.pulse(0, 1<<gpio, off))
   return wf

def play(name):

    GPIO = 17
    GAP_S = 0.1
    FREQ = 38.0

    pi = pigpio.pi()

    if not pi.connected:
        print("not connected")
        exit(0)

    records = openCodes()

    pi.set_mode(GPIO, pigpio.OUTPUT)
    pi.wave_add_new()

    emit_time = time.time()

    if name in records:
        code = records[name]

        # Create wave

        marks_wid = {}
        spaces_wid = {}

        wave = [0]*len(code)
        
        for i in range(0, len(code)):
            ci = code[i]
            if i & 1: # Space
               if ci not in spaces_wid:
                  pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                  spaces_wid[ci] = pi.wave_create()
               wave[i] = spaces_wid[ci]
            else: # Mark
               if ci not in marks_wid:
                  wf = carrier(GPIO, FREQ, ci)
                  pi.wave_add_generic(wf)
                  marks_wid[ci] = pi.wave_create()
               wave[i] = marks_wid[ci]

        delay = emit_time - time.time()

    else:
        pi.stop()
        print("{} is not exist".format(name) )
        exit(0)

    if delay > 0.0:
        time.sleep(delay)

    pi.wave_chain(wave)

    while pi.wave_tx_busy():
        time.sleep(0.002)

    emit_time = time.time() + GAP_S

    for i in marks_wid:
        pi.wave_delete(marks_wid[i])

    marks_wid = {}

    for i in spaces_wid:
        pi.wave_delete(spaces_wid[i])

    spaces_wid = {}

    pi.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='赤外線発信プログラム')
    parser.add_argument('id', help='IRデータのID')    # 必須の引数を追加
    args = parser.parse_args()

    play(args.id)

