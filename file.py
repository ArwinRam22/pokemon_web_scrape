#-------------------------------------------------------
#file.py
#Functions to write to a .txt file
#Similar to printing.py, print statements changed to output to file
#-------------------------------------------------------
#Author:            Arwin Ramesan
#Email:             ramesanarwin@gmail.com
#Date Created:      2023-03-21
#Last Modified:     2023-07-15
#-------------------------------------------------------
#Imports
import reformat, re

class text_file:
    def __init__(self, file_name):
        # '*' at start of file name so it appears first in folder
        self.file_name = '*'+file_name+'.txt'
        try:
            f = open(self.file_name, 'x')
        except:
            pass
        
    def write_to_file(self, output):        
        with open(self.file_name,"w+") as f:
            f.write(output)
            f.close()
    def append_to_file(self, output):
        with open(self.file_name,"a+") as f:
            f.write(output)
            f.close()

def output_basic_table(starting_pokemon, vitals, forms):
    form_number = 1
    iterations = 0
    num_tables = 4

    for vital in vitals:
        if (iterations % num_tables == 0 or iterations == 0):
            if (len(forms)-2 == 1):
                output_file = text_file(starting_pokemon.capitalize() + " Information")
                output_file.write_to_file('<'*25 + " " + starting_pokemon.upper() + " " + '>'*25)
            else: # Mod by 4 since only displaying 4 tables
                output_file = text_file(forms[form_number].capitalize() + " Informations")
                output_file.write_to_file('<'*25 + " " + forms[form_number].upper() + " " + '>'*25)
                form_number += 1

        output_basic_table_aux(vital, output_file)            
        iterations += 1

def output_basic_table_aux(vital, output_file):
    formatting_required = ['Type', 'Abilities', 'Local №']

    rows = vital.find_all('tr')
    for row in rows:
        header = row.find('th').text
        data = row.find('td').text
        data = reformat.replace(data, '\n', "")
        if header not in formatting_required:
            output_file.append_to_file(f"{header:>15}: {data}")
        else:
            if (header == 'Type'):
                typing_data = reformat.reformat_type(data)
                output_file.append_to_file(f"{header:>15}: {typing_data}")
            elif (header == 'Abilities'):            
                data = data.replace(' (hidden ability)', '*')
                ability_data = reformat.reformat_ability(data)
                output_file.append_to_file(f"{header:>15}: {ability_data}")
            elif (header == 'Local №'):
                locale_data = reformat.reformat_local_no(data)
                output_file.append_to_file(f"{header:>15}:")
                blank = ""
                for x in locale_data:
                    output_file.append_to_file(f"{blank:>16} {x}")
    output_file.append_to_file('='*50)

def output_move_table(pokemon_name, panels, regions):
    region_count = 1   
    panel_count = 0
    for x in panels:
        #Each region has its own panel
        if (region_count < len(regions)-1):
            excess_panels = output_move_table_aux(pokemon_name, panels[panel_count], regions[region_count])
            panel_count += excess_panels
            region_count += 1

        #remaining panels are breeding and egg move information

def output_move_table_aux(pokemon_name, current_panel, current_region):
    current_region = reformat.replace(current_region, '/', '-')
    output_file = text_file(pokemon_name.capitalize() + " (" + current_region + ") Moves")
    
    output_file.write_to_file('<'*25 + " " + current_region + " " + '>'*25)
            
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
        if (len(all_tables) > 0):   #Pokemon that don't learn any moves in a certain game will have 0 tables
            output_file.append_to_file(headers[header_count].text)
            output_file.append_to_file("   " + paragraphs[header_count].text)
            if ('the' in paragraphs[header_count].text):
                output_file.append_to_file('-'*50)

            
                #Current section has 1+ tabs, so multiple tables under same header
                if (len(tables_w_tabs) > 0 and len(tables_w_tabs) > table_w_tabs_count and tables_w_tabs[table_w_tabs_count].find('table', class_ = 'data-table').text in all_tables[table_count].text):

                    #Determines other forms for current section
                    forms = tables_w_tabs[table_w_tabs_count].find('div', class_ = 'sv-tabs-tab-list').text
                    forms = reformat.split_with(forms, '[a-z][A-Z]', '_')
                    forms = forms.split('_')

                    for form in forms:
                        output_file.append_to_file(headers[header_count].text + ' - ' + form)
                        output_file.append_to_file("   " + paragraphs[header_count].text)
                        output_file.append_to_file('-'*50)
                        moves = all_tables[table_count].find_all('tr')
                        #First element holds header of table
                        moves.pop(0)
                        output_move(moves, headers[header_count].text, output_file)

                        #table_count += len(forms)
                        table_count += 1
                    table_w_tabs_count += 1

                #Current section has 1 tab, so just 1 table in header
                else:
                    moves = all_tables[table_count].find_all('tr')
                    #First element holds header of table
                    moves.pop(0)
                    output_move(moves, headers[header_count].text, output_file)
                    table_count += 1
            output_file.append_to_file('='*50)
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

def output_move(moves, header, output_file):
    for move in moves:
        numbers = move.find_all('td', class_ = 'cell-num')
        
        if (header != 'Egg moves' and header != 'Move Tutor moves' and header != 'Transfer-only moves' and header != 'Pre-evolution moves'):
            level_learned = numbers[0].text
            temp = "Level: "
            output_file.append_to_file(f"{temp:>15}: {level_learned}")

        name = move.find('td', class_ = 'cell-name').text
        temp = "Move Name: "
        output_file.append_to_file(f"{temp:>15}: {name}")

        type = move.find('td', class_ = 'cell-icon').text
        temp = "Type: "
        output_file.append_to_file(f"{temp:>15}: {type}")

        category = re.findall('[A-Z][a-z]*', str(move.find('td', class_ = 'cell-icon text-center')))
        temp = "Category: "
        output_file.append_to_file(f"{temp:>15}: {category[0]}")
        
        if (header != 'Egg moves' and header != 'Move Tutor moves' and header != 'Transfer-only moves' and header != 'Pre-evolution moves'):
            power = numbers[1].text
            temp = "Power: "
            output_file.append_to_file(f"{temp:>15}: {power}")

            accuracy = numbers[2].text
            temp = "Accuracy: "
            output_file.append_to_file(f"{temp:>15}: {accuracy}")
        else:
            power = numbers[0].text
            temp = "Power: "
            output_file.append_to_file(f"{temp:>15}: {power}")

            accuracy = numbers[1].text
            temp = "Accuracy: "
            output_file.append_to_file(f"{temp:>15}: {accuracy}")
        if (header == 'Transfer-only moves'):
            method = move.find('td', class_ = 'text-small').text
            temp = "Method: "
            output_file.append_to_file(f"{temp:>15}: {method}")

        output_file.append_to_file("")

###
#Following methods are used to export data compactly in text files
###
def output_battle_info(starting_pokemon, vitals, forms):
    form_number = 1
    iterations = 0
    num_tables = 4

    output_file = text_file("Battle Information")

    for vital in vitals:
        if (iterations % num_tables == 0 or iterations == 0):
            if (len(forms)-2 == 1):
                output_file.append_to_file(starting_pokemon.upper() + '#')
            else:
                if (starting_pokemon.lower() in forms[form_number].lower()):
                    output_file.append_to_file(forms[form_number].upper() + '#')
                else:
                    output_file.append_to_file(starting_pokemon.upper() + " (" + forms[form_number].upper() + ')#')
                form_number += 1

        output_battle_info_aux(vital, output_file)            
        iterations += 1

def output_battle_info_aux(vital, output_file):
    formatting_required = ['Type', 'Abilities', 'Local №']
    
    battle_information = ['National №', 'Type', 'Abilities', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

    rows = vital.find_all('tr')

    for row in rows:
        header = row.find('th').text
        data = row.find('td').text

        if (header in battle_information):
            data = reformat.replace(data, '\n', "")
            if header not in formatting_required:
                output_file.append_to_file(f"{data}" + '#')
            else:
                if (header == 'Type'):
                    typing_data = reformat.reformat_type(data)
                    output_file.append_to_file(f"{typing_data}" + '#')
                elif (header == 'Abilities'):            
                    data = data.replace(' (hidden ability)', '*')
                    ability_data = reformat.reformat_ability(data)
                    output_file.append_to_file(f"{ability_data}" + '#')
                elif (header == 'Local №'):
                    locale_data = reformat.reformat_local_no(data)
                    for x in locale_data:
                        output_file.append_to_file(f"{x}" + '#')
        if (header == 'Speed'): #Last element in battle_information
            output_file.append_to_file(f"\n")

def output_all_moves_table(table, generation):
    if (generation.lower() == 'all'):
        output_file = text_file("All Moves")
    else:
        output_file = text_file(f"Gen {generation} Moves")
    output_file.write_to_file("")
    rows = table.find_all('tr')
    for move in rows:    
        name = move.find('td', class_ = 'cell-name').text
        output_file.append_to_file(f"{name}#")

        type = move.find('td', class_ = 'cell-icon').text
        output_file.append_to_file(f"{type}#")

        category = re.findall('[A-Z][a-z]*', str(move.find('td', class_ = 'cell-icon text-center')))
        if (len(category) > 0):
            output_file.append_to_file(f"{category[0]}#")
        else:
            category = '-'
            output_file.append_to_file(f"{category}#")

        numbers = move.find_all('td', class_ = 'cell-num')
        power = numbers[0].text
        output_file.append_to_file(f"{power}#")

        accuracy = numbers[1].text
        output_file.append_to_file(f"{accuracy}#")

        power_points = numbers[2].text
        output_file.append_to_file(f"{power_points}#")

        effect = move.find('td', class_ = 'cell-long-text').text
        output_file.append_to_file(f"{effect}#\n")

def output_all_abilities(table):
    output_file = text_file("All Abilities")
    output_file.write_to_file("")
    body = table.find('tbody')
    rows = body.find_all('tr')
    for ability in rows:
        name = ability.find(class_ = 'ent-name').text
        output_file.append_to_file(f"{name}#")

        count = ability.find(class_ = 'cell-num cell-total').text
        output_file.append_to_file(f"{count}#")

        desc = ability.find(class_ = 'cell-med-text').text
        output_file.append_to_file(f"{desc}#")

        generation = ability.find(class_ = 'cell-num').text
        output_file.append_to_file(f"{generation}#\n")