import akshare as ak
import pandas as pd
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create data directory if it doesn't exist
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def save_hk_stocks():
    try:
        # Fetch Hong Kong stock data
        logger.info("Attempting to fetch Hong Kong stock data...")
        df = ak.stock_hk_spot()
        
        if df is None:
            logger.error("API returned None instead of DataFrame")
            return None
            
        if df.empty:
            logger.error("API returned empty DataFrame")
            return None
            
        logger.info(f"Successfully fetched data with {len(df)} rows")
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'hk_stocks_{timestamp}.csv'
        filepath = os.path.join(DATA_DIR, filename)
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        logger.info(f"Successfully saved Hong Kong stock data to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Error saving Hong Kong stock data: {str(e)}", exc_info=True)
        return None

if __name__ == "__main__":
    result = save_hk_stocks()
    if result is None:
        logger.error("Failed to save Hong Kong stock data")
    else:
        logger.info(f"Data saved successfully to: {result}") 