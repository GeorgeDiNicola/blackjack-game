from os import system, name 

def display_list(list_items):
	for item in list_items:
		print(item)

def append_lists_item_wise(first_list, second_list):
	first_list = add_tab_after_list_items(first_list)
	appended_list = [i + j for i, j in zip(first_list, second_list)]
	return appended_list

def add_tab_after_list_items(input_list):
	output_list = [''] * len(input_list)
	for i in range(0, len(input_list)):
		output_list[i] = input_list[i] + '\t'
	return output_list

def get_valid_input(prompt, possible_input, error_message):
	valid = False
	while not valid:
		choice = input(prompt)
		if choice.lower() in possible_input:
			valid = True
		else:
			print(error_message)
	return choice.lower()

def clear_window(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux
    else: 
        _ = system('clear')