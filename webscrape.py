"""
-------------------------------------------------------
webscrape.py
Functions to pull information from html
-------------------------------------------------------
Author:            Arwin Ramesan
Email:             ramesanarwin@gmail.com
Date Created:      2023-03-21
Last Modified:     2023-11-04
-------------------------------------------------------
"""
#Imports
from bs4 import BeautifulSoup
import requests

import printing
import reformat
import file

BASE_URL    = 'https://pokemondb.net/pokedex/'
MOVE_URL    = 'https://pokemondb.net/move/'
ABILITY_URL = 'https://pokemondb.net/ability'
def valid_url(soup):
    """ Returns if url is valid """
    valid = True
    proof = soup.find('h1')
    if proof.text == "Page not found":
        valid = False
    return valid
def soup_creator(url):
    """ Returns valid soup or -1 """
    #Gets access to link's html data
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    if valid_url(soup):
        return soup
    print(f'Page not found: {url}')
    return -1

def web_scrape_basics(pokemon_name, boolean_battle_info_export):
    """
    Parameters
        (String) pokemon_name = Pokemon name entered by user
        (Boolean) boolean_output =  True => user wants output on .txt file, 
                                    False => user does not want output on .txt file
    
    """
    #Determines the link of the Pokémon
    url = BASE_URL + pokemon_name
    soup = soup_creator(url)
    if soup != -1:
        #Section of website with required information
        panel = soup.find('div', class_ = 'sv-tabs-panel-list')

        #list of all 'table' elements where class is 'vitals-table' in 'panel'
        #   --> Pokemon's information is listed in these tables
        vitals = panel.find_all('table', class_ = 'vitals-table')

        #list of all (if any) forms of the Pokemon
        #   --> e.g. Wooper has 2 forms => [Wooper, Paldean Wooper]
        #Note: First and last value is '\n'
        forms = soup.find('div', class_ = 'sv-tabs-tab-list').text.split('\n')

        if boolean_battle_info_export:
            file.condensedBasicInfo(pokemon_name.capitalize(), vitals, forms)
        else:
            printing.print_basic_info(pokemon_name.capitalize(), vitals, forms)

            # writeToTxt = input("Write to a text file? (y/n): ")
            # if writeToTxt.lower() is 'y':
            #     file.output_basic_info(pokemon_name.capitalize(), vitals, forms)


def web_scrape_all_moves(generation):
    """
    Parameters
        (String) generation = Number from 1-9 or 'all'
    """
    if generation.lower() == 'all':
        new_move_url = MOVE_URL + generation
    else:
        new_move_url = MOVE_URL + 'generation/' + generation
    soup = soup_creator(new_move_url)
    if soup != -1:
        table = soup.find('tbody')
        printing.print_all_moves_table(table)
        file.output_all_moves_table(table, generation)

def web_scrape_all_abilities():
    """ Webscrapes abilities from all generations """
    soup = soup_creator(ABILITY_URL)
    if soup != -1:
        table = soup.find('table', class_ = 'data-table sticky-header block-wide')
        printing.print_all_abilities(table)
        file.output_all_abilities(table)


def web_scrape_moves(pokemon_name, generation):
    """
    Webscrapes moves from specified generation or all moves
        Parameters
            (String) pokemon_name = Name of pokemon to search moveset
            (String) generation = Generation of which moves learned 
            (Boolean) boolean_output = True if user wants to output results onto text file
    """
    url = BASE_URL + pokemon_name + '/moves/' + generation
    soup = soup_creator(url)
    if soup != -1:
        #Regions in the generation chosen
        regions = soup.find('div', class_ = 'sv-tabs-tab-list').text.split('\n')
        panels = soup.find_all('div', class_ = 'sv-tabs-panel')

        printing.print_move_table(pokemon_name, generation, panels, regions)
        write_to_txt = input("Write to a text file? (y/n): ")
        if write_to_txt.lower() == 'y':
            file.output_move_table(pokemon_name, panels, regions)


def find_next_pokemon(pokemon_name):
    """
    Finds the next Pokemon based on National Dex number
        Parameters
            (String) pokemon_name = Name of Pokemon
        Return
            (String) next_pokemon = Name of next Pokemon
    """
    url = BASE_URL + pokemon_name
    soup = soup_creator(url)
    next_pokemon = ""
    if soup != -1:
        #1st Pokemon (Bulbasaur) has a different page layout that the rest
        if pokemon_name.lower() == 'bulbasaur':
            next_pokemon = soup.find('nav', class_ = 'entity-nav component')
            next_pokemon = next_pokemon.text.replace('\n', '')
        else:
            next_pokemon_finder = soup.find('nav', class_ = 'entity-nav component')
            splitter = next_pokemon_finder.text.split('\n')
            if len(splitter) > 2:
                next_pokemon = splitter[2]

        if next_pokemon is not None:
            next_pokemon = reformat.pokemon_name_changer(next_pokemon[6:].lower())
    return next_pokemon
