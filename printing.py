#-------------------------------------------------------
#printing.py
#Functions to output vitals tables
#-------------------------------------------------------
#Author:            Arwin Ramesan
#Email:             ramesanarwin@gmail.com
#Date Created:      2023-03-21
#Last Modified:     2023-07-15
#-------------------------------------------------------

#Imports
import reformat
import re
#####################################################################################################################
# Sends each table to the auxiliary method
    # Parameters
        #   (String)    starting_pokemon    = the name of the Pokemon
        #   (String[])  vitals              = list of tables that hold information of pokemon
        #   (String[])  forms               = list of different forms of the pokemon
def print_basic_info(starting_pokemon, vitals, forms):
    form_number = 1 # Starting index for 'forms'
    iterations = 0  # Number of iterations
    num_tables = 4  # Number of tables
    # Data from the following headers require formatting before printing
        # formatting_required = ['Type', 'Abilities', 'Local №']  
    
    for vital in vitals:
        if (iterations % num_tables == 0 or iterations == 0): # Mod by 4 since only displaying 4 tables
            if (len(forms)-2 == 1): #if Pokemon has no other forms (eg. Bulbasaur, Charmander, etc.)
                print('<'*25 + f' {starting_pokemon.upper()} ' + '>'*25)
            else:
                print('<'*25 + f' {forms[form_number].upper()} ' + '>'*25)
                form_number += 1

        # Data of all rows in the current table
        rows = vital.find_all('tr')

        # Prints each row individually
        for row in rows:
            header = row.find('th').text
            data = row.find('td').text
            data = reformat.replace(data, '\n', "")

            if (header == 'Local №'):
                locale_data = reformat.reformat_local_no(data)
                print(f"{'Local №':>15}:")
                for x in locale_data:
                    print(f"{'':>16} {x}")
            else:
                if (header == 'Type'):          data = reformat.reformat_type(data)
                elif (header == 'Abilities'):   data = reformat.reformat_ability(data.replace(' (hidden ability)', '*'))
                print(f"{header:>15}: {data}")

        if (len(forms)-2 == 1):
            print('='*(50 + len(starting_pokemon)+2))
        else:
            print('='*(50 + len(forms[form_number])+2))
        iterations += 1
    
#####################################################################################################################
#Prints the Pokemon's moves
# Parameters
#   (String)    pokemon_name        = the name of the pokemon
#   (String[])  panels              = list of tables that hold information of pokemon and other forms
#   (String[])  forms               = list of different forms of the pokemon
#   (String[])  regions             = list of different regions in the generation
def print_move_table(pokemon_name, generation, panels, regions):
    print('<'*25 + f' {pokemon_name.upper()} - {generation}' + '>'*25)

    region_count = 1   
    panel_count = 0
    for x in panels:
        #Each region has its own panel
        if (region_count < len(regions)-1):
            current_region = regions[region_count]
            current_panel = panels[panel_count]
            excess_panels = print_move_table_aux(current_panel, current_region)
            panel_count += excess_panels
            region_count += 1

#Prints the Pokemon's moves
# Parameters
#   (String)    current_panel   = section of html holding numerous move tables
#   (String)    current_region  = name of region for current tables
def print_move_table_aux(current_panel, current_region):
    print('<'*25 + f'{current_region}' + '>'*25)
            
    #All tables in panel
    all_tables = current_panel.find_all('table', class_ = 'data-table')
    #All tables with tabs
    tables_w_tabs = current_panel.find_all('div', class_ = 'tabset-moves-game-form sv-tabs-wrapper')
    #Headers for the tables
    headers = current_panel.find_all('h3')
    #Description for the tables            
    paragraphs = current_panel.find_all('p')

    header_count = 0
    table_count = 0
    table_w_tabs_count = 0
    for header in headers:
        if (len(all_tables) > 0):
            print(headers[header_count].text)
            print(f'\t{paragraphs[header_count].text}')
            if ('the' in paragraphs[header_count].text):
                print('-'*50)
                #Current section has 1+ tabs, so multiple tables under same header
                if (len(tables_w_tabs) > 0 and len(tables_w_tabs) > table_w_tabs_count and tables_w_tabs[table_w_tabs_count].find('table', class_ = 'data-table').text in all_tables[table_count].text):

                    #Determines other forms for current section
                    forms = tables_w_tabs[table_w_tabs_count].find('div', class_ = 'sv-tabs-tab-list').text
                    forms = reformat.split_with(forms, '[a-z][A-Z]', '_')
                    forms = forms.split('_')

                    for form in forms:
                        print(headers[header_count].text + ' - ' + form)
                        print(f'\t{paragraphs[header_count].text}')
                        print('-'*50)
                        moves = all_tables[table_count].find_all('tr')
                        #First element holds header of table
                        moves.pop(0)
                        print_move(moves, headers[header_count].text)

                        #table_count += len(forms)
                        table_count += 1
                    table_w_tabs_count += 1

                #Current section has 1 tab, so just 1 table in header
                else:
                    moves = all_tables[table_count].find_all('tr')
                    #First element holds header of table
                    moves.pop(0)
                    print_move(moves, headers[header_count].text)
                    table_count += 1
            print('='*50)
        header_count += 1
    
    excess_panels = 0
    if len(tables_w_tabs) > 0:
        for t_w_t in tables_w_tabs:
            tabs = t_w_t.find('div', class_ = 'sv-tabs-tab-list')
            excess_panels += len(tabs)-1
        excess_panels += 1
    else:
        excess_panels = 1

    return excess_panels

#Prints each move in a table
# Parameters
#   (String[])    moves        = table of moves
#   (String)  header              = header of table
def print_move(moves, header):
    for move in moves:
        numbers = move.find_all('td', class_ = 'cell-num')
        if (header != 'Egg moves' and header != 'Move Tutor moves' and header != 'Transfer-only moves' and header != 'Pre-evolution moves'):
            level_learned = numbers[0].text
            power = numbers[1].text
            accuracy = numbers[2].text
            print(f"{'Level':>15}: {level_learned}")
        else:
            power = numbers[0].text
            accuracy = numbers[1].text

        name = move.find('td', class_ = 'cell-name').text
        type = move.find('td', class_ = 'cell-icon').text
        category = re.findall('[A-Z][a-z]*', str(move.find('td', class_ = 'cell-icon text-center')))
        
        print(f"{'Move Name':>15}: {name}")
        print(f"{'Type':>15}: {type}")
        print(f"{'Category':>15}: {category[0]}")
        print(f"{'Power':>15}: {power}")
        print(f"{'Accuracy':>15}: {accuracy}")
        if (header == 'Transfer-only moves'):
            method = move.find('td', class_ = 'text-small').text
            print(f"{'Method':>15}: {method}")
        print()

#####################################################################################################################
#Prints table containing list of all moves
# Parameters
#   (String)    table        = table containing all moves
def print_all_moves_table(table):
    rows = table.find_all('tr')
    for move in rows:    
        name = move.find('td', class_ = 'cell-name').text
        type = move.find('td', class_ = 'cell-icon').text
        category = re.findall('[A-Z][a-z]*', str(move.find('td', class_ = 'cell-icon text-center')))
        numbers = move.find_all('td', class_ = 'cell-num')
        power = numbers[0].text
        accuracy = numbers[1].text
        power_points = numbers[2].text
        effect = move.find('td', class_ = 'cell-long-text').text

        print(f"{'Move Name':>15}: {name}")        
        print(f"{'Type':>15}: {type}")
        if (len(category) > 0):
            print(f"{'Category':>15}: {category[0]}")
        else:
            category = '-'
            print(f"{'Category':>15}: {category}")        
        print(f"{'Power':>15}: {power}")
        print(f"{'Accuracy':>15}: {accuracy}")
        print(f"{'PP':>15}: {power_points}")        
        print(f"{'Effect':>15}: {effect}\n")

#####################################################################################################################
#Prints table containing list of all abilities
# Parameters
#   (String)    table        = table containing all abilities
def print_all_abilities(table):
    body = table.find('tbody')
    rows = body.find_all('tr')
    for ability in rows:
        name = ability.find(class_ = 'ent-name').text
        count = ability.find(class_ = 'cell-num cell-total').text
        desc = ability.find(class_ = 'cell-med-text').text
        generation = ability.find_all(class_ = 'cell-num')
        
        print(f"{'Name':>15}: {name}")
        print(f"{'Description':>15}: {desc}")
        print(f"{'Count':>15}: {count}")
        print(f"{'Generation':>15}: {generation[1].text}\n")