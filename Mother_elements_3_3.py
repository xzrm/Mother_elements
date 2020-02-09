import os
import re
import itertools
import pprint


PROJECT_PATH = r'E:\user\kraczlam5898\Rozenoordbrug\Model\Models for NLA\Fase 4'

def pure_windows_path(path):
    return path.replace('\\', '\\\\')

PROJECT_PATH = pure_windows_path(PROJECT_PATH)

os.chdir(PROJECT_PATH)
print(os.getcwd())



def find_data_files():
    files_list = [file for file in os.listdir() if file.endswith('.dat')]
    
    print ("\n --- Available .dat files in {} \n".format(os.getcwd()))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(files_list)
    return files_list
    
    
def input_file():
    files_list = find_data_files()
    while True:
        user_input = input('\n --- Give the .dat file or type Quit: \n \n >>>')
        
        if not user_input.endswith('.dat') and user_input != 'Quit':
            user_input += ".dat"

        if user_input in files_list:
            input_data = open(user_input)
            return user_input, input_data
        elif user_input == 'Quit':
            exit()
        print ('\nFile not found')



file_name, input_data = input_file()


lines = input_data.readlines() 
lines = iter(lines)

    
def find_elem_groups():
    elem_sets = dict()
    temp_str = ""
    for line in lines:
        out_f.write(line)
        if 'REINFO' in line:
            elem_sets = find_group_members(temp_str)
            return line, elem_sets
        else:
            temp_str += " " + line.strip(" ").strip('\n')
    
    return line, elem_sets

def find_reinfo_groups():
    reinfo_sets = dict()
    
    temp_str = ""
    
    for line in lines:
        out_f.write(line)
        if "'REINFORCEMENTS'" in line:
            reinfo_sets = find_group_members(temp_str)
            return line, reinfo_sets
        else:
            temp_str += " " + line.strip(" ").strip('\n')
    
    return line, reinfo_sets

    
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return list(itertools.zip_longest(*args, fillvalue=fillvalue))
    
def find_group_members(string):
    groups = {}
    split_str = string.split(r" / ")
    grouped_list = grouper(split_str, 2)
    for set_name_str, members in grouped_list:
        set_number, set_name = set_name_str.strip().split(" ", 1)
        set_name = set_name.strip('"')
        _members = re.findall(r'\"(.+?)\"',members)
        groups[set_name] = _members
    return groups
        
    
def find_groups():
    for line in lines:
        out_f.write(line)
        if 'ELEMEN' in line:
            line, elem_sets = find_elem_groups()
        if 'REINFO' in line:
            line, reinfo_sets = find_reinfo_groups()
        if "'REINFORCEMENTS'" in line:
            check_num_groups(elem_sets)
            break
    return line, elem_sets, reinfo_sets
            

def check_num_groups(list):
    if not list:
        raise ValueError('Element sets not found!')
    # print (list)
    

    
def assign_mother_elem(elem_set):
    for line in lines:
        if "DATA" in line:
            out_f.write(line)
            break
        if 'LINE' in line:
            out_f.write(line)
            out_f.write('     ELEMEN   "{}" / \n'.format(elem_set))
        elif 'PLANE' in line:
            out_f.write(line)
            out_f.write('     ELEMEN   "{}" / \n'.format(elem_set))
        else:
            out_f.write(line)
            
def copy_lines():
    for line in lines:
        if "DATA" in line:
            out_f.write(line)
            break
        else:
            out_f.write(line)
        

def assign_elemen(groups):
    # assert reinfo_set in reinfo_sets.keys(), "GIVEN SET NOT IN REINFORCEMENT SETS!" <---- gotta be implemented
    for line in lines:
        if 'LOADS' not in line:
            out_f.write(line)
            for elem_set, reinfo_set in groups:
                if any(i in line for i in reinfo_sets[reinfo_set]):
                    # print (line.strip("\n"))
                    assign_mother_elem(elem_set)
        else:
            out_f.write(line)
            break

def check_input_groups():
    group_list = []
    while True:
        user_input = input("\n --- Input a pair of corresponding ELEMEN and REINFO GROUP as: ELEMEN_GROUP1, REINFO_GROUP1 or Run or Quit \n \n >>>")
        if not user_input:
            print ("\n --- Groups not selected")
        elif user_input == 'Quit':
            exit()
        elif user_input == 'Run':
            
            break
        else:
            try:
                element_group, reinfo_group = [i.strip() for i in user_input.split(",")]
            except ValueError:
                print ("\n --- WRONG INPUT \n")
            else:
                if element_group in elem_sets.keys() and reinfo_group in  reinfo_sets.keys():
                    group_list.append((element_group, reinfo_group)) #work this out
                    group_list = list(set(group_list))
                    print ("\n --- You selected: \n {}".format(group_list))
                else:
                    print ("\n --- Group(s) not found or unknown command \n")
    return group_list
                
                
with open('Analysis_' + file_name, 'w') as out_f:
    for line in lines:
        out_f.write(line)
        if 'GROUPS' in line:
            line, elem_sets, reinfo_sets = find_groups()
            print ("\n --- Available ELEMEN GROUPS: {}".format(elem_sets.keys()))
            print ("\n --- Available REINFO GROUPS: {}".format(reinfo_sets.keys()))
        if 'REINFORCEMENTS' in line:
            groups = check_input_groups()
            # print (groups)
            assign_elemen((groups))
            
    print ("\n --- JOB COMPLETED \n")

            
            

                
            

        
        
        
    
    

    

#condition that if reinfo_sets is empty then user has to specify list of reinfo for the assignment
#
#logging which reinfo -> which mother elements 


#try generator with yield statement for processing all lines

#exclusivness of sets with reinforcement.

#removing file if it already exists with a confirmation

#removing from a list



