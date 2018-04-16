#Re-organize call history file so that each record has one row, with info from
#attempts appended to end of row, in order of attempts, and no fields with
#unchanging values (e.g. project name, case ID) not duplicated.

#Attempts information appended at end of file.

#Precondition: First row contains header, file contains unique ID and attempts variable

import tkinter
import collections

def read_file():
    orig_file = tkinter.filedialog.askopenfilename()
    open_file = open(orig_file)
    return open_file.read()

#Read data file to list of rows.

def parse_csv(csv):
    list_of_rows = csv.split('\n')

    list_of_list = []
    for i in range(len(list_of_rows)):
        list_of_list.append(list_of_rows[i].split(','))

    if len(list_of_list[-1]) == 1:
        list_of_list.pop(-1)

    return list_of_list

#Identify unique case ID variable.

def get_user_input():
    id_var = int(input("Please enter the column number of the unique case ID variable (e.g. resRespondent):\n"))-1

#Identify attempts variable.
    attempts_var = int(input("Please enter the column number of the attempts variable (e.g. resCallCount):\n"))-1

#Identify remaining variables containing call history information.
    call_history_var_str = input("Please enter the column number of the remaining variables containing the call history information.\nThese would include interviewer number, last call date, last call start time, call outcome, etc.\nPlease separate numbers with commas:\n")
    call_history_var_list = call_history_var_str.split(',')
    return {"id": id_var, "attempts": attempts_var, "call_history": call_history_var_list}

def consolidate_rows(csv, user_input):
    for i in range(len(user_input["call_history"])):
        user_input["call_history"][i] = int(user_input["call_history"][i]) - 1

    all_call_history_var_list = []
    all_call_history_var_list.append(user_input["attempts"])

    for i in range(len(user_input["call_history"])):
        all_call_history_var_list.append(user_input["call_history"][i])

    all_call_history_var_list.sort()

    #Temporarily remove header row.
    header = csv.pop(0)


    #Sort by attempts.
    csv.sort(key=lambda x: int(x[user_input["attempts"]]))


    #Insert header back.
    csv.insert(0, header)

    #Append additional headers for max # of attempts.
    attempts = []


    for i in range(1, (len(csv))):
        attempts.append(int(csv[i][user_input["attempts"]]))


    max_attempts = int(max(attempts))

    for r in range(2, (max_attempts + 1)):
        for i in all_call_history_var_list:
            csv[0].append(csv[0][i] + str(r))

#Find locations of rows containing first attempt.

    first_attempt_rows = []
    list_of_ids = []
    for i in range(len(csv)):
        if csv[i][user_input["attempts"]] == '1':
            first_attempt_rows.append(i)
            list_of_ids.append(csv[i][user_input["id"]])

#Create a dictionary of unique case IDs and the rows associated with them that contain information for attempts 2+.

    ids_and_rows = collections.defaultdict(list)

    for row in range(1,len(csv)):
        if not row in first_attempt_rows:
            ids_and_rows[csv[row][user_input["id"]]].append(row)

#Add information from rows containing information for attempts 2+ to row containing information for attempt 1.

    temp_list = []
    for i in first_attempt_rows:
        temp_list = ids_and_rows[csv[i][user_input["id"]]]
        for i2 in temp_list:
            for i3 in all_call_history_var_list:
                csv[i].append(csv[i2][i3])
                                 
#Delete extra rows.

    for i in range(1, len(csv)):
        if int(csv[-1][user_input["attempts"]]) != 1:
                   csv.pop(-1)

    return csv

#Convert back to comma de-limited string.

def data_to_csv(data):
    output = ''

    for i in range(len(data)):
        for i2 in range(len(data[i])):
            output = output + data[i][i2] + ','
        output = output + '\n'

    return output

def write_to_file(csv):
    output_file = tkinter.filedialog.asksaveasfilename()
    to_file = open(output_file, 'w')

    to_file.write(csv)
    to_file.close()

csv = read_file()
data = parse_csv(csv)
user_input = get_user_input()
output_data = consolidate_rows(data, user_input)
output_csv = data_to_csv(output_data)
write_to_file(output_csv)
