import math
import numpy as np
from enum import Enum
import random

class OptionCalculator:

    def __init__(self, stockPrice, impliedVol, daysOut, trials) -> None:
        self.stockPrice = stockPrice
        self.impliedVol = impliedVol
        self.daysOut = daysOut
        self.standardDeviation = impliedVol * math.sqrt(daysOut/365)
        self.trials = trials
        

    def calcCallCreditSpread(self, strikePrice1, Premium1, strikePrice2, Premium2) -> float:
        # Retrieve inputs
        credit = Premium1 - Premium2 - 2.6
        # 2.6 is commission
        total = 0
        for i in range(self.trials):
            val = self.getRandomNumbers()
            if val > strikePrice1 and val >= strikePrice2:
                total += strikePrice1 - strikePrice2 + credit
            elif val <= strikePrice1:
                total += credit
            else:
                amt = strikePrice1 - val + credit
                total += amt
        print(total/self.trials)
        return total/self.trials
    
    def calcCallDebitSpread(self, strikePrice1, Premium1, strikePrice2, Premium2):
        debit = Premium1 - Premium2 + 2.6
        # 2.6 is commission with a 0.65 per contract bought/sold
        total = 0
        for i in range(self.trials):
            val = self.getRandomNumbers()
            if val <= strikePrice1:
                total -= debit
            elif val >= strikePrice2:
                total += strikePrice2 - strikePrice1 - debit
            else:
                total += val - strikePrice1 - debit
        print(total/self.trials)
        return total/self.trials
    
    def calcPutCreditSpread(self, strike1, premium1, strike2, premium2):
        credit = premium1 - premium2 - 2.6
        # 2.6 is commission for 4 contracts
        total = 0
        for i in range(self.trials):
            val = self.getRandomNumbers()
            if val >= strike1:
                total += credit
            elif val <= strike2:
                total += strike1 - strike2 + credit
            else:
                amt = strike1 - val + credit
                total += amt
        print(total/self.trials)
        return total/self.trials
    
    def calcPutDebitSpread(self, strike1, premium1, strike2, premium2):
        debit = premium1 - premium2
        total = 0
        for i in range(self.trials):
            val = self.getRandomNumbers()
            if val <= strike2:
                total += strike1 - strike2 - debit
            elif val >= strike1:
                total -= debit
            else:
                amt = strike1 - val - debit
                total += amt
        print(total/self.trials)
        return total/self.trials
    
    def calcLongStraddle(self, strikePrice, premium1, premium2):
        debit = premium1 + premium2 + 2.6
        total = 0
        for i in range(self.trials):
            val = self.getRandomNumbers()
            if (val > strikePrice):
                total += val - strikePrice - debit
            elif (val < strikePrice):
                total += strikePrice - val - debit
            else:
                total -= debit
        print(total/self.trials)
        return total/self.trials
    
    def calcLongStrangle(self, strikeCall, premiumCall, strikePut, premiumPut):
        debit = premiumCall + premiumPut
        total = 0
        for i in range(self.trials):
            val = self.getRandomNumbers()
            if (val >= strikeCall):
                total += val - strikeCall - debit
            elif (val <= strikePut):
                total += strikePut - val - debit
            else:
                total -= debit
        print(total/self.trials)
        return total/self.trials
    
    def calcShortStrangle(self, strikeCall, premiumCall, strikePut, premiumPut):
        credit = premiumCall + premiumPut
        total = 0
        for i in range(self.trials):
            val = self.getRandomNumbers()
            if (val >= strikeCall):
                total -= val - strikeCall + credit
            elif (val <= strikePut):
                total -= strikePut - val + credit
            else:
                total += credit
        print(total/self.trials)
        return total/self.trials
    
    def calcShortStraddle(self, strikePrice, premiumCall, premiumPut):
        credit = premiumCall + premiumPut
        total = 0
        for i in range(self.trials):
            val = self.getRandomNumbers()
            if (val >= strikePrice):
                total += strikePrice - val + credit
            else:
                total += val - strikePrice + credit
        print(total/self.trials)
        return total/self.trials
    
    def calcIronCondor(self, strikeCS, premiumCS, strikeCL, premiumCL, strikePS, premiumPS, strikePL, premiumPL):
        credit = premiumCS + premiumPS - premiumCL - premiumPL
        total = 0
        for i in range(self.trials):
            val = self.getRandomNumbers()
            if (val >= strikePS and val <= strikeCS):
                total += credit
            elif (val <= strikePS and val >= strikePL):
                total += val - strikePS + credit
            elif (val <= strikePL):
                total += credit + strikePL - strikePS
            elif (val >= strikeCS and val <= strikeCL):
                total += strikeCS - val + credit
            else:
                total += credit + strikeCS - strikeCL
        print(total/self.trials)
        return total/self.trials
    
    def calcIronFly(self, strikeShort, premiumCS, premiumPS, strikeCL, premiumCL, strikePL, premiumPL):
        credit = premiumCS + premiumPS - premiumCL - premiumPL
        total = 0
        for i in range(self.trials):
            total += credit
            val = self.getRandomNumbers()
            if (val >= strikeShort and val <= strikeCL):
                total += strikeShort - val
            elif (val >= strikeCL):
                total += strikeShort - strikeCL
            elif (val <= strikeShort and val >= strikePL):
                total += val - strikeShort
            else:
                total += strikePL - strikeShort
        print(total/self.trials)
        return total/self.trials
    
    def calcLongCall(self, strikeCall, premium):
        total = 0
        for i in range(self.trials):
            total -= premium
            val = self.getRandomNumbers()
            if (val > strikeCall):
                total += val - strikeCall
        print(total/self.trials)

    def calcLongPut(self, strikePut, premium):
        total = 0
        for i in range(self.trials):
            total -= premium
            val = self.getRandomNumbers()
            if (val < strikePut):
                total += strikePut - val

        print(total/self.trials)
        return total/self.trials
    
    def calcShortCall(self, strikeCall, premium):
        total = 0
        for i in range(self.trials):
            total += premium
            val = self.getRandomNumbers()
            if (val > strikeCall):
                total += strikeCall - val
        print(total/self.trials)
        return total/self.trials
    
    def calcShortPut(self, strikePut, premium):
        total = 0
        for i in range(self.trials):
            total += premium
            val = self.getRandomNumbers()
            if (val < strikePut):
                total += val - strikePut
        print(total/self.trials)
        return total/self.trials
        
    def getRandomNumbers(self) -> float:
        val = random.gauss(0, 1)
        return self.stockPrice * math.exp(self.standardDeviation * val)

optionCalculator = OptionCalculator(448.6, 0.11, 3, 100000)
optionCalculator.calcLongStraddle(448, 1.93, 3.01)
optionCalculator.calcCallDebitSpread(447, 3.65, 451, 1.48)
optionCalculator.calcCallCreditSpread(447, 3.65, 451, 1.48)
optionCalculator.calcPutCreditSpread(451, 3.41, 447, 1.57)
optionCalculator.calcPutDebitSpread(451, 3.41, 447, 1.57)
optionCalculator.calcLongStrangle(451, 1.48, 447, 1.57)
optionCalculator.calcShortStraddle(448, 1.93, 3.01)
optionCalculator.calcShortStrangle(451, 1.48, 447, 1.57)
optionCalculator.calcLongCall(447, 3.65)
optionCalculator.calcLongPut(451, 3.41)
optionCalculator.calcShortCall(447, 3.65)
optionCalculator.calcShortPut(451, 3.41)
# optionCalculator.calcIronCondor()
# optionCalculator.calcIronFly()

class OptionTradeType:
    CALL_CREDIT_SPREAD = 1
    CALL_DEBIT_SPREAD = 2
    PUT_CREDIT_SPREAD = 3
    PUT_DEBIT_SPREAD = 4
    LONG_STRANGLE = 5
    LONG_STRADDLE = 6
    SHORT_STRANGLE = 7
    SHORT_STRADDLE = 8
    IRON_CONDOR = 9
    IRON_BUTTERFLY = 10
    LONG_CALL = 11
    LONG_PUT = 12
    SHORT_CALL = 13
    SHORT_PUT = 14
