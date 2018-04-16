#Re-organize call history file so that each record has one row, with info from
#attempts appended to end of row, in order of attempts, and no fields with
#unchanging values (e.g. project name, case ID) not duplicated.

#Attempts information appended at end of file.

#Precondition: First row contains header, file contains unique ID and attempts variable

import tkinter
import collections
orig_file = tkinter.filedialog.askopenfilename()
open_file = open(orig_file)
data = open_file.read()

#Read data file to list of rows.

list_of_rows = data.split('\n')

list_of_list = []
for i in range(len(list_of_rows)):
    list_of_list.append(list_of_rows[i].split(','))

if len(list_of_list[-1]) == 1:
    list_of_list.pop(-1)

#Identify unique case ID variable.

id_var = int(input("Please enter the column number of the unique case ID variable (e.g. resRespondent):\n"))-1

#Identify attempts variable.
attempts_var = int(input("Please enter the column number of the attempts variable (e.g. resCallCount):\n"))-1

#Identify remaining variables containing call history information.
call_history_var_str = input("Please enter the column number of the remaining variables containing the call history information.\nThese would include interviewer number, last call date, last call start time, call outcome, etc.\nPlease separate numbers with commas:\n")
call_history_var_list = call_history_var_str.split(',')

for i in range(len(call_history_var_list)):
    call_history_var_list[i] = int(call_history_var_list[i]) - 1

all_call_history_var_list = []
all_call_history_var_list.append(attempts_var)

for i in range(len(call_history_var_list)):
    all_call_history_var_list.append(call_history_var_list[i])

all_call_history_var_list.sort()

#Temporarily remove header row.
header = list_of_list.pop(0)

#Sort by attempts.
list_of_list.sort(key=lambda x: int(x[attempts_var]))

#Insert header back.
list_of_list.insert(0, header)

#Append additional headers for max # of attempts.
attempts = []

for i in range(1, (len(list_of_list))):
    attempts.append(int(list_of_list[i][attempts_var]))

max_attempts = int(max(attempts))

for r in range(2, (max_attempts + 1)):
    for i in all_call_history_var_list:
        list_of_list[0].append(list_of_list[0][i] + str(r))

#Find locations of rows containing first attempt.

first_attempt_rows = []
list_of_ids = []
for i in range(len(list_of_list)):
    if list_of_list[i][attempts_var] == '1':
        first_attempt_rows.append(i)
        list_of_ids.append(list_of_list[i][id_var])

#Create a dictionary of unique case IDs and the rows associated with them that contain information for attempts 2+.

ids_and_rows = collections.defaultdict(list)

for row in range(1,len(list_of_list)):
    if not row in first_attempt_rows:
        ids_and_rows[list_of_list[row][id_var]].append(row)

#Add information from rows containing information for attempts 2+ to row containing information for attempt 1.

temp_list = []
for i in first_attempt_rows:
    temp_list = ids_and_rows[list_of_list[i][id_var]]
    for i2 in temp_list:
        for i3 in all_call_history_var_list:
            list_of_list[i].append(list_of_list[i2][i3])
                             
#Delete extra rows.

for i in range(1, len(list_of_list)):
    if int(list_of_list[-1][attempts_var]) != 1:
               list_of_list.pop(-1)

#Convert back to comma de-limited string.

output_file = tkinter.filedialog.asksaveasfilename()
to_file = open(output_file, 'w')
output = ''

for i in range(len(list_of_list)):
    for i2 in range(len(list_of_list[i])):
        output = output + list_of_list[i][i2] + ','
    output = output + '\n'

to_file.write(output)
to_file.close()
