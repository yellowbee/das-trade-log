#!/Users/ben/py-virtualenvs/trading/bin/python3

import sys
import pandas

# read the trade log file in csv format and reverse the row order
df = pandas.read_csv(sys.argv[1])
df = df.sort_index(axis=1, ascending=True)
df = df.iloc[::-1]

# *********** Init before loop ***********

# initization of variables for long trade statistics
# avgCostLong = {} # snapshot of the average cost for the tickers, for long position
# totalSharesLong = {} # snapshot of the total shares for the tickers 
# pnlLong = {} # snapshot of the pnlLong for the tickers
# tradepnlLong = {} # snapshot of the pnlLong for a trade, defined as the process from opening to closing of the position of a ticker
# verifypnlLong = {} # calculates the pnlLong in a different way to double check the validity of the results
# num_winners_long = 0
# num_losers_long = 0
# total_profit_long = 0
# total_loss_long = 0
# whole_shares_long = 0 
# winner_shares_long = 0
# loser_shares_long = 0
# breakeven_shares_long = 0

# initization of variables for short trade statistics
# avgDebtShort = {} # snapshot of the avg debt for the tickers, for short position
#totalSharesShort = {} # snapshot of the total shares for the tickers 
# pnlShort = {} # snapshot of the pnlLong for the tickers
# tradepnlShort = {} # snapshot of the pnlLong for a trade, defined as the process from opening to closing of the position of a ticker
# verifypnlShort = {} # calculates the pnlLong in a different way to double check the validity of the results
# num_winners_short = 0
# num_losers_short = 0
# total_profit_short = 0
# total_loss_short = 0
# whole_shares_short = 0 
# winner_shares_short = 0
# loser_shares_short = 0
# breakeven_shares_short = 0
# ************* End of init ******************

# last symbol streamed
last_sym = 'SYMBOL'

# variables shared by both long and short; "Pos" stands for "position" and for in-position tracking
avgInPosPrice = {}
sharesInPos = {}
pnlInPos = {}
pnlByTickers = {}

total_pnl_long = 0
total_pnl_short = 0
total_profit_long = 0
total_loss_long = 0
total_profit_short = 0
total_loss_short = 0

num_winners_long = 0
num_winners_short = 0
num_losers_long = 0
num_losers_short = 0

winner_shares_long = 0
winner_shares_short = 0
loser_shares_long = 0
loser_shares_short = 0

for index, row in df.iterrows():
	# ignore non-executed line 
	if row['Event'] != 'Execute':
		continue	

	sym = row['Symb']
	# first time for the ticker
	if sym not in pnlInPos:
		avgInPosPrice[sym] = 0
		sharesInPos[sym] = 0
		pnlInPos[sym] = 0
		pnlByTickers[sym] = 0

	# if execution is a BUY	
	if row['B/S'] == 'Buy':
		# if current symbol is different from the last streamed symbol, print a line
		if last_sym != sym:
			last_sym = sym
			print('')
		if sharesInPos[sym] == 0:
			print('------------ ' + sym + ' START Long ------------')

		#whole_shares_long += row['Shares']

		# for long position
		if sharesInPos[sym] >= 0: 
			avgInPosPrice[sym] = avgInPosPrice[sym] * sharesInPos[sym] + row['Shares']*row['Price']
			sharesInPos[sym] += row['Shares']
			avgInPosPrice[sym] = avgInPosPrice[sym] / sharesInPos[sym]

			pnlInPos[sym] -= row['Shares'] * row['Price']

			print(sym + ' buy long  ' + str(row['Shares']) + ' shares at ' + str(row['Price']) \
				+ ', shares remaining: ' + str(sharesInPos[sym]) \
				+ ', avgCost at: ' + str(round(avgInPosPrice[sym], 2)) \
				+ ', ' + row['Time'] \
				)

		# for short position
		else:
			sharesInPos[sym] += row['Shares']
			pnlInPos[sym] -= row['Shares'] * row['Price']

			print(sym + ' buy to cover ' + str(row['Shares']) + ' shares at ' + str(row['Price']) \
				+ ', shares remaining: ' + str(sharesInPos[sym]) \
				+ ', ' + row['Time'] \
				)

			# if it's a winner
			if row['Price'] <= abs(avgInPosPrice[sym]):
				num_winners_short += 1
				winner_shares_short += row['Shares']
				total_profit_short += (abs(avgInPosPrice[sym]) - row['Price']) * row['Shares']

			# if it's a loser
			else:
				num_losers_short += 1
				loser_shares_short += row['Shares']
				total_loss_short += (abs(avgInPosPrice[sym]) - row['Price']) * row['Shares']

			if sharesInPos == 0:
				pnlByTickers[sym] += pnlInPos
				total_pnl_short += pnlInPos
				avgInPosPrice[sym] = 0
				pnlInPos = 0

				print('------------ ' + sym + ' END Short ------------\n')


	elif (row['B/S'] == 'Sell' or row['B/S'] == 'Shrt'):
		# if current symbol is different from the last streamed symbol, print a line
		if last_sym != sym:
			last_sym = sym
			print('')
		if sharesInPos[sym] == 0:
			print('------------ ' + sym + ' START Short ------------')

		# for long position
		if sharesInPos[sym] > 0:
			sharesInPos[sym] -= row['Shares']
			pnlInPos[sym] += row['Shares'] * row['Price']

			print(sym + ' sell ' + str(row['Shares']) + ' shares at ' + str(row['Price']) \
				+ ', shares remaining: ' + str(sharesInPos[sym]) \
				+ ', avgCost at: ' + str(round(avgInPosPrice[sym], 2)) \
				+ ', ' + row['Time'] \
				)

			# if it's a winner
			if row['Price'] >= avgInPosPrice[sym]:
				num_winners_long += 1
				winner_shares_long += row['Shares']
				total_profit_long += (row['Price'] - avgInPosPrice[sym]) * row['Shares']

			# if it's a loser
			else:
				num_losers_long += 1
				loser_shares_long += row['Shares']
				total_loss_long += (row['Price'] - avgInPosPrice[sym]) * row['Shares']

			# if position is closed
			if sharesInPos[sym] == 0:
				pnlByTickers[sym] += pnlInPos[sym]
				total_pnl_long += pnlInPos[sym]
				avgInPosPrice[sym] = 0
				pnlInPos[sym] = 0

				print('------------ ' + sym + ' END Long ------------\n')

		# for short position
		else:
			avgInPosPrice[sym] = avgInPosPrice[sym] * sharesInPos[sym] + row['Shares']*row['Price']
			sharesInPos[sym] -= row['Shares']
			avgInPosPrice[sym] = avgInPosPrice[sym] / sharesInPos[sym]

			pnlInPos[sym] += row['Shares'] * row['Price']

			print(sym + ' short  ' + str(row['Shares']) + ' shares at ' + str(row['Price']) \
				+ ', shares remaining: ' + str(sharesInPos[sym]) \
				+ ', avgCost at: ' + str(round(avgInPosPrice[sym], 2)) \
				+ ', ' + row['Time'] \
				)


		'''
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
		'''

print('\n')
print('******** Trade Report ********')
dailypnl = 0
for key in pnlByTickers:
	print('pnl: ' + key + ' $' + str( round(pnlByTickers[key], 2) ) )
	dailypnl += pnlByTickers[key]

print('daily pnl: ' + str(round(dailypnl, 2)))
print('------------------')

print('#winners long: ' + str(num_winners_long))
print('#losers long: ' + str(num_losers_long))
print('#winners short: ' + str(num_winners_short))
print('#losers short: ' + str(num_losers_short))
#if num_winners_long > 0:
#	print('avg winner: ' + str(round(total_profit_long/num_winners_long, 2)))
#if num_losers_long > 0:
#	print('avg loser: ' + str(round(total_loss_long/num_losers_long, 2)))

print('------------------')

print('total profit long: ' + str(round(total_profit_long, 2)))
print('total loss long: ' + str(round(total_loss_long, 2)))
print('total profit short: ' + str(round(total_profit_short, 2)))
print('total loss short: ' + str(round(total_loss_short, 2)))
print('total pnl: ' + str(round(total_profit_long + total_profit_short + total_loss_long + total_loss_short, 2)))
print('------------------')

#print('#total shares: ' + str(whole_shares_long))
print('#winner shares long: ' + str(winner_shares_long))
print('#loser shares long: ' + str(loser_shares_long))
print('#winner shares short: ' + str(winner_shares_short))
print('#loser shares short: ' + str(loser_shares_short))
print('#total shares: ' + str(winner_shares_long+winner_shares_short+loser_shares_long+loser_shares_short))
#print('#break even shares: ' + str(breakeven_shares_long))
#if winner_shares_long > 0:
#	print('avg profit/share: ' + str(round(total_profit_long/winner_shares_long, 2)))
#if loser_shares_long > 0:
#	print('avg loss/share: ' + str(round(total_loss_long/loser_shares_long, 2)))
print('\n')

