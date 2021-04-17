#!/Users/ben/py-virtualenvs/trading/bin/python3

import sys
import pandas

# read the trade log file in csv format and reverse the row order
df = pandas.read_csv(sys.argv[1])
df = df.sort_index(axis=1, ascending=True)
df = df.iloc[::-1]

# init for long position variables
avgCostLong = {} # snapshot of the average cost for the tickers, for long position
totalSharesLong = {} # snapshot of the total shares for the tickers 
pnlLong = {} # snapshot of the pnlLong for the tickers
tradepnlLong = {} # snapshot of the pnlLong for a trade, defined as the process from opening to closing of the position of a ticker
verifypnlLong = {} # calculates the pnlLong in a different way to double check the validity of the results
num_winners_long = 0
num_losers_long = 0
total_profit_long = 0
total_loss_long = 0
whole_shares_long = 0 
winner_shares_long = 0
loser_shares_long = 0
breakeven_shares_long = 0

# last symbol streamed
last_sym = 'SYMBOL'

# init for short position variables
'''
avgDebtShort = {} # snapshot of the avg debt for the tickers, for short position
totalSharesShort = {} # snapshot of the total shares for the tickers 
pnlShort = {} # snapshot of the pnlLong for the tickers
tradepnlShort = {} # snapshot of the pnlLong for a trade, defined as the process from opening to closing of the position of a ticker
verifypnlShort = {} # calculates the pnlLong in a different way to double check the validity of the results
num_winners_short = 0
num_losers_short = 0
total_profit_short = 0
total_loss_short = 0
whole_shares_short = 0 
winner_shares_short = 0
loser_shares_short = 0
breakeven_shares_short = 0
'''

for index, row in df.iterrows():
	# ignore short for now
	if row['B/S'] == 'Shrt' or row['B/S'] == 'Cover':
		continue	

	sym = row['Symb']
	if sym not in pnlLong and row['Event'] == 'Execute':
		avgCostLong[sym] = 0
		totalSharesLong[sym] = 0
		pnlLong[sym] = 0
		tradepnlLong[sym] = 0
		verifypnlLong[sym] = 0
	
	# if execution is a BUY	
	if row['B/S'] == 'Buy' and row['Event'] == 'Execute':
		# if current symbol is different from the last streamed symbol, print a line
		if last_sym != sym:
			last_sym = sym
			print('')
		if totalSharesLong[sym] == 0:
			print('------------ ' + sym + ' START ------------')

		whole_shares_long += row['Shares']

		# for long position
		if totalSharesLong[sym] >= 0: 
			avgCostLong[sym] = avgCostLong[sym] * totalSharesLong[sym] + row['Shares']*row['Price']
			totalSharesLong[sym] += row['Shares']
			avgCostLong[sym] = avgCostLong[sym] / totalSharesLong[sym]
			pnlLong[sym] -= row['Shares'] * row['Price']
			tradepnlLong[sym] -= row['Shares'] * row['Price']
			print(sym + ' buy ' + str(row['Shares']) + ' shares at ' + str(row['Price']) \
				+ ', shares remaining: ' + str(totalSharesLong[sym]) \
				+ ', avgCostLong at: ' + str(round(avgCostLong[sym], 2)) \
				+ ', ' + row['Time'] \
				)
		# for short position
		'''
		else:
			# if it's a winner
			if row['Price'] < avgDebtShort[sym]:
				num_winners_short += 1
				total_profit_short += row['Shares']*(avgDebtShort[sym] - row['Price'])
				winner_shares_short += row['Shares']
			# if it's a loser
			elif row['Price'] > avgCostLong[sym]:
				num_losers_short += 1
				total_loss_short += row['Shares']*(row['Price'] - avgCostLong[sym])
				loser_shares_short += row['Shares']
			else:
				breakeven_shares_short += row['Shares']

			totalSharesShort[sym] -= row['Shares']
			pnlShort[sym] -= row['Shares'] * row['Price']
			tradepnlShort[sym] -= row['Shares'] * row['Price']
			print(sym + ' cover ' + str(row['Shares']) + ' shares at ' + str(row['Price']) \
				+ ', shares remaining: ' + str(round(totalSharesLong[sym], 2)) \
				+ ', ' + row['Time'] \
				)

			if totalSharesShort[sym] == 0:
				print('pnlShort: ' + str(round(tradepnlLong[sym], 2)))
				verifypnlShort[sym] -= tradepnlShort[sym]
				tradepnlShort[sym] = 0
				print('\n')
		'''



	elif (row['B/S'] == 'Sell' or row['B/S'] == 'Shrt') and row['Event'] == 'Execute':
		# if current symbol is different from the last streamed symbol, print a line
		if last_sym != sym:
			last_sym = sym
			print('')

		# if it's a winner
		if row['Price'] > avgCostLong[sym]:
			num_winners_long += 1
			total_profit_long += row['Shares']*(row['Price'] - avgCostLong[sym])
			winner_shares_long += row['Shares']
		# if it's a loser
		elif row['Price'] < avgCostLong[sym]:
			num_losers_long += 1
			total_loss_long += row['Shares']*(row['Price'] - avgCostLong[sym])
			loser_shares_long += row['Shares']
		else:
			breakeven_shares_long += row['Shares']

		totalSharesLong[sym] -= row['Shares']
		pnlLong[sym] += row['Shares'] * row['Price']
		tradepnlLong[sym] += row['Shares'] * row['Price']
		print(sym + ' sell ' + str(row['Shares']) + ' shares at ' + str(row['Price']) \
			+ ', shares remaining: ' + str(round(totalSharesLong[sym], 2)) \
			+ ', ' + row['Time'] \
			)

		if totalSharesLong[sym] == 0:
			print('pnlLong: ' + str(round(tradepnlLong[sym], 2)))
			verifypnlLong[sym] += tradepnlLong[sym]
			tradepnlLong[sym] = 0
			print('------------ ' + sym + ' END ------------\n')

print('\n')
print('******** Trade Report ********')
dailypnlLong = 0
for key in pnlLong:
	print('pnlLong: ' + key + ' $' + str( round(pnlLong[key], 2) ) )
	dailypnlLong += pnlLong[key]
for key in verifypnlLong:
	print('Verified pnlLong: ' + key + ' $' + str( round(pnlLong[key], 2) ) )

print('------------------')

print('#winners: ' + str(num_winners_long))
print('#losers: ' + str(num_losers_long))
if num_winners_long > 0:
	print('avg winner: ' + str(round(total_profit_long/num_winners_long, 2)))
if num_losers_long > 0:
	print('avg loser: ' + str(round(total_loss_long/num_losers_long, 2)))

print('------------------')

print('daily pnlLong: ' + str(round(dailypnlLong, 2)))
print('total profit: ' + str(round(total_profit_long, 2)))
print('total loss: ' + str(round(total_loss_long, 2)))

print('------------------')

print('#total shares: ' + str(whole_shares_long))
print('#winner shares: ' + str(winner_shares_long))
print('#loser shares: ' + str(loser_shares_long))
print('#break even shares: ' + str(breakeven_shares_long))
if winner_shares_long > 0:
	print('avg profit/share: ' + str(round(total_profit_long/winner_shares_long, 2)))
if loser_shares_long > 0:
	print('avg loss/share: ' + str(round(total_loss_long/loser_shares_long, 2)))
print('\n')

