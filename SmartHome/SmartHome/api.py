#!/usr/bin/python3
# -*- Coding: utf-8 -*-

from SmartHome.remoteIR import openCodes,play
from flask_api import status

codes = openCodes()
colors = ['white', 'red', 'blue', 'orange', 'gray']

def CeilingLight(switch:bool):
    if switch:
        play('light:on')
    else:
        play('light:off')

def LED(switch:bool):
    if switch:
        play('LED:on')
    else:
        play('LED:off')

def LED_color(color:str):
    if color in colors:
        play('LED:on')
        play('LED:' + color)

def AirConditioner(switch:bool, degree:int=27):
    if switch:
        play('air:on')
    else:
        play('air:off')

def callAPI(target:str, switch_str:str, color_str:str=None):

    switch = (switch_str.upper == 'ON')
    if color_str in colors:
        color = color_str
    else:
        color = None

    if target.upper == 'light'.upper:
        CeilingLight(switch)
    elif target.upper == 'LED':
        if color == None:
            LED(switch)
        else:
            LED_color(color)
    elif target.upper == 'air'.upper:
        AirConditioner(switch)
    else:
        return "target  ot exist", status.HTTP_204_NO_CONTENT

    return "OK", status.HTTP_200_OK

if __name__ == '__main__':
    json = openCodes()
    print(json)