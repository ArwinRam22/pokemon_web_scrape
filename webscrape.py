#-------------------------------------------------------
#webscrape.py
#Functions to pull information from html
#-------------------------------------------------------
#Author:            Arwin Ramesan
#Email:             ramesanarwin@gmail.com
#Date Created:      2023-03-21
#Last Modified:     2023-07-15
#-------------------------------------------------------

#Imports
from bs4 import BeautifulSoup
import requests

import printing
import reformat
import file

#####################################################################################################################
#Validates the 'soup' object
    # Parameters
        #(Object)    soup    = HTML file of link of Pokemon entered by user
    #Return
        #(Boolean)   valid   => False if user entered non-existing Pokemon name, True if user entered valid Pokemon name
def valid_url(soup):
    valid = True

    proof = soup.find('h1')
    if (proof.text == "Page not found"):
        valid = False
        print("Page not found")
    return valid

#####################################################################################################################
#Changes pokemon_name into name for URL
    # Parameters
        #(String)    pokemon_name       = Name of Pokemon
    #Return
        #(String)    new_pokemon_name   = Modified Name suitable for URL
def pokemon_name_changer(pokemon_name):
    new_pokemon_name = reformat.replace(pokemon_name, ' ', '-')
    new_pokemon_name = reformat.replace(pokemon_name, '.', '')
    new_pokemon_name = reformat.replace(pokemon_name, '♀', '-f')
    new_pokemon_name = reformat.replace(pokemon_name, '♂', '-m')
    new_pokemon_name = reformat.replace(pokemon_name, 'é', 'e')
    new_pokemon_name = reformat.replace(pokemon_name, ':', '')
    new_pokemon_name = reformat.replace(pokemon_name, '\'', '')

    return new_pokemon_name

#####################################################################################################################
#Webscrapes following information:
    #Pokedex Data
        #Pokedex Number
        #Typing
        #Species
        #Height
        #Weight
        #Abilities
        #Local Number
    #Training
        #EV Yield
        #Catch Rate
        #Base Friendship
        #Base EXP
        #Growth Rate
    #Breeding
        #Egg Groups
        #Gender
        #Egg Cycles
    #Base Stats
        #HP
        #Attack
        #Defence
        #Special Attack
        #Special Defence
        #Speed
# Parameters
    #(String)   pokemon_name    = Pokemon name entered by user
    #(Boolean)  boolean_output  = True = user wants output on .txt file, False = user does not want output on .txt file

def web_scrape_basics(pokemon_name, boolean_output, boolean_export):
    #Determines the link of the Pokémon
    base_url = 'https://pokemondb.net/pokedex/'
    new_pokemon_name = pokemon_name_changer(pokemon_name)
    url = base_url + new_pokemon_name
    
    #Gets access to link's html data
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    if valid_url(soup):
        
        #Section of website with required information
        panel = soup.find('div', class_ = 'sv-tabs-panel-list')
        
        #list of all 'table' elements where class is 'vitals-table' in 'panel'
        #   --> Pokemon's information is listed in these tables
        vitals = panel.find_all('table', class_ = 'vitals-table')
        
        #list of all (if any) forms of the Pokemon
        #   --> e.g. Wooper has 2 forms => [Wooper, Paldean Wooper]
        forms = soup.find('div', class_ = 'sv-tabs-tab-list').text.split('\n')  #Note: First and last value is '\n'

        if (boolean_export):
            file.output_battle_info(pokemon_name.capitalize(), vitals, forms)
        else:
            printing.print_basic_info(pokemon_name.capitalize(), vitals, forms)
            if (boolean_output):                
                file.output_basic_table(pokemon_name.capitalize(), vitals, forms)

#####################################################################################################################
#Webscrapes moves from specified generation or all moves
    # Parameters
        #(String)    generation       = Number from 1-9 or 'all'
def web_scrape_all_moves(generation):
    url = 'https://pokemondb.net/move/'
    if (generation.lower() == 'all'):
        url += generation
    else:
        url += 'generation/' + generation
    #Gets access to link's html data
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    if (valid_url(soup)):
        table = soup.find('tbody')
        printing.print_all_moves_table(table)
        file.output_all_moves_table(table, generation)

#####################################################################################################################
#Webscrapes abilities from all generations
def web_scrape_all_abilities():
    url = 'https://pokemondb.net/ability'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    if (valid_url):
        table = soup.find('table', class_ = 'data-table sticky-header block-wide')
        printing.print_all_abilities(table)
        file.output_all_abilities(table)

#####################################################################################################################
#Webscrapes moves from specified generation or all moves
    # Parameters
        #(String)    pokemon_name       = Name of pokemon to search moveset
        #(String)    generation       = Generation of which moves learned 
        #(Boolean)    boolean_output       = True if user wants to output results onto text file
def web_scrape_moves(pokemon_name, generation, boolean_output):
    #Determines the link of the Pokémon
    starting_url = 'https://pokemondb.net/pokedex/'
    ending_url = '/moves/'    
    new_pokemon_name = pokemon_name_changer(pokemon_name)
    url = starting_url + new_pokemon_name + ending_url + generation
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    if valid_url(soup):
        #Regions in the generation chosen
        regions = soup.find('div', class_ = 'sv-tabs-tab-list').text.split('\n')
        panels = soup.find_all('div', class_ = 'sv-tabs-panel')
        
        printing.print_move_table(pokemon_name, generation, panels, regions)
        if (boolean_output):
            file.output_move_table(pokemon_name, panels, regions)

#####################################################################################################################
#Finds the next Pokemon based on National Dex number
    # Parameters
        #(String)    pokemon_name       = Name of Pokemon
    #Return
        #(String)    next_pokemon   = Name of next Pokemon
def find_next_pokemon(pokemon_name):

    #Determines the link of the Pokémon
    base_url = 'https://pokemondb.net/pokedex/'
    new_pokemon_name = pokemon_name_changer(pokemon_name)
    url = base_url + new_pokemon_name
    
    #Gets access to link's html data
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    if valid_url(soup):
        #Go to next Pokemon using website HTML
        if pokemon_name.lower() == 'bulbasaur':  #1st Pokemon (Bulbasaur) has a different page layout that the rest
            next_pokemon = soup.find('nav', class_ = 'entity-nav component')
            next_pokemon = next_pokemon.text.replace('\n', '')
        else:
            next_pokemon_finder = soup.find('nav', class_ = 'entity-nav component')
            splitter = next_pokemon_finder.text.split('\n')
            next_pokemon = splitter[2]

        if (next_pokemon == None):
            return 0

        next_pokemon = next_pokemon[6:].lower()
        return next_pokemon