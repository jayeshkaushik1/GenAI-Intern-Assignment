import yfinance as yf
from typing import Dict, Any
from .base_tool import BaseTool

class StockTool(BaseTool):
    name = "stock_tool"
    description = "Fetches stock price for a given symbol. Use .NS for NSE (e.g. RELIANCE.NS) and .BO for BSE (e.g. TCS.BO). Args: symbol (str)"

    def to_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The stock symbol (e.g., AAPL, RELIANCE.NS, TCS.BO)"
                        }
                    },
                    "required": ["symbol"]
                }
            }
        }

    def execute(self, symbol: str) -> str:
        # Common corrections map
        CORRECTIONS = {
            "LICIND.NS": "LICI.NS",
            "LIC": "LICI.NS",
            "RELIANCE": "RELIANCE.NS",
            "TCS": "TCS.NS",
            "INFY": "INFY.NS",
            "HDFCBANK": "HDFCBANK.NS",
            "SBI": "SBIN.NS",
            "SBIN": "SBIN.NS",
            "TATAMOTORS": "TATAMOTORS.NS",
            "ZOMATO": "ZOMATO.NS"
        }
        
        # Auto correct common mistakes
        clean_symbol = symbol.upper().strip()
        if clean_symbol in CORRECTIONS:
            clean_symbol = CORRECTIONS[clean_symbol]
        
        # Helper to fetch price
        def fetch_price(sym):
            try:
                ticker = yf.Ticker(sym)
                if hasattr(ticker, "fast_info") and "last_price" in ticker.fast_info:
                    val = ticker.fast_info["last_price"]
                    if val is not None: return val
                
                hist = ticker.history(period="1d")
                if not hist.empty:
                    return hist["Close"].iloc[-1]
            except:
                pass
            return None

        # 1. Try exact/corrected symbol
        price = fetch_price(clean_symbol)
        
        # 2. If failed and no suffix, try adding .NS (NSE is default for India)
        if price is None and "." not in clean_symbol:
            clean_symbol = f"{clean_symbol}.NS"
            price = fetch_price(clean_symbol)

        if price is not None:
             try:
                 ticker = yf.Ticker(clean_symbol)
                 info = ticker.info
                 currency = info.get('currency', 'INR')
                 long_name = info.get('longName', clean_symbol)
                 return f"Stock: {long_name} ({clean_symbol})\nPrice: {currency} {price:.2f}"
             except:
                 return f"Stock: {clean_symbol}\nPrice: {price:.2f}"

        return f"No stock data found for symbol: {symbol}. Ensure correct suffix (.NS for NSE, .BO for BSE)."
