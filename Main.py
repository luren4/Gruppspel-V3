import random
from unittest import skip
import Chest_system
import Grafik_system
import potion_system
import Combat_system
import time


#Startvärden för spelaren
# class player:
#     playerWeapon = 100
#     playerArmor = 100
#     playerHealth = 100
#     playerRing = 1
#     playerLevel = 1



playerWeapon = 100
playerArmor = 100
playerHealth = 100
playerRing = 1
playerLevel = 1
potionlist = []




#Välkommst medelande ________________________________________________________________
Grafik_system.welcometext()
time.sleep(2)
try:
    keepgoing = 1
    while keepgoing == 1:
        #Kista ______________________________________________________________________________

        #Här finner spelaren en kista som tar fram tre nya möjliga accesory val
        new_weapon, new_armor, new_ring = Chest_system.foundchest(playerWeapon, playerArmor, playerRing, playerLevel)

        #Här displayas nuvarande men även de nya hitttade accesoriesen
        Grafik_system.foundchesttext(new_weapon, new_armor, new_ring, playerWeapon, playerArmor, playerRing, playerHealth, playerLevel)

        #Här väljer spelaren bland de tre nya möjliga valen
        
        NewAcessoryChoice = int(input("Välj ditt val --->  "))
        


        #Här tillsätts det nya valet i spelarens inventory
        playerWeapon, playerArmor, playerRing = Chest_system.chestchoice(new_weapon, new_armor, new_ring, playerWeapon, playerArmor, playerRing, NewAcessoryChoice)
        playerLevel += 1



        #Potion _____________________________________________________________________________________
        #Här slumpas chansen om spelaren ska få en ny potion eller inte
        if potion_system.chance_to_give_potion(playerLevel) == True:
            #Här slumpas potionens typ fram av potionsystenet
            potiontype = potion_system.give_potion()
            #Här läggs potiontypen till i spelarens potionlista
            potionlist.append(potiontype)
            Grafik_system.You_found_a_potion(potiontype)
            time.sleep(2)




        



        #Monster ______________________________________________________________________________
        #Här har spelaren chans att skippa att hamna i combat
        if random.randint(1, 10) == 10:
            Grafik_system.Dodged_enemy()
            time.sleep(4)
            skipcombat = True
            
        else:
            #Här finner spelaren ett monster med delvist slumpad attack och damage beroende level
            enemyAttack, enemyHealth = Combat_system.found_enemy(playerLevel)
            Grafik_system.Found_enemy(enemyAttack, enemyHealth)
            time.sleep(3)
            skipcombat = False

            #Här ges spelaren en random attack multiplier


        incombat = True
        enemyAlive = True
        if skipcombat == False:
            while incombat == True:
                
                #Här ges spelaren en random attack multiplier
                attackMultiplier = Combat_system.Roll_dice()
                Grafik_system.Dice_roll(attackMultiplier, playerWeapon, playerRing)
                time.sleep(4)

                if Combat_system.Damage_enemy(playerWeapon, attackMultiplier, playerRing) > enemyHealth:
                    Grafik_system.Enemy_struck()
                    Grafik_system.Killed_enemy()
                    input("Press enter to move on...  ")
                    incombat = False
                
                else: 
                    enemyHealth = enemyHealth - Combat_system.Damage_enemy(playerWeapon, attackMultiplier, playerRing)
                    Grafik_system.Enemy_struck()
                    Grafik_system.Enemy_Survived(enemyHealth)


                    if len(potionlist) > 0:
                        Grafik_system.Potion_inventory_show(potionlist)
                        potionChoose = True
                        while potionChoose == True:
                            if int(input("Would you like to use a potion? Yes => 1, no=> 2 --> ")) == 1:
                                Grafik_system.Potion_inventory_choice(potionlist)
                                potionChoice = int(input("wich potion type would you like to use?"))
                                if  potionlist.count(potionChoice) > 0:
                                    potionlist.remove(potionChoice)

                                    potionChoose = False
                                    if potionChoice == 1:
                                        heal = round( 100 * (0.1 * playerLevel + 1), 2)
                                        playerHealth = playerHealth + heal
                                        Grafik_system.You_used_a_healing_potion(heal, playerHealth)
                                        input("Press enter to move on...  ")

                                    if potionChoice == 2:
                                        enemyHealth = enemyHealth - 100   
                                        Grafik_system.You_used_a_damage_potion()
                                        if enemyHealth < 0:
                                            Grafik_system.Killed_enemy()
                                            input("Press enter to move on...  ")
                                            incombat = False
                                            enemyAlive = False
                                        else:
                                            Grafik_system.Enemy_Survived(enemyHealth)

                                    if potionChoice == 3:
                                        Grafik_system.You_used_an_attack_again_potion()
                                        input("Press enter to move on...  ")

                                        
                                        if Combat_system.Damage_enemy(playerWeapon, attackMultiplier, playerRing) > enemyHealth:
                                            Grafik_system.Enemy_struck()
                                            Grafik_system.Killed_enemy()
                                            input("Press enter to move on...  ")
                                            incombat = False
                                            enemyAlive = False
                                        else: 
                                            enemyHealth = enemyHealth - Combat_system.Damage_enemy(playerWeapon, attackMultiplier, playerRing)
                                            Grafik_system.Enemy_struck()
                                            Grafik_system.Enemy_Survived(enemyHealth)
                                else:
                                    Grafik_system.Potion_missing()
                            else:
                                potionChoose = False


                    if enemyAlive == True:
                        if enemyAttack > playerArmor:
                            playerHealth = Combat_system.Damage_player(enemyAttack, playerArmor, playerHealth)
                            if playerHealth < 0:
                                Grafik_system.Player_died()
                                time.sleep(5) 
                                exit()
                            else:
                                Grafik_system.Player_lost_health(playerHealth)
                                time.sleep(5)
                        else:
                            Grafik_system.Enemy_didnt_pierce_armor(enemyAttack, playerArmor)
                            time.sleep(5)
except:
    print("invalid input")                    



