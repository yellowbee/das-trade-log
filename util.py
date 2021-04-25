import datetime

# calcuate the time difference between two timestamps in string
# start: '00:00:00', end: '00:00:01'
def timeDiff(start, end):
	datetimeFormat = '%H:%M:%S'
	start_time = datetime.datetime.strptime(start, datetimeFormat)
	end_time = datetime.datetime.strptime(end, datetimeFormat)

	print(start_time < end_time)

	if (start_time > end_time):
		raise Exception("Start time cannot be bigger than end time!")

	diff = end_time - start_time
	return diff.seconds


# Returns the time slot in string of a timestamp
# time slot:
# 	PREMARKET 4:00 - 9:30
#   SESSION_ONE_AM 9:30 - 10:00
#   SESSION_TWO_AM 10:00 - 10:30
#   SESSION_THREE_AM 10:30 - 11:00
#   SESSION_FOUR_AM 11:00 - 11:30
#   SESSION_FIVE_AM  11:30 - 12:00
#   SESSION_SIX_AM  12:00 - 12:30
#   MIDDAY 12:30 - 13:30
#   PM 13:30 - 15:00
#   POWER_HOUR 15:00 - 16:00
# timestamp example: '00:00:01'
PREMARKET = 'PREMARKET'
SESSION_ONE_AM = 'SESSION_ONE_AM'
SESSION_TWO_AM = 'SESSION_TWO_AM'
SESSION_THREE_AM = 'SESSION_THREE_AM'
SESSION_FOUR_AM = 'SESSION_FOUR_AM'
SESSION_FIVE_AM = 'SESSION_FIVE_AM'
SESSION_SIX_AM = 'SESSION_SIX_AM'
MIDDAY = 'MIDDAY'
PM = 'PM'
POWER_HOUR = 'POWER_HOUR'
AFTER_HOUR = 'AFTER_HOUR'

datetimeFormat = '%H:%M:%S'
FOUR = datetime.datetime.strptime('04:00:00', datetimeFormat)
NINE_THIRTY = datetime.datetime.strptime('09:30:00', datetimeFormat)
TEN = datetime.datetime.strptime('10:00:00', datetimeFormat)
TEN_THIRTY = datetime.datetime.strptime('10:30:00', datetimeFormat)
ELEVEN = datetime.datetime.strptime('11:00:00', datetimeFormat)
ELEVEN_THIRTY = datetime.datetime.strptime('11:30:00', datetimeFormat)
TWELVE = datetime.datetime.strptime('12:00:00', datetimeFormat)
TWELVE_THIRTY = datetime.datetime.strptime('12:30:00', datetimeFormat)
THIRTEEN_THIRTY = datetime.datetime.strptime('13:30:00', datetimeFormat)
FIFTEEN = datetime.datetime.strptime('15:00:00', datetimeFormat)
SIXTEEN = datetime.datetime.strptime('16:00:00', datetimeFormat)
# return
# 	-1: if ts1 < ts2
#    0: if ts = ts2
#    1: if ts > ts2
def compareTimestamps(ts1_dt, ts2_dt):
	if (ts1_dt < ts2_dt):
		return -1
	elif (ts1_dt == ts2_dt):
		return 0
	else:
		return 1


def getTimeSlot(time):
	datetimeFormat = '%H:%M:%S'
	time_dt = datetime.datetime.strptime(time, datetimeFormat)
	if (compareTimestamps(time_dt, FOUR) >= 0 and compareTimestamps(time_dt, NINE_THIRTY) < 0):
		return PREMARKET
	elif (compareTimestamps(time_dt, NINE_THIRTY) >= 0 and compareTimestamps(time_dt, TEN) < 0):
		return SESSION_ONE_AM
	elif (compareTimestamps(time_dt, TEN) >= 0 and compareTimestamps(time_dt, TEN_THIRTY) < 0):
		return SESSION_TWO_AM
	elif (compareTimestamps(time_dt, TEN_THIRTY) >= 0 and compareTimestamps(time_dt, ELEVEN) < 0):
		return SESSION_THREE_AM
	elif (compareTimestamps(time_dt, ELEVEN) >= 0 and compareTimestamps(time_dt, ELEVEN_THIRTY) < 0):
		return SESSION_FOUR_AM
	elif (compareTimestamps(time_dt, ELEVEN_THIRTY) >= 0 and compareTimestamps(time_dt, TWELVE) < 0):
		return SESSION_FIVE_AM
	elif (compareTimestamps(time_dt, TWELVE) >= 0 and compareTimestamps(time_dt, TWELVE_THIRTY) < 0):
		return SESSION_SIX_AM
	elif (compareTimestamps(time_dt, TWELVE_THIRTY) >= 0 and compareTimestamps(time_dt, THIRTEEN_THIRTY) < 0):
		return MIDDAY
	elif (compareTimestamps(time_dt, THIRTEEN_THIRTY) >= 0 and compareTimestamps(time_dt, FIFTEEN) < 0):
		return PM
	elif (compareTimestamps(time_dt, FIFTEEN) >= 0 and compareTimestamps(time_dt, SIXTEEN) < 0):
		return POWER_HOUR
	else:
		return AFTER_HOUR


'''
print(getTimeSlotOfTimestamp('8:30:00'))
print(getTimeSlotOfTimestamp('9:30:00'))
print(getTimeSlotOfTimestamp('10:30:00'))
print(getTimeSlotOfTimestamp('12:35:00'))
print(getTimeSlotOfTimestamp('14:25:00'))
print(getTimeSlotOfTimestamp('15:25:00'))
'''


