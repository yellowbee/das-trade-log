#!/Users/ben/py-virtualenvs/trading/bin/python3

import sys
import pandas
import util
from util import *

# read the trade log file in csv format and reverse the row order
df = pandas.read_csv(sys.argv[1])
df = df.sort_index(axis=1, ascending=True)
df = df.iloc[::-1]

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

start_time = {}
end_time = {}
num_positions_long = 0
num_positions_short = 0
total_hold_time_long = 0
total_hold_time_short = 0

#######################
timeslot_pnl = {}

timeslot_pnl[util.PREMARKET] = {}
timeslot_pnl[util.SESSION_ONE_AM] = {}
timeslot_pnl[util.SESSION_TWO_AM] = {}
timeslot_pnl[util.SESSION_THREE_AM] = {}
timeslot_pnl[util.SESSION_FOUR_AM] = {}
timeslot_pnl[util.SESSION_FIVE_AM] = {}
timeslot_pnl[util.SESSION_SIX_AM] = {}
timeslot_pnl[util.MIDDAY] = {}
timeslot_pnl[util.PM] = {}
timeslot_pnl[util.POWER_HOUR] = {}
timeslot_pnl[util.AFTER_HOUR] = {}

timeslot_pnl[util.PREMARKET]['profit'] = {}
timeslot_pnl[util.PREMARKET]['loss'] = {}
timeslot_pnl[util.SESSION_ONE_AM]['profit'] = {}
timeslot_pnl[util.SESSION_ONE_AM]['loss'] = {}
timeslot_pnl[util.SESSION_TWO_AM]['profit'] = {}
timeslot_pnl[util.SESSION_TWO_AM]['loss'] = {}
timeslot_pnl[util.SESSION_THREE_AM]['profit'] = {}
timeslot_pnl[util.SESSION_THREE_AM]['loss'] = {}
timeslot_pnl[util.SESSION_FOUR_AM]['profit'] = {}
timeslot_pnl[util.SESSION_FOUR_AM]['loss'] = {}
timeslot_pnl[util.SESSION_FIVE_AM]['profit'] = {}
timeslot_pnl[util.SESSION_FIVE_AM]['loss'] = {}
timeslot_pnl[util.SESSION_SIX_AM]['profit'] = {}
timeslot_pnl[util.SESSION_SIX_AM]['loss'] = {}
timeslot_pnl[util.MIDDAY]['profit'] = {}
timeslot_pnl[util.MIDDAY]['loss'] = {}
timeslot_pnl[util.PM]['profit'] = {}
timeslot_pnl[util.PM]['loss'] = {}
timeslot_pnl[util.POWER_HOUR]['profit'] = {}
timeslot_pnl[util.POWER_HOUR]['loss'] = {}
timeslot_pnl[util.AFTER_HOUR]['profit'] = {}
timeslot_pnl[util.AFTER_HOUR]['loss'] = {}

timeslot_pnl[util.PREMARKET]['profit']['long'] = 0
timeslot_pnl[util.PREMARKET]['profit']['short'] = 0
timeslot_pnl[util.PREMARKET]['loss']['long'] = 0
timeslot_pnl[util.PREMARKET]['loss']['short'] = 0
timeslot_pnl[util.SESSION_ONE_AM]['profit']['long'] = 0
timeslot_pnl[util.SESSION_ONE_AM]['profit']['short'] = 0
timeslot_pnl[util.SESSION_ONE_AM]['loss']['long'] = 0
timeslot_pnl[util.SESSION_ONE_AM]['loss']['short'] = 0
timeslot_pnl[util.SESSION_TWO_AM]['profit']['long'] = 0
timeslot_pnl[util.SESSION_TWO_AM]['profit']['short'] = 0
timeslot_pnl[util.SESSION_TWO_AM]['loss']['long'] = 0
timeslot_pnl[util.SESSION_TWO_AM]['loss']['short'] = 0
timeslot_pnl[util.SESSION_THREE_AM]['profit']['long'] = 0
timeslot_pnl[util.SESSION_THREE_AM]['profit']['short'] = 0
timeslot_pnl[util.SESSION_THREE_AM]['loss']['long'] = 0
timeslot_pnl[util.SESSION_THREE_AM]['loss']['short'] = 0
timeslot_pnl[util.SESSION_FOUR_AM]['profit']['long'] = 0
timeslot_pnl[util.SESSION_FOUR_AM]['profit']['short'] = 0
timeslot_pnl[util.SESSION_FOUR_AM]['loss']['long'] = 0
timeslot_pnl[util.SESSION_FOUR_AM]['loss']['short'] = 0
timeslot_pnl[util.SESSION_FIVE_AM]['profit']['long'] = 0
timeslot_pnl[util.SESSION_FIVE_AM]['profit']['short'] = 0
timeslot_pnl[util.SESSION_FIVE_AM]['loss']['long'] = 0
timeslot_pnl[util.SESSION_FIVE_AM]['loss']['short'] = 0
timeslot_pnl[util.SESSION_SIX_AM]['profit']['long'] = 0
timeslot_pnl[util.SESSION_SIX_AM]['profit']['short'] = 0
timeslot_pnl[util.SESSION_SIX_AM]['loss']['long'] = 0
timeslot_pnl[util.SESSION_SIX_AM]['loss']['short'] = 0
timeslot_pnl[util.MIDDAY]['profit']['long'] = 0
timeslot_pnl[util.MIDDAY]['profit']['short'] = 0
timeslot_pnl[util.MIDDAY]['loss']['long'] = 0
timeslot_pnl[util.MIDDAY]['loss']['short'] = 0
timeslot_pnl[util.PM]['profit']['long'] = 0
timeslot_pnl[util.PM]['profit']['short'] = 0
timeslot_pnl[util.PM]['loss']['long'] = 0
timeslot_pnl[util.PM]['loss']['short'] = 0
timeslot_pnl[util.POWER_HOUR]['profit']['long'] = 0
timeslot_pnl[util.POWER_HOUR]['profit']['short'] = 0
timeslot_pnl[util.POWER_HOUR]['loss']['long'] = 0
timeslot_pnl[util.POWER_HOUR]['loss']['short'] = 0
timeslot_pnl[util.AFTER_HOUR]['profit']['long'] = 0
timeslot_pnl[util.AFTER_HOUR]['profit']['short'] = 0
timeslot_pnl[util.AFTER_HOUR]['loss']['long'] = 0
timeslot_pnl[util.AFTER_HOUR]['loss']['short'] = 0
#######################


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

		start_time[sym] = '00:00:00'
		end_time[sym] = '00:00:00'

	# if execution is a BUY	
	if row['B/S'] == 'Buy':
		# if current symbol is different from the last streamed symbol, print a line
		if last_sym != sym:
			last_sym = sym
			print('')
		if sharesInPos[sym] == 0:
			start_time[sym] = row['Time']

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
				timeslot_pnl[util.getTimeSlot(row['Time'])]['profit']['short'] += (abs(avgInPosPrice[sym]) - row['Price']) * row['Shares']


			# if it's a loser
			else:
				num_losers_short += 1
				loser_shares_short += row['Shares']
				total_loss_short += (abs(avgInPosPrice[sym]) - row['Price']) * row['Shares']
				timeslot_pnl[util.getTimeSlot(row['Time'])]['loss']['short'] += (abs(avgInPosPrice[sym]) - row['Price']) * row['Shares']

			# if closing the short position
			if sharesInPos == 0:
				pnlByTickers[sym] += pnlInPos
				total_pnl_short += pnlInPos
				avgInPosPrice[sym] = 0
				pnlInPos = 0

				end_time[sym] = row['Time']
				total_hold_time_short += timeDiff(start_time[sym], end_time[sym])
				start_time[sym] = '00:00:00'
				end_time[sym] = '00:00:00'
				num_positions_short += 1

				print('------------ ' + sym + ' END Short ------------\n')

	# if execution is a SELL or SHORT
	elif (row['B/S'] == 'Sell' or row['B/S'] == 'Shrt'):
		# if current symbol is different from the last streamed symbol, print a line
		if last_sym != sym:
			last_sym = sym
			print('')
		if sharesInPos[sym] == 0:
			start_time[sym] = '00:00:00'

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
				timeslot_pnl[util.getTimeSlot(row['Time'])]['profit']['long'] += (row['Price'] - avgInPosPrice[sym]) * row['Shares']

			# if it's a loser
			else:
				num_losers_long += 1
				loser_shares_long += row['Shares']
				total_loss_long += (row['Price'] - avgInPosPrice[sym]) * row['Shares']
				timeslot_pnl[util.getTimeSlot(row['Time'])]['loss']['long'] += (row['Price'] - avgInPosPrice[sym]) * row['Shares']

			# if closing the long position 
			if sharesInPos[sym] == 0:
				pnlByTickers[sym] += pnlInPos[sym]
				total_pnl_long += pnlInPos[sym]
				avgInPosPrice[sym] = 0
				pnlInPos[sym] = 0

				end_time[sym] = row['Time']
				total_hold_time_long += timeDiff(start_time[sym], end_time[sym])
				start_time[sym] = '00:00:00'
				end_time[sym] = '00:00:00'
				num_positions_long += 1


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
print('\n')

print('# of long positions: ' + str(num_positions_long))
print('# of short positions: ' + str(num_positions_short))
print('total long hold time in seconds: ' + str(total_hold_time_long))
print('total short hold time in seconds: ' + str(total_hold_time_short))
print('\n')

pnl_checksum = 0
for timeSlot in timeslot_pnl:
	pnl_long = 0
	pnl_short = 0
	pnl_long += timeslot_pnl[timeSlot]['profit']['long'] + timeslot_pnl[timeSlot]['loss']['long']
	pnl_short += timeslot_pnl[timeSlot]['profit']['short'] + timeslot_pnl[timeSlot]['loss']['short']
	pnl_checksum += pnl_long + pnl_short
	print(timeSlot + ' long pnl: ' + str(round(pnl_long, 2)))
	print(timeSlot + ' short pnl: ' + str(round(pnl_short, 2)))
	print('')
print('pnl checksum: ' + str(round(pnl_checksum, 2)))
print('\n')