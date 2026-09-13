#!/usr/bin/env python3
import curses
import time 
from pathlib import Path
import random

class Player:
    def __init__(self, start_y, start_x, grid, min_weapon_damage, max_weapon_damage):
        self.eq = {
            "health_potions":3,
            "keys":0,
            "strenght_apples":1,
            }
        self.stamina = 100
        self.key_found = False
        self.eq_open = 0
        self.health = 100
        self.weapon = "basic_sword"
        self.min_hero_damage, self.max_hero_damage = min_weapon_damage, max_weapon_damage
        self.y = start_y
        self.x = start_x
        self.grid = grid
    def key_control(self, stdscr):
        if self.health != 100:
            level_loader
        while True:
            key =  stdscr.getkey()
            if key in ["w", "s", "a", "d"]:
                self.player_move(stdscr, key)
            elif key == "e":
                self.open_inventory(stdscr)
            elif key == " ":
                self.interact(stdscr)

    def player_move(self, stdscr, key):
        prev_x, prev_y = self.x, self.y
        if key == "w":
            self.y = self.y - 1
        elif key == "s":
            self.y = self.y + 1
        elif key == "a":
            self.x = self.x - 1
        elif key == "d":
            self.x =self.x + 1
        wanted_tile = self.grid[self.y][self.x]
        if wanted_tile == "#" or wanted_tile == "c" or wanted_tile == "o":
            self.x, self.y = prev_x, prev_y
            stdscr.addstr(self.y,self.x,"@")
        else:
            stdscr.addstr(prev_y,prev_x,".")
            stdscr.addstr(self.y,self.x,"@" )
        stdscr.refresh()
    def open_inventory(self, stdscr):
        if self.eq_open == 1:
            stdscr.addstr(36,0,"                                                                 ")
            self.eq_open = 0
        else:
            stdscr.addstr(36,0,f"{self.eq}")
            self.eq_open = 1
    def interact(self, stdscr):
        max_x = len(self.grid[0])
        max_y = len(self.grid)
        check_char = [ (-1, -1), (1, -1), (-1, 1), (0, -1), (-1, 0), (0, 1), (1, 0), (1, 1) ]
        for dy, dx in check_char:
            check_x = self.x + dx
            check_y = self.y + dy
            if 0 <= check_y < max_y and 0 <= check_x < max_x:         
                if self.grid[check_y][check_x] == "c":
                    self.open_chest(stdscr)
                    self.grid[check_y][check_x] = "o"
                    self.redraw_map(stdscr)
                    break
    def redraw_map(self, stdscr):
        if self.key_found:
            self.key_found = False
        else:
            stdscr.clear()
            for row_height,row in enumerate(self.grid):
                stdscr.addstr(row_height,0,"".join(row))
            stdscr.addstr(self.y,self.x,"@")
            stdscr.refresh() 
    def open_chest(self, stdscr):
        stdscr.refresh()
        #if random.choice([True, False]):
        if random.randint(1, 5) == 1:
            current_enemy = Enemy(150, 16 , 24)
        else:
            current_enemy = Enemy(85, 8, 12)
        max_x = len(self.grid[0])
        stdscr.addstr(39, 0, "Choose action:")
        stdscr.addstr(40, 0, f"1: Attack")
        stdscr.addstr(41, 0, f"2: Ask on a date")
        stdscr.addstr(42, 0, "3: Sneak")        
        stdscr.refresh()
        while True:
            key = stdscr.getkey()
            if key == "1":
                fight_mechanic(stdscr, self , current_enemy)
                break
            elif key == "2":
                #date_mechanic(stdscr, self)
                break
            elif key == "3":
                #sneak_mechanic(stdscr, self)
                break
            else:
                time.sleep(1)
        #else:
            #self.key_found = True
            #stdscr.addstr(39, 0, "You have found a key")
            #self.eq["keys"] = 1
            

def load_full(file_path):
    return open(Path(file_path), "r")

def start(stdscr):
    curses.curs_set(0)
    welcmsg = load_full("maps/welcome.txt")       
    stdscr.addstr(0, 0, welcmsg.read())
    welcmsg.close()
    stdscr.refresh()
    time.sleep(0.5)
    stdscr.clear()
    testmsg = load_full("maps/game_name.txt")
    stdscr.addstr(0, 0, testmsg.read())
    testmsg.close()
    stdscr.refresh()
    time.sleep(1)
    return 1
def main_menu(stdscr):
    menumsg = load_full("maps/main_menu.txt")
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, menumsg.read())
        menumsg.close()
        stdscr.addstr(14,0, "Type 1 or 2.")
        stdscr.refresh()
        key = stdscr.getkey()
        if key == "1":
            return "Play"
        elif key == "2":
            return "Exit"
        else:
            stdscr.addstr(16,0,"Wrong key, try again")
            stdscr.refresh()
            time.sleep(1)
#fight mechanic part
#other mechanics also
def fight_mechanic(stdscr, hero, enemy):
    stdscr.clear()
    goblin = load_full('maps/goblin.txt')
    border = load_full('maps/border.txt')
    stdscr.addstr(0,0, goblin.read())
    stdscr.addstr(38,0,border.read())
    stdscr.addstr(37,0, f"You have encountered a goblin named {enemy.name}")
    min_dmg, max_dmg = hero.min_hero_damage, hero.max_hero_damage
    bash_damage = min_dmg
    stun_status = 0
    hero_dead = 0
    enemy_attack = random.randint(1, 100)
    current_attack = 1
    if enemy_attack <= 60:
        enemy_attack = 1
    elif enemy_attack > 60 and enemy_attack <= 80:
        enemy_attack = 2
    else:
        enemy_attack = 0 
    while enemy.health_points >= 0:
        if hero.stamina < 95:
            hero.stamina += 10
        elif hero.stamina >= 95:
            hero.stamina = 100
        if hero.stamina >= 50:
            miss_chance = 5
            dmg_multiplier = 1
            crit_chance = 15
        elif hero.stamina < 50 and hero.stamina >= 20:
            miss_chance = 15
            dmg_multiplier = 0,85
            crit_chance = 12
        else:
            miss_chance = 30
            dmg_multiplier = 0,60
            crit_chance = 5
        if enemy_attack == 0:
            current_attack = 0
            msg = f"{enemy.name} draws his weapon back"
            stdscr.addstr(48,1,msg.ljust(75))
        elif enemy_attack == 1:
            current_attack = 1
            insult_generator = enemy.insults[random.randint(1, 14)]  
            msg = f"{enemy.name}: {insult_generator}"
            stdscr.addstr(48,1,msg.ljust(75))
        elif enemy_attack == 2:
            current_attack = 2
            msg = f"{enemy.name}: {random.choice(enemy.defensive_insults)}"
        if current_attack != 0:
            enemy_attack = random.randint(1, 100)
            if enemy_attack <= 60:
                enemy_attack = 1
            elif enemy_attack > 60 and enemy_attack <= 80:
                enemy_attack = 2
            else: 
                enemy_attack = 0
        msg = f"Enemy hp: {enemy.health_points} ; Your hp: {hero.health}; Your stamina: {hero.stamina}"
        stdscr.addstr(39,1, msg.ljust(30))  
        stdscr.addstr(40,1,f"Stab with {hero.weapon}")
        stdscr.addstr(41,1,f"Bash with hilt of {hero.weapon}")
        stdscr.addstr(42,1,f"Use a heal potion. Potions left:{hero.eq["health_potions"]}")
        stdscr.addstr(43,1,f"Pair")
        stdscr.refresh()
        key = stdscr.getkey()
        if hero.health <= 0:
            goblin.close()
            border.close()
            stdscr.clear()
            game_over(stdscr)
            break
        while True:
            miss_attack = random.randint(1,100)
            if key == "1":
                if miss_attack >= miss_chance:
                    attack = random.randint(min_dmg, max_dmg) * dmg_multiplier
                    enemy.health_points = enemy.health_points - attack
                    msg =  f"Your stab dealed {attack}"
                    stdscr.addstr(45,1, msg.ljust(75))
                else:
                    msg =  f"Your Your hand slipped"
                    stdscr.addstr(45,1, msg.ljust(75))
                hero.stamina -= 12
                break
            elif key == "2":
                if miss_attack >= miss_chance:
                    enemy.health_points = enemy.health_points - bash_damage
                    stun_chance = random.randint(35, 100)
                    stun_work = random.randint(1, 100)
                    if stun_work > stun_chance:
                        msg = f"Your bash dealed {bash_damage}"
                        stdscr.addstr(45,1,msg.ljust(75))
                    elif current_attack == 0 or stun_work < stun_chance:
                        msg = f"Your bash dealed {bash_damage} and stunned the enemy"
                        stdscr.addstr(45,1,msg.ljust(75))
                        stun_status = 1
                else:
                    msg = "Your grip was to weak"
                    stdscr.addstr(45,1,msg.ljust(75))
                hero.stamina -= 35
                break
            elif key == "4":
                    
            elif key == "3" and hero.eq["health_potions"] > 0:
                if miss_attack >= miss_chance:
                    hero.eq["health_potions"] = hero.eq["health_potions"] - 1
                    hero.health = hero.health + 100
                    msg = f"You have succesfully healed 100hp"
                    stdscr.addstr(45,1,msg.ljust(75))
                else:
                    hero.eq["health_potions"] = hero.eq["health_potions"] - 1
                    msg = f"Potion fell out of your hands"
                    stdscr.addstr(45,1,msg.ljust(75))
                break
            else:
                if hero.eq["health_potions"] >= 0:
                    msg = "Press another key"
                    stdscr.addstr(45,1,msg.ljust(75))
                else:
                    msg = "No potions left"
                    stdscr.addstr(45,1,msg.ljust(75))
            stdscr.refresh()    
        if current_attack == 0:
            current_attack = 3
            enemy_attack = 1
        elif current_attack == 1:
            dmg = random.randint(enemy.min_damage, enemy.max_damage)
            hero.health = hero.health - dmg
            msg = f"{enemy.name} swings his sword -{dmg} dmg"
            stdscr.addstr(46,1,msg.ljust(75))
        elif current_attack == 3:
            dmg = random.randint(enemy.min_damage, enemy.max_damage) * 2.5
            hero.health = hero.health - dmg
            msg = f"{enemy.name} unleash hell on you -{dmg} dmg"
            stdscr.addstr(46,1,msg.ljust(75))
        else:
            enemy_heal = random.randint(1, 10)
            msg = f"{enemy.name} healed {enemy_heal} hp"
            enemy.health_points = enemy.health_points + enemy_heal
            stdscr.addstr(46,1,msg.ljust(75))
    stdscr.clear()
    dead = load_full('maps/dead.txt')
    stdscr.addstr(0,0,dead.read())
    stdscr.addstr(43,0,"You won")
    stdscr.addstr(44,0,"Press any key to continue...")
    stdscr.refresh()
    stdscr.getkey()
    dead.close()
    goblin.close()
    border.close()

def game_over(stdscr):
    while True:
        msg = load_full("maps/over.txt")
        stdscr.clear()
        stdscr.addstr(0,0,msg.read())
        stdscr.refresh()
        time.sleep(3)
        msg = load_full("maps/again.txt")
        stdscr.clear()
        stdscr.addstr(0,0,msg.read())
        stdscr.refresh()
        time.sleep(3)
        
        
class Enemy:
    def __init__(self, health , min_damage , max_damage):
        self.health_points = health
        self.affection = random.randint(1, 30)
        goblins = {
        1:"Mieczyslaw",
        2:"Geralt",
        3:"Ruby",
        4:"Marcin",
        5:"Szczepan"
        }
        self.insults = {
            1:"Gag the torch! Snuff it, smash it!",
            2:"Mind the tripwire, fool! Push them into the pit!",
            3:"Stab the ankles! Bring the meat low!",
            4:"Watch the swinging steel! Under, go under!",
            5:"Dibs on the copper! Dibs on the pointy hat!",
            6:"Spit the dart! Make the poison crawl in the blood!",
            7:"Drop the grate! Lock them in the hall!",
            8:"Break the shield arm! Swarm the back!",
            9:"Too narrow for your big blade, tall-one! Walls have teeth!",
            10:"Who triggered the darts?! That was our trap, you dung-head!",
            11:"Skin the knuckles, snatch the belt pouch!",
            12:"More coming from the tunnels! Pile on, drag them down!",
            13:"Claw the eyes out! Blind meat don't hit back!",
            14:"Crack the ribs, find the marrow!"
        }
        self.defensive_insults = ["Just me, yes... but the tunnel is tight, and the shiv is tipped with rot",
            "Step on the trigger-stone, tall-thing. Go on. One step.",
            "My hole. My ditch. You fit into the crawlway, but you won't crawl back out.",
            "I don't need a pack to watch you bleed out in the gravel.",
            "Too fat for the crack in the stone. Can't reach me, can't smash me.",
            "One spear, one gap. The dark works for free.",
            "Come closer to the grating. The drop below is deep and hungry.",
            "No brothers left to take a share. All your shiny trinkets stay with me.",
            "The trip-wire hums. Do you hear it? You're standing right over the teeth.",
            "I know where the roof is thin. Swing that blade again, cave it on us both."]
        self.complements = {
            1:"muscular body",
            2:"majestic sword",
            3:"extravagant left ear",
            4:"humor",
            5:"politeness",
        }
        self.name = goblins[(random.randint(1, 5))] 
        self.agree = {
            1:f'{self.name} leans forward, shadows deepening across a sudden smirk. "Then come closer. Let the dark witness how easily you yield to it."',
            2:f'{self.name} rests a hand near the hilt, eyes locking in silent thrill. "A keen eye. Keep looking, and I might show you how gently it cuts."',
            3:f'A subtle, knowing tilt of the chin reveals a concealed secret. {self.name} whispers, "You notice the anomalies the blind fear to touch. I find that dangerous... and alluring."',
            4:f'A low, velvet chuckle breaks across the table. {self.name} raises a glass. "A dangerous confession. Once my defenses breach yours, I never retreat."',
            5:f'Fingers brush across the dark cloth, pausing an inch away. {self.name} replies softly, "Courtly grace is merely the cage. Since you ask so gently, perhaps I will let you inside."'
        }
        self.disagree = {
            1:f'{self.name} sets down the silver goblet with a dull, hollow ring. "Flattery carved from meat and bone moves cutthroats, not me. Eat your bread in silence."',
            2:f'The cold metal stays dormant. {self.name} turns a gaze colder than lead. "You mistake a weapon for an ornament. Such careless eyes rarely keep their sight."',
            3:f'{self.name} pulls the cowl lower, voice dripping like bitter venom. "You gawk at oddities like a carnival jester. The supper is over."',
            4:f'The smile vanishes into an impenetrable mask. {self.name} stares past the flame. "My words are not your entertainment. Do not mistake breathing air for an invitation."',
            5:f'{self.name} recoils into rigid, iron stillness. "You speak of manners while trespassing with your eyes. We have concluded all that was to be shared."'
        }
        self.min_damage, self.max_damage = min_damage, max_damage
    

    ...
def level_loader(stdscr, level, player_y, player_x, min_weapon_damage, max_weapon_damage):
    eq_open = 0
    curses.curs_set(0)
    stdscr.clear()
    with open(level, "r") as f:
        grid = [list(line.rstrip("\n")) for line in f if line.strip()]
    hero = Player(player_y,player_x,grid,min_weapon_damage, max_weapon_damage)
    for y, row in enumerate(grid):
        stdscr.addstr(y, 0, "".join(row))
    stdscr.addstr(hero.y, hero.x, "@")
    stdscr.refresh()
    hero.key_control(stdscr)


   
def main(stdscr):
    dungeons = {
    "1": Path("maps/1.txt")
    }
    player_y = {
        "1": 10,
    }
    player_x = {
        "1": 10,
    }
    weapon_damage = {
        "1": 8
    }
    max_weapon_damage = {
        "1": 12
    } 
    #start(stdscr)
    #game_status = "main_menu"
    #if game_status == "main_menu":
    #    main_menu(stdscr)
    #if game_status == "Exit":
    #    exit
    #elif game_status == "Play":
    for i in range(1, 2):
        i =  str(i)
        level_loader(stdscr, dungeons[i], player_y[i], player_x[i], weapon_damage[i], max_weapon_damage[i])

curses.wrapper(main)
