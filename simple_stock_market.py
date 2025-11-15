from decimal import Decimal
from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
from threading import Lock
from typing import List, Dict, Optional
import math

class Stock:
    def __init__(self,_type,symbol,last_dividend,fixed_dividend,par_value):
        self.symbol=symbol
        self._type=_type
        self.last_dividend=last_dividend
        self.fixed_dividend=fixed_dividend
        self.par_value=par_value

    def dividend_yield(self, price):
        """
        Calculate Dividend Yield based on the stock type
        price: Decimal > 0
        Returns Decimal (may raise Value Error for Invalid price)
        """
        if price <= 0:
            raise ValueError("Price should be greater than zero to compute dividend")
        if self._type.lower() == 'common':
            return (self.last_dividend/price).quantize(Decimal("0.000001"))
        elif self._type.lower() == 'preferred':
            if self.fixed_dividend:
                return ((self.fixed_dividend * self.par_value) / price).quantize(Decimal("0.000001"))
        else:
            raise ValueError(f"Unknown stock type: {self._type}")

    def pe_ratio(self,price):
        """
        Calculate p/e ratio : price / dividend
        If Dividend is 0 return None to indicate undefined
        """
        #Dividend for P/E: for common -> last_dividend; preferred -> fixed_dividend * par_value
        if self._type.lower() == 'common':
            dividend=self.last_dividend
        else:
            dividend=(self.fixed_dividend * self.par_value) if self.fixed_dividend else 0.0

        if dividend == 0:
            return None
        return (price/dividend).quantize(Decimal(0.000001))

class Trade:
    def __init__(self,timestamp,stock_symbol,quantity,buy_sell,price):
        self.timestamp = timestamp 
        self.stock_symbol = stock_symbol 
        self.quantity = quantity
        if self.quantity <= 0:
            raise ValueError("Trade quantity must be greater than 0")
        elif self.price <= 0:
            raise ValueError("Trade price must be greater than zero")
        self.buy_sell=buy_sell.upper()
        if self.buy_sell not in ("BUY","SELL"):
            raise ValueError("buy_sell must be 'BUY' or 'SELL'")

class Exchange:
    def __init__(self):
        self._stocks: Dict[str, Stock] = {}
        self._trades: List[Trade] = []
        self._lock =Lock()

        def add_stock(self, stock:Stock):
            self._stocks[stock.symbol.upper()] = stock

        def get_stock(self, symbol:str):
            return self._stocks.get(symbol.upper())
        
        def record_trade(self, stock_symbol: str, quantity: int, buy_sel: str, price: Decimal, timestamp: Optional[datetime]):
            """
            Record a trade. Thread-safe append to internal trade list.
            If timestamp not provided, uses current UTC time.
            """
            ts=timestamp or datetime.utcnow()
            trade = Trade(timestamp=ts, stock_symbol=stock_symbol.upper(), quantity=quantity, buy_sell=buy_sell, price=price)
            with self._lock:
                self._trades.append(trade)
            return trade

        def trades_for_stock_in_interval(self,stock_symbol: str, minutes: int):
            """
            Returns trades for stock in last minutes 'minutes' from now
            """
            interval = datetime.utcnow() - timedelta(minutes=minutes)
            symbol = stock_symbol.upper()
            return [t for t in self._trades if t.stock_symbol == symbol and t.timestamp >= interval]

        def vol_weighted_stock_price(self, stock_symbol,minutes):
            """
            VWSP = sum(price_i * quantity_i) / sum(quantity_i) for 'trades' in last 'minutes'
            Returns None if no trades in that window
            """
            trades = self.trades_for_stock_in_interval(stock_symbol, minutes)
            if not trades:
                return None
            num = 0.0
            den=0
            for t in trades:
                num += (t.price * Decimal(t.quantity))
                den += t.quantity
            if den == 0:
                return None
            vws_price = (num/Decimal(den)).quantize(Decimal("0.000001"))
            return vws_price

        def gbce_all_share_index(self,minutes):
            """
            GBCE All Share Index = geometric mean of VWSP for all stocks (use VWSP for each stock)
            Only stocks that have VWSP (i.e. trades in last 'minutes') are considered.
            Returns None if no VWSP's are available
            """
            vws_prices = []
            for symbol in self._stocks:
                v = self.vol_weighted_stock_price(symbol,minutes)
                if v is not None and v > 0:
                    vws_prices.append(float(v))
            if not vws_prices:
                return None

            logs_sum = sum(math.log(p) for p in vws_prices)
            geom_mean = math.exp(logs_sum / len(vws_prices))
            #return as Decimal rounded sensibly
            return Decimal(str(geom_mean)).quantize(Decimal("0.000001"))

        def all_trades(self):
            return list(self._trades)

def _sample_run():
    ex=Exchange()
    # Add sample stocks from the assignment (numbers are pennies in PDF; we treat them as decimals)
    ex.add_stock(Stock(symbol="Tea", _type="Common", last_dividend=Decimal("0"), fixed_dividend=None, par_value=Decimal("100")))
    ex.add_stock(Stock(symbol="POP", _type="Common", last_dividend=Decimal("8"), fixed_dividend=None, par_value=Decimal("100")))
    ex.add_stock(Stock(symbol="ALE", _type="Common", last_dividend=Decimal("23"), fixed_dividend=None, par_value=Decimal("60")))
    ex.add_stock(Stock(symbol="GIN", _type="Preferred", last_dividend=Decimal("8"), fixed_dividend=("0.02"), par_value=Decimal("100")))
    ex.add_stock(Stock(symbol="JOE", _type="Common", last_dividend=Decimal("13"), fixed_dividend=None, par_value=Decimal("250")))

    now = datetime.utcnow()

    # Record some trades (timestamps: some now, some older)
    ex.record_trade("POP", quantity=50, buy_sell="BUY", price=Decimal("100"), timestamp=now - timedelta(minutes=1))
    ex.record_trade("POP", quantity=20, buy_sell="SELL", price=Decimal("101"), timestamp=now - timedelta(minutes=2))
    ex.record_trade("ALE", quantity=10, buy_sell="BUY", price=Decimal("60"), timestamp=now - timedelta(minutes=3))
    ex.record_trade("GIN", quantity=5, buy_sell="BUY", price=Decimal("120"), timestamp=now - timedelta(minutes=4))
    ex.record_trade("JOE", quantity=25, buy_sell="SELL", price=Decimal("95"), timestamp=now - timedelta(minutes=6))

    # Show dividend yield examples
    pop = ex.get_stock("POP")
    print("POP dividend yield @ price 100:", pop.dividend_yield(Decimal("100")))

    gin = ex.get_stock("GIN")
    print("GIN dividend yield @ price 100:", pop.dividend_yield(Decimal("100")))

    # P/E ratio examples
    print("POP P/E @ price 100:", pop.pe_ratio(Decimal("100")))

    # TEA has zero dividend -> P/E undefined
    tea = ex.get_stock("TEA")
    print("TEA P/E @ price 100:", pop.pe_ratio(Decimal("100")))

    # VWSP (last 5 minutes)
    print("POP VWSP (5min):", ex.vol_weighted_stock_price("POP", minutes=5))
    print("ALE VWSP (5min):", ex.vol_weighted_stock_price("ALE", minutes=5))
    print("JOE VWSP (5min):", ex.vol_weighted_stock_price("JOE", minutes=5))

    # GBCE All Share Index (considers only stocks with VWSP available)
    print("GBCE All Share Index (5min):", ex.gbce_all_ahare_index(minutes=5))

    # List all recorded trades
    print("\nAll recoreded trades:")
    for t in ex.all_trades():
        print(f"{t.timestamp.isoformat()} | {t.stock_symbol} | {t.buy_sell} | qty={t.quantity} | price={t.price}")

if __name__ == "__main__":
    _sample_run()

        




