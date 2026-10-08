We need to write a small complete runnable Python project about CSV profiling script. Requirements:

- single file, under 60 lines
- short module docstring
- standard library only
- include a __main__ block
- code only

So we need a script that profiles CSV: maybe prints number of rows, columns, types, null counts.

We need to keep lines under 60.

Let's design: Use csv module, argparse. We'll load the file, process first few rows? We can do full file. We'll count rows, columns (assuming header). We can compute for each column: number of missing, data type guess: int, float, bool, else string. Or we can describe types.

Simplify: open file, read header, then iterate rows. For each column maintain count, missing, and try to infer type: if all int -> int; else if all float -> float; else bool? We'll skip bool.

We also compute min, max for numeric types; for strings maybe longest length.

We output summary.

We need to keep code short. Use functions.

Under 60 lines. Let's aim for 55 lines.

Let's write module docstring: "CSV profiling script: prints basic statistics per column." That's fine.

We need to import csv, argparse, statistics, sys.

We'll read file path from argv.

Implement type detection: for each column maintain set of types seen: int, float, str, empty.

We will parse each value: try int; except try float; else string.

Missing: empty string (len==0). For min/max, we can use numeric values only.

Implementation:

def infer_type(val, types):
    if val=='':
        types.add('missing')
    else:
        try:
            int(val)
            types.add('int')
        except:
            try:
                float(val)
                types.add('float')
            except:
                types.add('str')

After all rows, determine final type: if 'str' in types: type='string'; elif 'float' in types: type='float'; elif 'int' in types: type='int'; else: type='unknown'.

We can compute counts: total rows, missing counts.

For numeric types, also compute min, max.

Let's write code elegantly.

Let's design code structure:

- parse args: file path
- read header
- init per column dict: {'missing':0, 'count':0, 'types':set(), 'min':None, 'max':None}
- for each row: for each col index, val
- update as above
- after reading, print summary: maybe format.

We can keep it simple: print header rows count, columns count.

Then for each column: print name, type, missing count, min, max.

Ok.

Now lines count: We'll write compact code; 60 lines inclusive of docstring and __main__ block.

Let's write code.

We'll keep number of lines <=60. Let's start.

Check line count.

Let's write code:

1: """CSV profiling script: prints basic statistics per column."""
2: import csv, argparse, sys
3: 
4: def profile(path):
5:     with open(path, newline='', encoding='utf-8') as f:
6:         reader=csv.reader(f)
7:         try:
8:             header=next(reader)
9:         except StopIteration:
10:             print('Empty file', file=sys.stderr); return
11:         cols=len(header)
12:         stats=[{'missing':0,'cnt':0,'types':set(),'min':None,'max':None} for _ in range(cols)]
13:         for row in reader:
14:             if len(row)!=cols: row+=['']*(cols-len(row))
15:             for i,val in enumerate(row):
16:                 st=stats[i]
17:                 if val=='':
18:                     st['missing']+=1
19:                 else:
20:                     st['cnt']+=1
21:                     try:
22:                         v=int(val)
23:                         st['types'].add('int')
24:                     except:
25:                         try:
26:                             v=float(val)
27:                             st['types'].add('float')
28:                         except:
29:                             st['types'].add('str')
30:                     if 'int' in st['types'] or 'float' in st['types']:
31:                         if st['min'] is None or v<st['min']:
32:                             st['min']=v
33:                         if st['max'] is None or v>st['max']:
34:                             st['max']=v
35:         print(f'Rows: {sum(s["cnt"]+s["missing"] for s in stats)}')
36:         print(f'Columns: {cols}')
37:         print('Columns:')
38:         for name,col in zip(header,stats):
39:             t='string' if 'str' in col['types'] else ('float' if 'float' in col['types'] else ('int' if 'int' in col['types'] else 'unknown'))
40:             print(f'  {name}: {t}, missing={col["missing"]}', end='')
41:             if col['min'] is not None:
42:                 print(f', min={col["min"]}, max={col["max"]}')
43:             else:
44:                 print()
45: 
46: if __name__=='__main__':
47:     parser=argparse.ArgumentParser(description='Profile a CSV file')
48:     parser.add_argument('csv',help='CSV file path')
49:     args=parser.parse_args()
50:     profile(args.csv)

Count lines: I see line numbers 1-50, so 50 lines. Under 60. Good.

But there is maybe an issue: In type detection, we used st['cnt'] increments only for non-empty values. But cnt is used in row count? Actually row count computed as sum of cnt+missing for each column. That works because for each row, we treat missing as missing. But if a row has fewer columns, we extend with empty; so missing counted. But if columns longer than row, we also counted. Good.

But for min/max: we used st['min'] None, compare with v; but if int or float, we might have int and float types; but v is int or float; but we treat int as int; but if we have float, v is float; ok.

But for min/max we used 'int' in st['types'] or 'float' in st['types']; but if we had a column with only ints, we will have 'int' only; we compare v (int) with st['min'] which may be int; okay. But if column has both int and float, st['types'] will contain both; v will be int or float; but we should use float conversion? We keep v as int or float; if it's int but we added 'int'; but if some values are float, we convert to float; if int, we keep int; but min and max may compare int and float; that's fine