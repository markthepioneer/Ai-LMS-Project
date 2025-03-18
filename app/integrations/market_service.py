# integrations/market_service.py
import os
import logging
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Keys (in production, use environment variables)
MARKET_API_KEY = os.getenv("MARKET_DATA_API_KEY", "demo_key")

class MarketServiceError(Exception):
    """Custom exception for market service errors"""
    pass

class MarketService:
    """Service for retrieving market data"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or MARKET_API_KEY
        self.base_url = "https://api.marketdata.example.com/v1"  # Example URL
    
    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price for a stock symbol
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Dictionary with price information
        """
        try:
            # In a real implementation, this would make an API call
            # For now, return dummy data
            
            # Example API call (commented out)
            # response = requests.get(
            #     f"{self.base_url}/quote/{symbol}",
            #     params={"apikey": self.api_key}
            # )
            # response.raise_for_status()
            # data = response.json()
            
            # Dummy data for demo purposes
            data = {
                "symbol": symbol,
                "price": self._get_dummy_price(symbol),
                "change": 1.25,
                "change_percent": 0.5,
                "last_updated": datetime.now().isoformat()
            }
            
            return data
        
        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {str(e)}")
            raise MarketServiceError(f"Failed to get current price: {str(e)}")
    
    def get_historical_prices(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: Optional[str] = None,
        interval: str = "1d"
    ) -> List[Dict[str, Any]]:
        """
        Get historical price data for a stock symbol
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format (defaults to today)
            interval: Data interval ('1d', '1w', '1m')
            
        Returns:
            List of historical price dictionaries
        """
        try:
            # In a real implementation, this would make an API call
            # For now, return dummy data
            
            end_date = end_date or datetime.now().strftime("%Y-%m-%d")
            
            # Example API call (commented out)
            # response = requests.get(
            #     f"{self.base_url}/historical/{symbol}",
            #     params={
            #         "apikey": self.api_key,
            #         "start_date": start_date,
            #         "end_date": end_date,
            #         "interval": interval
            #     }
            # )
            # response.raise_for_status()
            # data = response.json()
            
            # Generate dummy data
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Simple logic to generate some dummy data points
            data = []
            current_date = start
            price = self._get_dummy_price(symbol)
            
            while current_date <= end:
                # Add some random variation to price
                price = price + (((hash(current_date.isoformat()) % 100) - 50) / 1000) * price
                
                data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "open": round(price * 0.99, 2),
                    "high": round(price * 1.02, 2),
                    "low": round(price * 0.98, 2),
                    "close": round(price, 2),
                    "volume": 1000000 + (hash(current_date.isoformat()) % 10000000)
                })
                
                # Move to next date based on interval
                if interval == "1d":
                    current_date = current_date.replace(day=current_date.day + 1)
                elif interval == "1w":
                    current_date = current_date.replace(day=current_date.day + 7)
                elif interval == "1m":
                    # Simple month increment logic
                    if current_date.month == 12:
                        current_date = current_date.replace(year=current_date.year + 1, month=1)
                    else:
                        current_date = current_date.replace(month=current_date.month + 1)
            
            return data
        
        except Exception as e:
            logger.error(f"Error getting historical prices for {symbol}: {str(e)}")
            raise MarketServiceError(f"Failed to get historical prices: {str(e)}")
    
    def search_symbols(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for stock symbols
        
        Args:
            query: Search query
            
        Returns:
            List of matching symbols
        """
        try:
            # In a real implementation, this would make an API call
            # For now, return dummy data
            
            # Example API call (commented out)
            # response = requests.get(
            #     f"{self.base_url}/search",
            #     params={
            #         "apikey": self.api_key,
            #         "query": query
            #     }
            # )
            # response.raise_for_status()
            # data = response.json()
            
            # Dummy data for common stock symbols
            dummy_symbols = [
                {"symbol": "AAPL", "name": "Apple Inc.", "exchange": "NASDAQ"},
                {"symbol": "MSFT", "name": "Microsoft Corporation", "exchange": "NASDAQ"},
                {"symbol": "GOOGL", "name": "Alphabet Inc.", "exchange": "NASDAQ"},
                {"symbol": "AMZN", "name": "Amazon.com Inc.", "exchange": "NASDAQ"},
                {"symbol": "META", "name": "Meta Platforms Inc.", "exchange": "NASDAQ"},
                {"symbol": "TSLA", "name": "Tesla Inc.", "exchange": "NASDAQ"},
                {"symbol": "V", "name": "Visa Inc.", "exchange": "NYSE"},
                {"symbol": "JNJ", "name": "Johnson & Johnson", "exchange": "NYSE"},
                {"symbol": "WMT", "name": "Walmart Inc.", "exchange": "NYSE"},
                {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "exchange": "NYSE"}
            ]
            
            # Filter based on query
            query = query.lower()
            results = [
                symbol for symbol in dummy_symbols
                if query in symbol["symbol"].lower() or query in symbol["name"].lower()
            ]
            
            return results
        
        except Exception as e:
            logger.error(f"Error searching symbols: {str(e)}")
            raise MarketServiceError(f"Failed to search symbols: {str(e)}")
    
    def _get_dummy_price(self, symbol: str) -> float:
        """Generate a consistent dummy price based on symbol"""
        # Use hash of symbol to generate a price between $10 and $1000
        price_seed = sum(ord(c) for c in symbol)
        return round(10 + (price_seed % 990), 2)

# Singleton instance
market_service = MarketService()
