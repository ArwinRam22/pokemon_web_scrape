#-------------------------------------------------------
#main.py
#Driver class
#-------------------------------------------------------
#Author:            Arwin Ramesan
#Email:             ramesanarwin@gmail.com
#Date Created:      2023-03-21
#Last Modified:     2023-07-15
#-------------------------------------------------------

#Imports
import webscrape, file

#Variables
quit = False

while (quit == False):
    print(f'''
    *1 = Pokemon's Information (Pokédex Data, Training, Breeding, Stats)
    2 = Pokemon's Moves (Learned By Levelup, Learned By Evolution, Egg Moves, TM, TR) 
    
    97 = Output All Abilities
    98 = Output All Moves
    99 = Output Battle Information
    ''')
    choice = input("What would you like to search for: ")
        
    if choice == '1':
        pokemon_choice = input("What Pokemon would you like to search for: ")
        x = input("Write to a text file? (y/n): ")
        if (x == 'y'):
            webscrape.web_scrape_basics(pokemon_choice, True, False)
        else:
            webscrape.web_scrape_basics(pokemon_choice, False, False)

    elif choice == '2':
        pokemon_choice = input("What Pokemon would you like to search for: ")
        generation = input("Which generation for moves learned: ")
        x = input("Write to a text file? (y/n): ")
        if (x == 'y'):
            webscrape.web_scrape_moves(pokemon_choice, generation, True)
        else:
            webscrape.web_scrape_moves(pokemon_choice, generation, False)
        
    elif choice == '97':
        webscrape.web_scrape_all_abilities()

    elif choice == '98':
        generation = input("Which generation for moves learned (1-9) or 'all': ")
        webscrape.web_scrape_all_moves(generation)

    elif choice == '99':
        output_file = file.text_file("Battle Information")
        output_file.write_to_file("")
        pokemon_choice = input("What Pokemon would you like to start at: ")
        x = int(input("How many Pokemon would you like to web-scrape?: "))
        for y in range(x):
            webscrape.web_scrape_basics(pokemon_choice, True, True)
            print(f"{pokemon_choice} complete!\n")
            pokemon_choice = webscrape.find_next_pokemon(pokemon_choice)
       
    else:
        quit = True