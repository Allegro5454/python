#!/usr/bin/env python3
import curses
import time
from pathlib import Path
import random

def start(stdscr):
    curses.curs_set(0)

    welcmsg = r"""                               
     __      __        __                               
    /  \    /  \ ____ |  |   ____  ____   _____   ____  
    \   \/\/   // __ \|  | _/ ___\/  _ \ /     \_/ __ \ 
     \        /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/ 
      \__/\  /  \___  >____/\___  >____/|__|_|  /\___  >
           \/       \/          \/            \/     \/ 
    """

    stdscr.addstr(0, 0, welcmsg)
    stdscr.refresh()
    time.sleep(1)
    stdscr.clear()

    testmsg = r"""
    ___________              __                                  
    \__    ___/___   _______/  |_    ____ _____    _____   ____  
      |    |_/ __ \ /  ___/\   __\  /    \\__  \  /     \_/ __ \ 
      |    |\  ___/ \___ \  |  |   |   |  \/ __ \|  Y Y  \  ___/ 
      |____| \___  >____  > |__|   |___|  (____  /__|_|  /\___  >
                 \/     \/              \/     \/      \/     \/ 
                 """
    stdscr.addstr(0, 0, testmsg)
    stdscr.refresh()
    time.sleep(1)
def main_menu(stdscr):
    menumsg = r"""
 ____      ___________              __                                  
/_   |     \__    ___/___   _______/  |_    ____ _____    _____   ____  
 |   |       |    |_/ __ \ /  ___/\   __\  /    \\__  \  /     \_/ __ \ 
 |   |       |    |\  ___/ \___ \  |  |   |   |  \/ __ \|  Y Y  \  ___/ 
 |___| /\    |____| \___  >____  > |__|   |___|  (____  /__|_|  /\___  >
       \/               \/     \/              \/     \/      \/     \/ 
________       ___________      .__  __                                 
\_____  \      \_   _____/__  __|__|/  |_                               
 /  ____/       |    __)_\  \/  /  \   __\                              
/       \       |        \>    <|  ||  |                                
\_______ \ /\  /_______  /__/\_ \__||__|                                
        \/ \/          \/      \/                                       
"""
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, menumsg)
        stdscr.addstr(14,0, "Type 1 or 2.")
        stdscr.refresh()
        key = stdscr.getkey()
        if key == "1":
            return "Test name"
        elif key == "2":
            return "Exit"
        else:
            stdscr.addstr(16,0,"Wrong key, try again")
            stdscr.refresh()
            time.sleep(1)
dungeons = {
    "1": Path("maps/1.txt")
}
goblins = {
    1:"Mieczyslaw",
    2:"Geralt",
    3:"Ruby",
    4:"Marcin",
    5:"Szczepan"
}

complements = {
    1:"muscular body",
    2:"majestic sword",
    3:"extravagant left ear",
    4:"humor",
    5:"politeness",
}
name = goblins[(random.randint(1, 5))]
complement_num = random.randint(1, 5)
complement = complements[complement_num] 


texts = {
    1:f"Across this candlelit table, {name}, the shadows tremble not from the dark, but before your {complement}.",
    2:f"Wine and moonlight pale tonight, {name}, eclipsed entirely by the lethal poise of your {complement}.",
    3:f"Every sculpted beauty in the realm is mundane, {name}, beside the rare, intoxicating presence of your {complement}.",
    4:f"The grave quiet of this supper was suffocating until you spoke, {name}; nothing disarms my guards like your {complement}.",
    5:f"A world of beasts tore itself apart outside tonight, yet here with you, {name}, I am subdued by your {complement}.",
}
agree = {
    1:f'{name} leans forward, shadows deepening across a sudden smirk. "Then come closer. Let the dark witness how easily you yield to it."',
    2:f'{name} rests a hand near the hilt, eyes locking in silent thrill. "A keen eye. Keep looking, and I might show you how gently it cuts."',
    3:f'A subtle, knowing tilt of the chin reveals a concealed secret. {name} whispers, "You notice the anomalies the blind fear to touch. I find that dangerous... and alluring."',
    4:f'A low, velvet chuckle breaks across the table. {name} raises a glass. "A dangerous confession. Once my defenses breach yours, I never retreat."',
    5:f'Fingers brush across the dark cloth, pausing an inch away. {name} replies softly, "Courtly grace is merely the cage. Since you ask so gently, perhaps I will let you inside."'
}
disagree = {
    1:f'{name} sets down the silver goblet with a dull, hollow ring. "Flattery carved from meat and bone moves cutthroats, not me. Eat your bread in silence."',
    2:f'The cold metal stays dormant. {name} turns a gaze colder than lead. "You mistake a weapon for an ornament. Such careless eyes rarely keep their sight."',
    3:f'{name} pulls the cowl lower, voice dripping like bitter venom. "You gawk at oddities like a carnival jester. The supper is over."',
    4:f'The smile vanishes into an impenetrable mask. {name} stares past the flame. "My words are not your entertainment. Do not mistake breathing air for an invitation."',
    5:f'{name} recoils into rigid, iron stillness. "You speak of manners while trespassing with your eyes. We have concluded all that was to be shared."'
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



def fight_mechanic(stdscr, max_x, health, enemy_health, enemy_damage_min, enemy_damage_max):
    stdscr.addstr(39, max_x, "Choose action:")
    stdscr.addstr(40, max_x, f"1: Attack with {weapon}")
    stdscr.addstr(41, max_x, f"2: Ask on a date")
    stdscr.addstr(42, max_x, "3: Heal")        
    stdscr.refresh()
    while enemy_health >= 0:
        key = stdscr.getkey()
        stdscr.addstr(38, max_x, "                                     ")
        stdscr.addstr(38, max_x, f"Enemy Health: {enemy_health} | Your Health: {health}")
        stdscr.addstr(43, max_x,"                                ")
        if key == "1" or key == "2" or key == "3":
            if key == "1":
                enemy_health -= int(weapon["basic_sword"])
                stdscr.addstr, max_x, f"You attacked: {int(weapon["basic_sword"])} "
            elif key == "2":
                dating(stdscr, max_x)
                time.sleep(1)
            elif key == "3":
                if "potion" in eq:
                    health =+ 50
                    stdscr.addstr(43, max_x, "Healed 50hp")
                    eq.remove("potion")    
            enemy_attack = random.randint(enemy_damage_min, enemy_damage_max)
            health = health - enemy_attack
            stdscr.addstr(43, max_x,f"Goblin attacked: -{enemy_attack}hp")
            stdscr.refresh()
        else:
            stdscr.addstr(43, max_x,f"Press 1, 2 or 3")
            stdscr.refresh()
        if health <= 0:
            break    
        time.sleep(1)
    if enemy_health <= 0:
        stdscr.addstr(38,max_x,"Enemy health: 0 ") 
        stdscr.addstr(43, max_x,"                                ")    
        stdscr.addstr(43,max_x,"You won")
        time.sleep(2)
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
    complement = complements[complement_num]
    affection = 0
    chance1 = affection + random.randint(40, 100)
    chance2 = affection + random.randint(40, 90)
    chance3 = 2*affection + random.randint(20, 40)
    for i in range(46):
        stdscr.addstr(i, max_x, "                                                                 ")
    grid = load_level(Path("maps/goblin_date.txt"))
    for y, row in enumerate(grid):
        stdscr.addstr(y, max_x, "".join(row))
    stdscr.addstr(37, max_x, f"You are on a date with {name} ")
    stdscr.addstr(38, max_x, f"Current affection toward goblins: {affection}")
    stdscr.addstr(39, max_x, f"1: Complement his {complement}, {chance1} %")
    stdscr.addstr(40, max_x, f"2: Ask about his interests, {chance2} %")
    stdscr.addstr(41, max_x, f"3: Ask for his hand, (Risky move){chance3} %")
    stdscr.refresh()
    sex_appeal = 0
    while sex_appeal <= 100:
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
                stdscr.addstr(41, 0, f"{reply}")
            stdscr.refresh() 
        affection_rise = random.randint(1, 2)
        if affection_rise == 1:
            affection =+ 5
          
        chance1 = affection + random.randint(40, 100)
        chance2 = affection + random.randint(40, 90)
        chance3 = 2*affection + random.randint(20, 40)
        complement = complements[random.randint(1, 5)]
        stdscr.addstr(38, max_x, f"Current affection toward goblins:      ")
        stdscr.addstr(39, max_x, f"1: Complement his                                      ")
        stdscr.addstr(40, max_x, f"2: Ask about his interests,     ")
        stdscr.addstr(41, max_x, f"3: Ask for his hand, (Risky move)      ")
        stdscr.addstr(38, max_x, f"Current affection toward goblins: {affection}")
        stdscr.addstr(39, max_x, f"1: Complement his {complement}, {chance1} %")
        stdscr.addstr(40, max_x, f"2: Ask about his interests, {chance2} %")
        stdscr.addstr(41, max_x, f"3: Ask for his hand, (Risky move){chance3} %")

        key2 = stdscr.getkey()
        stdscr.addstr(43,0,"                                                                                                                                                         ")
        stdscr.addstr(44,0,"                                                                                                                                                         ")
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
