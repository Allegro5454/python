#!/usr/bin/env python3
import curses
import time
from pathlib import Path
import random


dungeons = {
    "1": Path("maps/1.txt")
}

eq = {'potion'}
health = 100
weapon = {
    "basic_sword":"10"
}

def load_level(file_path):
    with open(file_path, "r") as f:
        return [list(line.rstrip("\n")) for line in f if line.strip()]

def testname(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    player_y = 10
    player_x = 10
    current_level = "1"
    
    grid = load_level(dungeons[current_level])
    for y, row in enumerate(grid):
        stdscr.addstr(y, 0, "".join(row))
        
    stdscr.addstr(player_y, player_x, "@")
    stdscr.refresh()
    player_move(stdscr, player_y, player_x, grid)
    
def player_move(stdscr, player_y, player_x, dungeon_grid):
    max_x = len(dungeon_grid[0])
    door = 0
    show1 = 0
    while True:
        prev_x, prev_y = player_x, player_y
        key = stdscr.getkey()
        if key == "w":
            player_y = player_y - 1
        elif key == "s":
            player_y = player_y + 1
        elif key == "a":
            player_x = player_x - 1
        elif key == "d":
            player_x = player_x + 1
        if key == "e" and show1 != 1:
            show1 = 1
            stdscr.addstr(36,0,f"EQ: {eq}" )
        elif key == "e" and show1 == 1:
            stdscr.addstr(36,0,"\n" )
            show1 = 0
        wanted_tile = dungeon_grid[player_y][player_x]
        if wanted_tile == "#" or wanted_tile == "c":
            player_x,player_y = prev_x, prev_y
            stdscr.addstr(player_y,player_x,"@")
            stdscr.refresh()
        elif wanted_tile == "-":
            door = 1
            stdscr.addstr(prev_y,prev_x,".")
            stdscr.addstr(player_y,player_x,"@" )            
        elif door == 1 and wanted_tile != "#":
            door = 0
            stdscr.addstr(prev_y,prev_x,"-")
            stdscr.addstr(player_y,player_x,"@" )
        else:
            stdscr.addstr(prev_y,prev_x,".")
            stdscr.addstr(player_y,player_x,"@" )
            stdscr.refresh()
        if wanted_tile == "c":
            eq.add("key")
            chest_fight(stdscr,max_x)
        time.sleep(0.1)    
def chest_fight(stdscr, max_x):
    grid = load_level(Path("maps/goblin.txt"))
    for y, row in enumerate(grid):
        stdscr.addstr(y, max_x, "".join(row))
    stdscr.addstr(37, max_x, "You encountered a goblin guarding the chest")
    enemy_damage_min = 2
    enemy_damage_max = 100
    fight_mechanic(stdscr, max_x, health, 50, enemy_damage_min, enemy_damage_max)



    else:
        game_over(stdscr)
def game_over(stdscr):
    stdscr.clear()
    grid = load_level(Path("maps/over.txt"))
    for y, row in enumerate(grid):
        stdscr.addstr(y, 0, "".join(row))
    stdscr.addstr(y, 30, "Violence isn't the answer")
    stdscr.refresh()
    time.sleep(100)           


def dating(stdscr, max_x):

    for i in range(46):
        stdscr.addstr(i, max_x, "                                                                 ")
    grid = load_level(Path("maps/goblin_date.txt"))
    for y, row in enumerate(grid):
        stdscr.addstr(y, max_x, "".join(row))
    sex_appeal = 0
    while sex_appeal <= 100:
        affection_rise = random.randint(1, 5)
        complement = complements[random.randint(1, 5)]
        complement_num = random.randint(1, 5)
        complement = complements[complement_num]
        if affection_rise == 1:
            affection =+ 5
        if affection <=30:  
            chance1 = affection + random.randint(40, 100)
            chance2 = affection + random.randint(40, 90)
            chance3 = 2*affection + random.randint(20, 40)
        else:
            chance1 = affection + random.randint(40, 100)
            chance2 = affection + random.randint(40, 90)
            chance3 = 2*affection + random.randint(20, 40)
        texts = {
            1:f"Across this candlelit table, {name}, the shadows tremble not from the dark, but before your {complement}.",
            2:f"Wine and moonlight pale tonight, {name}, eclipsed entirely by the lethal poise of your {complement}.",
            3:f"Every sculpted beauty in the realm is mundane, {name}, beside the rare, intoxicating presence of your {complement}.",
            4:f"The grave quiet of this supper was suffocating until you spoke, {name}; nothing disarms my guards like your {complement}.",
            5:f"A world of beasts tore itself apart outside tonight, yet here with you, {name}, I am subdued by your {complement}.",
            }
        stdscr.addstr(38, max_x, f"Current affection toward goblins:      ")
        stdscr.addstr(39, max_x, f"1: Complement his                                      ")
        stdscr.addstr(40, max_x, f"2: Ask about his interests,     ")
        stdscr.addstr(41, max_x, f"3: Ask for his hand, (Risky move)      ")
        stdscr.addstr(38, max_x, f"Current affection toward goblins: {affection}")
        stdscr.addstr(39, max_x, f"1: Complement his {complement}, {chance1} %")
        stdscr.addstr(40, max_x, f"2: Ask about his interests, {chance2} %")
        stdscr.addstr(41, max_x, f"3: Ask for his hand, (Risky move){chance3} %")
        stdscr.refresh()
        key = stdscr.getkey()
        if key == "1":
            text = texts[int(complement_num)]
            stdscr.addstr(43, 0, f"{text}")
            check =  random.randint(1,100)
            if check <= chance1:
                reply = agree[int(complement_num)]
                stdscr.addstr(44, 0, f"{reply}")
                sex_appeal =+ 5 
            else:
                reply = disagree[int(complement_num)] 
                stdscr.addstr(44, 0, f"{reply}")
            stdscr.refresh()
        stdscr.getkey()
        stdscr.addstr(43,0,"                                                                                                                                                         ")
        stdscr.addstr(44,0,"                                                                                                                                                                                        ")
        stdscr.refresh() 
        

        
        
def main(stdscr):
    start(stdscr)

    state = main_menu(stdscr)
    if state == "Test name":
        stdscr.clear()
        stdscr.addstr(0, 0, "Starting Test name...")
        stdscr.refresh()
        time.sleep(0.2)
        testname(stdscr)
    elif state == "Exit":
        return 


curses.wrapper(main)
