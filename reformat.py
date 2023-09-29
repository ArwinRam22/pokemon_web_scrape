#-------------------------------------------------------
#reformat.py
#Functions to reformat strings
#-------------------------------------------------------
#Author:            Arwin Ramesan
#Email:             ramesanarwin@gmail.com
#Date Created:      2023-03-21
#Last Modified:     2023-07-15
#-------------------------------------------------------

#Imports
import re


#####################################################################################################################
#Changes pokemon_name into name for URL
    # Parameters
        #(String)    pokemon_name       = Name of Pokemon
    #Return
        #(String)    new_pokemon_name   = Modified Name suitable for URL
def pokemon_name_changer(pokemon_name):
    replacementCharacters = {
        ' ': '-',
        '.': '',
        '♀': '-f',
        '♂': '-m',
        'é': 'e',
        ':': '',
        '\'': ''
    }
    illegalCharacters = [' ', '.', '♀', '♂', 'é', ':', '\'']

    for x in illegalCharacters:
        if x in pokemon_name:
            pokemon_name = replace(pokemon_name, x, replacementCharacters.get(x))

    return pokemon_name
#####################################################################################################################
# Reformats typing input
# Since Pokemon typing are 1 word, splits the input from uppercase letter to another
    # Parameters
        # (String)  input   = XxxxYyyy or Xxxx
    # Return
        # (List)    result  = [Xxxx, Yyyy] or [Xxxx]

def reformat_type(input):
    # Returns an array of 1 or 2 elements of the Pokémon's typing
    return list_to_string(re.findall('[A-Z][a-z]*', input)) 

#####################################################################################################################
# Expands short form version of typing 
# Returns the typing based on the 3 letter input String
    # Parameters
        # (String) input = First 3 letters of typing
    # Return
        # (String) = Typing Name

def reformat_typing(input):
    typeList = {
        'Nor': 'Normal',
        'Fir': 'Fire',
        'Wat': 'Water',
        'Ele': 'Electric',
        'Gra': 'Grass',
        'Ice': 'Ice',
        'Poi': 'Poison',
        'Gro': 'Ground',
        'Fly': 'Flying',
        'Roc': 'Rock',
        'Dra': 'Dragon',
        'Ste': 'Steel',
        'Psy': 'Psychic',
        'Gho': 'Ghost',
        'Dar': 'Dark',
        'Fig': 'Fighting',
        'Bug': 'Bug',
        'Fai': 'Fairy'
    }

    if (input in typeList.keys()):
        return typeList.get(input)
    elif (input in list(typeList.values)):
        return list(typeList.keys)[list(typeList.values).index(input)]

    return -1

#####################################################################################################################
# Reformats ability input
# Abilities begin with '1. ' or '2. ' or end with '(hidden ability)'
    # Parameters
        # (String)  input   = 1. Xxxx2. YyyyZzzz*
            # Case 1 = 1 ability                        => input = 1. Xxxx
            # Case 2 = 2 abilities                      => input = 1. Xxxx2. Yyyy
            # Case 3 = 2 abilities and hidden ability   => input = 1. Xxxx2. YyyyZzzz*
            # Case 4 = 1 ability and hidden ability     => input = 1. XxxxZzzz*
    # Return
        # (List)  abilities
            # Case 1 = 1 ability                        => abilities = [Xxxx]
            # Case 2 = 2 abilities                      => abilities = [Xxxx, Yyyy]
            # Case 3 = 2 abilities and hidden ability   => abilities = [Xxxx, Yyyy, Zzzz*]
            # Case 4 = 1 ability and hidden ability     => abilities = [Xxxx, Zzzz*]

def reformat_ability(input):
    skip = False
    if (input.find('2') != -1 and input.find('*') != -1):       # Pokemon has 3 possible abilities (hidden ability) e.g. Muk
        # input would look like --> "1. Xxxx2. YyyyZzzz*"
        
        #Removes '*' at end of input
        input_temp = input[:len(input)-1]
        #Splits lowercase letter followed by uppercase letter with '^'
        input_temp = split_with(input_temp, '[a-z][A-Z]', '^')
        #input_temp now looks like --> "1. Xxxx2. Yyyy^Zzzz"
        #Removes 2 with '^'
        input_temp = input_temp[:input_temp.find('2. ')] + '^' + input_temp[input_temp.find('2. ')+1:]
        #input_temp now looks like --> "1. Xxxx^. Yyyy^Zzzz*^"
        #So now, each ability starts with an uppercase letter and ends with a '^'

    elif (input.find('2') != -1):       # Pokemon has 2 possible abilities (no hidden ability) e.g. Zygarde
        #Removes 2 with '^'
        input_temp = input[:input.find('2. ')] + '^' + input[input.find('2. ')+1:]
        
    elif (input.find('*') != -1):       # Pokemon has 2 possible abilities (hidden ability) e.g. Torterra, Froslass
        #Removes '*' at end of input
        input_temp = input[:len(input)-1]
        #Splits lowercase letter followed by uppercase letter with '^'
        input_temp = split_with(input_temp, '[a-z][A-Z]', '^')
        
    elif (input.find('1. ') != -1):     # Pokemon has 1 possible ability (no hidden ability) e.g. Darkrai, Gastly
        input_temp = input   
        
    else:
        abilities = re.findall(input, input)
        skip = True

    if (not skip):
        input_temp = input_temp + '^' # This is added so the re.findall knows where to stop
        #Underscore is used so that re.findall works properly
        input_temp = replace(input_temp, ' ', '_')

        #[A-Z][\w]*[\^] = Starts with uppercase, followed by any number of letters/digits/white-spaces and ends with '^' 
        abilities = re.findall('[A-Z][\w]*[\^]', input_temp)

        if (len(abilities) > 0):
            abilities[0] = abilities[0][:len(abilities[0])-1]
            abilities[0] = replace(abilities[0], '_', ' ')
        if (len(abilities) > 1):
            abilities[1] = abilities[1][:len(abilities[1])-1]
            abilities[1] = replace(abilities[1], '_', ' ')
        if (len(abilities) > 2):
            abilities[2] = abilities[2][:len(abilities[2])-1]
            abilities[2] = replace(abilities[2], '_', ' ')

        #adds '*' to last ability to indicate it is a hidden ability
        if '*' in input:
            abilities[len(abilities)-1] = abilities[len(abilities)-1] + '*'

    return list_to_string(abilities)

#####################################################################################################################
# Reformats local number
# input is not split, so input must be split with \n
    # Parameters
        # (String)  input   = 0000 (Aaaa)0001 (Bbbb)
    #Return
        # (List)    result  = [0000 (Aaaa), 0001 (Bbbb)]

def reformat_local_no(input):
    result = split_with(input, '[\)][0-9]', '\n')
    result = result.split("\n")
    return result

#####################################################################################################################
# Acts as a replace function
    # Parameters
        # (String)  simplify    = string to modify
        # (String)  search      = string to remove
        # (String)  replacement = string to add
    #Return
        # (String)  result      = string with replaced string

def replace(simplify, search, replacement):
    result = simplify
    while result.find(search) != -1:
        result = result[:result.find(search)] + replacement + result[result.find(search)+len(search):]
    return result

#####################################################################################################################
# Acts as a split function
    # Parameters
        # (String)  simplify    = string to modify
        # (String)  search      = string to break
        # (String)  split       = string to insert
    #Return
        # (String)  result      = string with replaced string

def split_with(simplify, search, split):
    result = simplify
    found = re.findall(search, result) # Finds all instances of 'find'
    for x in found:
        index = result.find(x)    # Locates first index of that instance
        result = result[:index+1] + split + result[index+1 :]  #inserts a 'split' inbetween the lowercase and uppercase
    return result

#####################################################################################################################
# Removes white space at beginning of String
    # Parameters
        # (String)  simplify    = string to modify
    #Return
        # (String)  result      = string with leading white spaces removes

def remove_beginning_white_space(simplify):
    current_index = 0
    result = ""
    while (simplify[current_index].isspace()):
        current_index += 1
    result = simplify[current_index:]
    return result

def list_to_string(list_to_convert):
    result = list_to_convert.pop(0)
    for x in list_to_convert:
        result += f', {list_to_convert.pop(0)}'

    return result