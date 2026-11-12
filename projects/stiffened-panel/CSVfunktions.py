import csv

"""data entry with LC"""
def data_entry(file_path, head_trigger, lc_trigger, trigger,list_to_insert):
    
    with open(file_path, 'r') as f:
        data = list(csv.reader(f, delimiter=';'))

    
    for r_idx in range(len(data)):
        
        if head_trigger in data[r_idx]:
            
            print("head trigger found")
            #print(r_idx)
            hc_idx = data[r_idx].index(head_trigger)
            #print(hc_idx)
            LC_idx = data[r_idx + 1].index(lc_trigger)

            #print(LC_idx)
            for collum_idx in range(LC_idx, len(data[r_idx + 1])):
                if data[r_idx + 2][collum_idx] == trigger:
                    print("trigger found")
                    for i in range(len(list_to_insert)):
                        # Accessing row (r_idx + 1 + i) in the SAME column (c_idx)
                        data[r_idx + 3 + i ][collum_idx] = list_to_insert[i]
                    break
                
        
    
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(data) 

"""data entry without LC"""
def data_entry_noLC(file_path, head_trigger, trigger,list_to_insert):
    
    with open(file_path, 'r') as f:
        data = list(csv.reader(f, delimiter=';'))

    
    for r_idx in range(len(data)):
        
        if head_trigger in data[r_idx]:
            
            print("head trigger found")
            #print(r_idx)
            hc_idx = data[r_idx].index(head_trigger)
            

            #print(LC_idx)
            for collum_idx in range(hc_idx, len(data[r_idx + 1])):
                if data[r_idx + 1][collum_idx] == trigger:
                    print("trigger found")
                    for i in range(len(list_to_insert)):
                        # Accessing row (r_idx + 1 + i) in the SAME column (c_idx)
                        data[r_idx + 2 + i ][collum_idx] = list_to_insert[i]
                    break
                
        
    
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(data) 

"""Extracting Altair result tables"""
def find_trigger(Table, Trigger):
    with open(Table, 'r') as f:
        i = 0
        for line in f:
            if Trigger in line:
                return i
            else:
                i = i+1

"""Extracts the value of a specific trigger from the general values table"""
def get_general_value(trigger, locationGeneral_values):
    with open(locationGeneral_values, 'r') as f:
        i = 0
        for line in f:
            if trigger in line:
                #print("line found")
                words = line.split(";")
                j = 0
                for j in range(0,len(words)):
                    if words[j] == trigger:
                     #print("word found")
                        return words[j+1]