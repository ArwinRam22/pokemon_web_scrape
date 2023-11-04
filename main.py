"""
main.py
Driver class
-------------------------------------------------------
Author:            Arwin Ramesan
Email:             ramesanarwin@gmail.com
Date Created:      2023-03-21
Last Modified:     2023-11-04
"""

#Imports
import webscrape
import file
import reformat

#Variables
END = False

while END is False:
    print('''
    0 = Quit
    1 = Pokemon's Information (Pokédex Data, Training, Breeding, Stats)
    2 = Pokemon's Moves (Learned By Levelup, Learned By Evolution, Egg Moves, TM, TR) 
    
    97 = Output All Abilities
    98 = Output All Moves
    99 = Output Battle Information
    ''')
    choice = input("What would you like to search for: ")

    if choice in ('1', '2', '99'):
        pokemon_choice = input("What Pokemon would you like to search for: ")
        formattedPokemon_Choice = reformat.pokemon_name_changer(pokemon_choice)

        if choice == '2':
            generation = input("Which generation for moves learned: ")

    if choice == '98':
        move_generation = input("Which generation for moves learned (1-9) or 'all': ")

    if choice == '1':
        webscrape.web_scrape_basics(formattedPokemon_Choice, False)

    elif choice == '2':
        webscrape.web_scrape_moves(formattedPokemon_Choice, generation)

    elif choice == '97':
        webscrape.web_scrape_all_abilities()

    elif choice == '98':
        webscrape.web_scrape_all_moves(move_generation)

    elif choice == '99':
        output_file = file.text_file("Basic Information")
        output_file.write_to_file("")
        numOfPokemon = int(input("How many Pokemon would you like to web-scrape?: "))
        currentPokemon = formattedPokemon_Choice
        for eachPokemon in range(numOfPokemon):
            webscrape.web_scrape_basics(currentPokemon, True)
            formattedPokemon_Choice = webscrape.find_next_pokemon(currentPokemon)
            print(f'{currentPokemon} finished.')
            currentPokemon = formattedPokemon_Choice
    else:
        END = True
