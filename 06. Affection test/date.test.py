#def dating(stdscr, max_x):
#    complement = complements[complement_num]
#    affection = 0
#    chance1 = affection + random.randint(40, 100)
#    chance2 = affection + random.randint(40, 90)
#    chance3 = 2*affection + random.randint(20, 40)
#    for i in range(46):
#        stdscr.addstr(i, max_x, "                                                                 ")
#    grid = load_level(Path("maps/goblin_date.txt"))
#    for y, row in enumerate(grid):
#        stdscr.addstr(y, max_x, "".join(row))
#    stdscr.addstr(37, max_x, f"You are on a date with {name} ")
#    stdscr.addstr(38, max_x, f"Current affection toward goblins: {affection}")
#    stdscr.addstr(39, max_x, f"1: Complement his {complement}, {chance1} %")
#    stdscr.addstr(40, max_x, f"2: Ask about his interests, {chance2} %")
#    stdscr.addstr(41, max_x, f"3: Ask for his hand, (Risky move){chance3} %")
#    stdscr.refresh()
#    sex_appeal = 0
#    while sex_appeal <= 100:
#        key = stdscr.getkey()
#        if key == "1":
#            text = texts[int(complement_num)]
#            stdscr.addstr(43, 0, f"{text}")
#            check =  random.randint(1,100)
#            if check <= chance1:
#                reply = agree[int(complement_num)]
#                stdscr.addstr(44, 0, f"{reply}")
#                sex_appeal =+ 5 
#            else:
#                reply = disagree[int(complement_num)] 
#                stdscr.addstr(41, 0, f"{reply}")
#            stdscr.refresh() 
#        affection_rise = random.randint(1, 2)
#        if affection_rise == 1:
#            affection =+ 5
#        if affection <=30:  
#            chance1 = affection + random.randint(40, 100)
#            chance2 = affection + random.randint(40, 90)
#            chance3 = 2*affection + random.randint(20, 40)
#        else:
#            chance1 = affection + random.randint(40, 100)
#            chance2 = affection + random.randint(40, 90)
#            chance3 = 2*affection + random.randint(20, 40)
#        complement = complements[random.randint(1, 5)]
#        stdscr.addstr(38, max_x, f"Current affection toward goblins:      ")
#        stdscr.addstr(39, max_x, f"1: Complement his                                      ")
#        stdscr.addstr(40, max_x, f"2: Ask about his interests,     ")
#        stdscr.addstr(41, max_x, f"3: Ask for his hand, (Risky move)      ")
#        stdscr.addstr(38, max_x, f"Current affection toward goblins: {affection}")
#        stdscr.addstr(39, max_x, f"1: Complement his {complement}, {chance1} %")
#        stdscr.addstr(40, max_x, f"2: Ask about his interests, {chance2} %")
#        stdscr.addstr(41, max_x, f"3: Ask for his hand, (Risky move){chance3} %")
#
#        key2 = stdscr.getkey()
#        stdscr.addstr(43,0,"                                                                                                                                                         ")
#        stdscr.addstr(44,0,"                                                                                                                                                         ")
#        stdscr.refresh()
#
#    class player:
#        def __init__(self):
#            self.dungeons = {
#                "1": Path("maps/1.txt")
#            }
#            self.player_y = {
#                "1": 10,
#            }
#            self.player_x = {
#                "1": 10,
#            }
#            self.eq = {'potion'}
#            self.health = 100
#            self.weapon = {
#                "basic_sword":"10"
#            }
#            pass
#        def player_move(stdscr, grid, player_y, player_x):
#            stdscr.addstr(player_y, player_x, "@")
#            stdscr.refresh()
#            max_x = len(grid[0])
#            door = 0
#            show1 = 0
#            while True:
#                prev_x, prev_y = player_x, player_y
#                key = stdscr.getkey()
#                if key == "w":
#                    player_y = player_y - 1
#                elif key == "s":
#                    player_y = player_y + 1
#                elif key == "a":
#                    player_x = player_x - 1
#                elif key == "d":
#                    player_x = player_x + 1
#                if key == "e" and show1 != 1:
#                    show1 = 1
#                    stdscr.addstr(36,0,f"EQ:" )
#                elif key == "e" and show1 == 1:
#                    stdscr.addstr(36,0,"\n" )
#                    show1 = 0
#                wanted_tile = grid[player_y][player_x]
#                if wanted_tile == "#" or wanted_tile == "c":
#                    player_x,player_y = prev_x, prev_y
#                    stdscr.addstr(player_y,player_x,"@")
#                    stdscr.refresh()
#                elif wanted_tile == "-":
#                    door = 1
#                    stdscr.addstr(prev_y,prev_x,".")
#                    stdscr.addstr(player_y,player_x,"@" )            
#                elif door == 1 and wanted_tile != "#":
#                    door = 0
#                    stdscr.addstr(prev_y,prev_x,"-")
#                    stdscr.addstr(player_y,player_x,"@" )
#                else:
#                    stdscr.addstr(prev_y,prev_x,".")
#                    stdscr.addstr(player_y,player_x,"@" )
#                    stdscr.refresh()
#                if wanted_tile == "c":
#                    chest_fight(stdscr)
#                time.sleep(0.1)
#        def chest_fight(stdscr):
#            ...
#        def level_loader(stdscr, level, player_y, player_x):
#            curses.curs_set(0)
#            stdscr.clear()
#            with open(level, "r") as f:
#                grid = [list(line.rstrip("\n")) for line in f if line.strip()]
#            for y, row in enumerate(grid):
#                stdscr.addstr(y, 0, "".join(row))
#            stdscr.refresh()
#            player_move(stdscr, grid, player_y, player_x)
#