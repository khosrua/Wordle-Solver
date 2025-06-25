import pandas as pd
import time as t
from tqdm import tqdm

word_list_file = 'Wordle List.txt'
lookup_file = 'wordle_lookup.csv'

def rspn_calc(wInput,wTarget):
    input = list(wInput)
    target = list(wTarget)
    rspn = list("bbbbb")
#Assign Green output for matching letters
    for i in range(5):
        if input[i] == target[i]:
            rspn[i] = "g"

    for i in range(4,-1,-1):
        if rspn[i] == "g":
            del target[i]
#Assign Yellow for correct letters in wrong places
    for i in range(5):
        if rspn[i] == "b":
            for j in target:
                if input[i] == j:
                    rspn[i] = "y"
                    target.remove(j)
    return ''.join(rspn)

def write_lookup():
    global df
    print('Read word list...')
    df = pd.read_csv(word_list_file, header = None)
    print('Done')
    
    print('Cross Join word list...')
    df = df.merge(df, how='cross')
    df = df.rename(columns={'0_x':'input','0_y':"target"})
    print('Done')

    tqdm.pandas(desc="Calculate word guess responses")
    df['rspn'] = df.progress_apply(lambda x: rspn_calc(x['input'], x['target']), axis=1)
    print(df)

    df.to_csv(lookup_file,index=False)

    print('Lookup Table constructed')

def load_lookup():
    global df
    print('Read word list...')
    df = pd.read_csv(lookup_file)
    print('Done')
    print(df)

def load_working_lookup():
    global wrkdf
    wrkdf = df

def group_lookup():
    global groupdf
    groupdf = wrkdf.groupby(['input','rspn']).count().groupby(['input']).count().sort_values('target',ascending=False)

def cand_target(input,rspn):
    global target_list
    target_list = wrkdf.loc[(wrkdf['input'] == input) & (wrkdf['rspn'] == rspn),'target']

def filter_target():
    global wrkdf
    wrkdf = wrkdf[(wrkdf['target'].isin(target_list))]

def filter_input():
    global wrkdf
    wrkdf = wrkdf[(wrkdf['input'].isin(target_list))]

#Main
print('Wordle Solver')
print('1. Recalculate the lookup table. Use if the word list has been updated')
print('2. Load lookup table from file')

while True:
    optn = input('Select: ')
    if optn == '1':
        write_lookup()
        break
    elif optn == '2':
        load_lookup()
        break
    else:
        print('Invalid input')
while True:
    load_working_lookup()
    for i in range(6):
        group_lookup()
        print(groupdf.head())
        
        inputG = input('Word guessed: ')
        rspnG = input('Game response: ')
        if rspnG == 'ggggg' or inputG == '0':
            print('Congratulation')
            break
        cand_target(inputG,rspnG)
        filter_target()
        #filter_input()
        print(target_list)
    cont = input('Play again? y/n: ')
    if cont == 'n':
        break
