Moving Average = 
		AVERAGEX(
			DATESINPERIOD(
				'Stream'[WeekStart],
				LASTDATE('Stream'[WeekStart]) ,
				 -21 , 
				 DAY),
			CALCULATE(sum('Stream'[Count]))
			)