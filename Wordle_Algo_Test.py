import pandas as pd
import time as t
from tqdm import tqdm
import random

word_list_file = 'Wordle List.txt'
lookup_file = 'wordle_lookup.csv'

def load_word_list():
    global word_list
    word_list = pd.read_csv(word_list_file, header = None)
    print(word_list)

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

def guess():
    group_lookup()
    return groupdf.index[0]

def solver(target):
    load_working_lookup()
    for n in range(16):
        print('Guess ', n+1)
        input = guess()
        print(input)
        rspn = df.loc[(df['input'] == input) & (df['target'] == target),'rspn'].to_string(index=False)
        print(rspn)
        if rspn == 'ggggg':
            return n+1
            break
        cand_target(input,rspn)
        filter_target()
        filter_input()

#Main Entrance

load_word_list()
load_lookup()
load_working_lookup()
#row = random.randrange(1,2314)
#row = int(input('Row: '))
#target = word_list.iloc[row,0]
#print(target)
#solver(target)
#print(word_list.columns)
#print(df.columns)

output = word_list
tqdm.pandas(desc="Solver running")
output['GuessCount'] = output.progress_apply(lambda x: solver(x[0]), axis=1)
output.to_csv('Wordle-Algo-Test-Result.csv')
print(output)
