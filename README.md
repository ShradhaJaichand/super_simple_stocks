Super Simple Stock Market – Python Implementation
Overview
This project is an object-oriented implementation of the "Super Simple Stocks" assignment for the Global Beverage Corporation Exchange (GBCE). The system models stocks and trades entirely in memory and computes key financial metrics as required.
The implementation provides only the functionality requested in the assignment and follows a clean, minimal, production-quality design.
Features Implemented
1.	For a given stock:

         •	Calculate Dividend Yield (Common and Preferred)
         
         •	Calculate P/E Ratio
         
         •	Record a trade with timestamp, quantity, buy/sell indicator, and price
         
         •	Compute the Volume Weighted Stock Price (VWSP) using trades from the last 5 minutes

2.	For all stocks:
   
         •	Calculate the GBCE All Share Index using the geometric mean of all Volume Weighted Stock Prices
         Assignment Constraints (All Satisfied)
         
         •	Implemented in Python
         
         •	All data is stored in memory
         
         •	No database, no GUI, and no file I/O
         
         •	No unnecessary features or architectural layers (e.g., MVC)
         
         •	Only core functionality required by the assignment is included
         
         •	Production-quality, testable code with clear object-oriented design

Architecture
This project follows a simple Domain Model architecture where each major concept is represented as a class:

1.	Stock
   
      •	Holds stock details such as symbol, type, last dividend, fixed dividend, and par value
      
      •	Computes Dividend Yield and P/E Ratio

2.	Trade

      •	Represents a trade operation with timestamp, stock symbol, quantity, buy/sell indicator, and price

3.	Exchange

      •	Stores stocks and trades in memory
      
      •	Records trades
      
      •	Computes Volume Weighted Stock Price (VWSP) using trades from the past 5 minutes
      
      •	Computes the GBCE All Share Index

Formulas Implemented

Dividend Yield (Common Stock):
Last Dividend / Price

Dividend Yield (Preferred Stock):
(Fixed Dividend * Par Value) / Price

P/E Ratio:
Price / Dividend
Dividend is last dividend for common stocks, and fixed dividend * par value for preferred stocks

Volume Weighted Stock Price (VWSP):
Sum of (Price * Quantity) / Sum of Quantity
Computed using trades from the past 5 minutes only

GBCE All Share Index:
Geometric mean of the VWSP values for all stocks

Project Structure
super-simple-stocks/
super_simple_stocks.py (core implementation)
README.txt (this file)

Usage Example
Below is a minimal sample demonstrating how to interact with the classes:
from decimal import Decimal
from super_simple_stocks import Stock, Exchange
ex = Exchange()

# Add stock
ex.add_stock(Stock("POP", "Common", Decimal(8), None, Decimal(100)))

# Record trades
ex.record_trade("POP", 50, "BUY", Decimal(100))
ex.record_trade("POP", 30, "SELL", Decimal(101))

# Fetch stock
stock = ex.get_stock("POP")

# Calculate values
print(stock.dividend_yield(Decimal(100)))

print(stock.pe_ratio(Decimal(100)))

print(ex.volume_weighted_stock_price("POP"))

print(ex.gbce_all_share_index())

Testing
The code is structured to allow easy creation of unit tests to validate:

         •	Dividend yield calculations
         
         •	P/E ratio behavior when dividend is zero
         
         •	VWSP calculations with varying trade compositions
         
         •	GBCE index calculations

License
This project is open-source and free to use.
Author
Your Name
GitHub: https://github.com/ShradhaJaichand






