#!/usr/bin/python
#-*- coding: utf-8 -*-

import curses
import json
import os
from random import randint
from time import sleep

LOGO = """
                   N88888888N           
                   N888888888888        
                        ~D88888888?     
                             8888888    
                               888888~  
                                888888  
                                 D88888 
                                  88888 
~~~~~                             88888D
88888                             88888 
888888                           888888 
 888888                         888888  
  888888                       888888~  
   8888888$                  8888888    
    I888888888:         ~8888888887     
       8888888888888888888888888        
          M88888888888888888M           
                 MN8NM                  
"""



class InfoScreen(object):
    def __init__(self):
        self.running = True
        self.scr = curses.initscr()
        curses.noecho()
        curses.start_color()
        curses.cbreak()
        self.scr.keypad(1)
        curses.curs_set(0)        

        info_begin_x = 44
        info_begin_y = 3
        self.info_height = 45
        self.info_width = 140
        self.infowin = curses.newwin(self.info_height, self.info_width, info_begin_y, info_begin_x)

        logo_begin_x = 2
        logo_begin_y = 2
        logo_height = 22
        logo_width = 42
        self.logowin = curses.newwin(logo_height, logo_width, logo_begin_y, logo_begin_x)

        yellowtext_begin_x = 2
        yellowtext_begin_y = 22
        yellowtext_height = 5
        yellowtext_width = 42
        self.yellowtextwin = curses.newwin(yellowtext_height, yellowtext_width, yellowtext_begin_y, yellowtext_begin_x)
        self.current_page = 0
        self.pages = []

        self.update_data()

    def update_data(self):
        if not os.path.exists("./pages/"):
            os.mkdir("pages")
        self.yellowtext = json.loads(open("yellowtext.json","r").read())
        self.pages = [open("pages/"+f,"r").read() for f in os.listdir("pages")]

    def render_yellowtext(self):
        if len(self.yellowtext) > 0:
            yellowtext = self.yellowtext[randint(0, len(self.yellowtext)-1)]
            if len(yellowtext) > 42:
                arr = []
                while len(yellowtext) >1:
                    arr.append(yellowtext[:41])
                    yellowtext=yellowtext[41:]
                arr.append(yellowtext[:41]+" "*(42-len(yellowtext[:41])))
                return "\n".join(arr)
            return yellowtext+" "*(42-len(yellowtext))
        else:
            return "OHAI!"
    
    def fillinfowin(self):
        string = ""
        for i in range(0,self.info_height-2):
            string+=" "*(self.info_width-1)+"\n"
        return string+" "*(self.info_width-1)

    def drawscreen(self):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)

        self.logowin.addstr(0,0, LOGO, curses.color_pair(1))
        self.yellowtextwin.addstr(0,0, self.render_yellowtext(), curses.color_pair(2))
        self.infowin.addstr(0,0, self.fillinfowin(), curses.color_pair(3))
        self.current_page += 1
        if self.current_page >= len(self.pages):
            self.current_page = 0
        if len(self.pages) > 0:
            self.infowin.addstr(1,1, self.pages[self.current_page], curses.color_pair(3))
        else:
            self.infowin.addstr(1,1, "Gehen sie weiter, hier gibt es nichts zu sehen.", curses.color_pair(3))
        self.logowin.refresh()
        self.yellowtextwin.refresh()
        self.infowin.refresh()

    def main(self):
        try:
            while self.running:
                self.update_data()
                self.drawscreen()
                sleep(1)
        except KeyboardInterrupt:
          self.main_quit()
    
    def main_quit(self):
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()


infoscreen = InfoScreen()
infoscreen.main()
