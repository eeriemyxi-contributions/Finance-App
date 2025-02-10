import streamlit as st
from models.stock import StockData
from utils.formatters import format_number
from utils.stock_utils import create_stock_chart
from database.connection import get_database
from datetime import datetime
from streamlit_lottie import st_lottie
import requests
import time
import yfinance as yf
from streamlit.components.v1 import html


@st.cache_data(ttl="5m")
def fetch_stock_data(symbol):
    """Fetch stock data with caching"""
    return StockData.get_stock_data(symbol)

def create_stock_cards():
   # Popular stock tickers with their names
   popular_stocks = {
       'AAPL': 'Apple',
       'GOOGL': 'Google', 
       'MSFT': 'Microsoft',
       'AMZN': 'Amazon',
       'META': 'Meta',
       'TSLA': 'Tesla',
       'NVDA': 'NVIDIA',
       'AMD': 'AMD',
       'NFLX': 'Netflix',
       'DIS': 'Disney'
   }
   
   # Start grid container
   html_content = """
   <div class="stock-grid-container">
   """
   
   for symbol, name in popular_stocks.items():
       try:
           stock = yf.Ticker(symbol)
           info = stock.info
           price = info.get('currentPrice', 0)
           change = info.get('regularMarketChangePercent', 0)
           volume = info.get('volume', 0)
           day_low = info.get('dayLow', 0)
           day_high = info.get('dayHigh', 0)
           pe_ratio = info.get('forwardPE', 'N/A')
           
           volume_str = f"${volume/1000000:.1f}M" if isinstance(volume, (int, float)) else "N/A"
           pe_ratio_str = f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A"
           
           html_content += f"""
               <div class="stock-card">
                   <div class="stock-header">
                       <div>
                           <div class="stock-symbol">{symbol}</div>
                           <div class="stock-name">{name}</div>
                       </div>
                       <div class="stock-price-container">
                           <div class="stock-price">${price:,.2f}</div>
                           <div class="price-change {'positive' if change >= 0 else 'negative'}">
                               {change:+.2f}%
                           </div>
                       </div>
                   </div>
                   
                   <div class="trading-stats">
                       <div class="stat-item">
                           <span class="stat-label">24h Vol</span>
                           <span class="stat-value">{volume_str}</span>
                       </div>
                       <div class="stat-item">
                           <span class="stat-label">P/E Ratio</span>
                           <span class="stat-value">{pe_ratio_str}</span>
                       </div>
                   </div>
                   
                   <div class="market-trends">
                       <div class="trend-item">
                           <span class="trend-label">Day Range</span>
                           <div class="trend-range">
                               <span>${day_low:,.2f}</span>
                               <span class="range-divider">-</span>
                               <span>${day_high:,.2f}</span>
                           </div>
                       </div>
                   </div>
                   
                   <div class="quick-actions">
                       <button class="action-btn buy">Buy</button>
                       <button class="action-btn sell">Sell</button>
                   </div>
               </div>
           """
           
       except Exception as e:
           st.error(f"Error fetching data for {symbol}: {str(e)}")
   
   html_content += "</div>"
   
   # CSS Styles
   styles = """
   <style>
       .stock-grid-container {
           display: grid;
           grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
           gap: 1.8rem;
           padding: 1.5rem;
           margin: 1.5rem;
       }
       
       .stock-card {
           background: #1F1F1F;
           border: 1px solid rgba(168, 85, 247, 0.2);
           border-radius: 12px;
           padding: 1.2rem;
           cursor: pointer;
           transition: all 0.3s ease;
           min-width: 0;
           position: relative;
           overflow: hidden;
       }
       
       .stock-card::before {
           content: '';
           position: absolute;
           top: 0;
           left: 0;
           width: 100%;
           height: 100%;
           background: linear-gradient(45deg, transparent, rgba(168, 85, 247, 0.03), transparent);
           transform: translateX(-100%);
           transition: 0.5s;
       }
       
       .stock-card:hover {
           transform: translateY(-3px);
           border-color: rgba(168, 85, 247, 0.4);
           box-shadow: 0 0 20px rgba(168, 85, 247, 0.15);
       }
       
       .stock-card:hover::before {
           transform: translateX(100%);
       }
       
       .stock-header {
           display: flex;
           justify-content: space-between;
           align-items: flex-start;
           margin-bottom: 0.8rem;
           border-bottom: 1px solid rgba(168, 85, 247, 0.1);
           padding-bottom: 0.8rem;
       }
       
       .stock-symbol {
           font-size: 1.3rem;
           font-family: Georgia, serif;
           font-weight: 400;
           background: linear-gradient(to right, #E2E8F0, #A855F7);
           -webkit-background-clip: text;
           -webkit-text-fill-color: transparent;
           white-space: nowrap;
       }
       
       .stock-name {
           color: #94A3B8;
           font-size: 0.9rem;
           margin: 0.3rem 0;
           white-space: nowrap;
           overflow: hidden;
           text-overflow: ellipsis;
       }
       
       .stock-price-container {
           display: flex;
           flex-direction: column;
           align-items: flex-end;
       }
       
       .stock-price {
           font-size: 1.4rem;
           font-weight: 700;
           font-family: Georgia, serif;
           color: #E2E8F0;
           margin: 0.5rem 0;
           white-space: nowrap;
           overflow: hidden;
           text-overflow: ellipsis;
           max-width: 100%;
       }
       
       .trading-stats {
           display: flex;
           justify-content: space-between;
           margin: 1rem 0;
           padding: 0.8rem 0;
           border-bottom: 1px solid rgba(168, 85, 247, 0.1);
       }
       
       .stat-item {
           display: flex;
           flex-direction: column;
       }
       
       .stat-label {
           font-size: 0.75rem;
           color: #94A3B8;
           margin-bottom: 0.2rem;
       }
       
       .stat-value {
           font-size: 0.9rem;
           color: #E2E8F0;
           font-weight: 400;
       }
       
       .market-trends {
           padding: 0.8rem 0;
       }
       
       .trend-item {
           margin-bottom: 0.5rem;
       }
       
       .trend-label {
           font-size: 0.75rem;
           color: #94A3B8;
           display: block;
           margin-bottom: 0.3rem;
       }
       
       .trend-range {
           display: flex;
           justify-content: space-between;
           align-items: center;
           font-size: 0.9rem;
           color: #E2E8F0;
       }
       
       .range-divider {
           color: #94A3B8;
           margin: 0 0.5rem;
       }
       
       .quick-actions {
           display: flex;
           gap: 0.8rem;
           margin-top: 1rem;
       }
       
       .action-btn {
           flex: 1;
           padding: 0.5rem;
           border-radius: 8px;
           font-size: 0.9rem;
           font-weight: 600;
           cursor: pointer;
           transition: all 0.2s ease;
           background: transparent;
           border: 1px solid rgba(168, 85, 247, 0.3);
           color: #E2E8F0;
       }
       
       .action-btn:hover {
           background: rgba(168, 85, 247, 0.1);
           border-color: rgba(168, 85, 247, 0.5);
       }
       
       .action-btn.buy {
           color: #4ADE80;
           border-color: rgba(74, 222, 128, 0.3);
       }
       
       .action-btn.buy:hover {
           background: rgba(74, 222, 128, 0.1);
           border-color: rgba(74, 222, 128, 0.5);
       }
       
       .action-btn.sell {
           color: #FB7185;
           border-color: rgba(251, 113, 133, 0.3);
       }
       
       .action-btn.sell:hover {
           background: rgba(251, 113, 133, 0.1);
           border-color: rgba(251, 113, 133, 0.5);
       }
       
       .price-change {
           padding: 0.3rem 1rem;
           border-radius: 20px;
           font-size: 0.9rem;
           font-weight: 600;
           display: inline-block;
           white-space: nowrap;
           margin-top: 0.5rem;
       }
       
       .positive {
           color: #4ADE80;
           background: rgba(74, 222, 128, 0.1);
           border: 1px solid rgba(74, 222, 128, 0.2);
       }
       
       .negative {
           color: #FB7185;
           background: rgba(251, 113, 133, 0.1);
           border: 1px solid rgba(251, 113, 133, 0.2);
       }
   </style>
   """
   
   # Combine styles and content
   full_html = f"{styles}{html_content}"
   
   st.components.v1.html(full_html, height=800, scrolling=True)
    # Function for loading the trading page
def trading_page():
    st.title('Trading Dashboard')
    symbol = st.text_input('Enter Stock Symbol (e.g., AAPL, GOOGL)', '').upper()
    content_placeholder = st.empty()
    # Stock symbol input

    if not symbol:
        create_stock_cards()
    else:
        content_placeholder.empty()
        hist_data, stock_info = StockData.get_stock_data(symbol)  

        # Add error handling for empty data
        if hist_data is not None and not hist_data.empty and stock_info is not None:
            # Display stock info
            col1, col2, col3 = st.columns(3)
            try:
                current_price = hist_data['Close'].iloc[-1]
                
                # Displaying the stock's values that were fetched from yfinance
                with col1:
                    st.metric(
                        label="Current Price",
                        value=f"${current_price:.2f}",
                        delta=f"{((current_price - hist_data['Close'].iloc[-2])/hist_data['Close'].iloc[-2]*100):.2f}%"
                    )
                
                with col2:
                    st.metric(
                        label="Market Cap",
                        value=format_number(stock_info.get('marketCap', 0))
                    )
                
                with col3:
                    st.metric(
                        label="Volume",
                        value=format_number(hist_data['Volume'].iloc[-1])
                    )

                # Display chart via trading view. simply rendering the tradingview tv
                create_stock_chart(symbol)
            
                def load_transaction_complete_lottie():
                    def load_lottieurl(url: str):
                            r = requests.get(url)
                            r.raise_for_status()
                            return r.json()

                    transaction_complete_lottie = "https://lottie.host/1c4c35ec-5ff0-4485-a777-8ed0f60b16e7/1mDPJ8vsSy.json"

                    
                    st.markdown('<div class="lottie-overlay"></div>', unsafe_allow_html=True)
                    lottie_json = load_lottieurl(transaction_complete_lottie)

                    st.markdown("""
                    <style>
                    .lottie-overlay {
                        position: fixed;
                        top:: 0;
                        left: 0;
                        width: 100vw;
                        height: 100vh;
                        background: rgba(0, 0, 0, 0.5);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                    if lottie_json:
                        st_lottie(
                            lottie_json,
                            speed=1,
                            loop=False,
                            height=300,
                            width=300,
                            key="lottie"
                        )
                        time.sleep(2)
                #Forms for trading -> buy and sell
                col1, col2 = st.columns(2)

                # for buying the stock
                with col1:
                    with st.form('buy_form'):
                        st.subheader('Buy Stock')
                        shares_to_buy = st.number_input('Number of shares to buy', min_value=0.0, step=1.0)
                        total_share_cost = shares_to_buy * current_price
                        st.write(f'Total Cost: ${total_share_cost:.2f}')
                        buy_submit_btn = st.form_submit_button('Buy')

                        if buy_submit_btn:
                            # Fetching the user's balance to check if the user has enough funds to buy the shares if not than error
                            if total_share_cost > st.session_state.user['balance']:
                                st.error('Insufficient funds!')
                            else:
                                # If the user has enough funds
                                db = get_database()
                                # Calling the update_portfolio function from the database with the argments as the user's id symbol, shares, current_price, and if it's a buy or a sell
                                if db.update_portfolio(st.session_state.user['id'], symbol, shares_to_buy, current_price, True):
                                    st.success(f'Successfully bought {shares_to_buy} shares of {symbol}')
                                    load_transaction_complete_lottie()
                                    st.session_state.user['balance'] -= total_share_cost  # substracting the amount from the user's total balance
                                    st.rerun()
                                else:
                                    st.error('Transaction Failed. Please try later')  # else Failed
                

                # for selling the stock
                with col2:
                    with st.form('sell_form'):
                        st.subheader('Sell Stock')
                        shares_to_sell = st.number_input('Number of shares to sell', min_value=0.0, step=1.0)
                        total_share_cost_for_selling = shares_to_sell * current_price
                        st.write(f'Total Cost : ${total_share_cost:.2f}')
                        sell_submit_btn = st.form_submit_button('Sell')

                        if sell_submit_btn:

                            db = get_database()
                            
                            # Firstly checking if the user has enough shares to sell. If not then error
                            if db.update_portfolio(st.session_state.user['id'], symbol, shares_to_sell, current_price, False):
                                st.success(f'Successfully Sold {shares_to_sell} shares of {symbol}')  # User had shares for that stocks so sell 
                                load_transaction_complete_lottie()
                                st.session_state.user['balance'] += total_share_cost_for_selling
                                st.rerun()
                            else:
                                st.error('Insufficient amount of Shares')  # else failed
            except (IndexError, KeyError) as e:
                    st.error(f"Error loading data for {symbol}. Please try again or check if the symbol is correct.")
        else:
            st.error('Invalid stock symbol or error fetching the data. Please check the symbol and try again.')


    if symbol:
        st.markdown("---")
        st.subheader(f"Latest News for {symbol}")
        
        
        news = StockData.get_stock_news(symbol)
        
        if news:
            for item in news:
                with st.container():
                    col1, col2 = st.columns([7,3])  # 70% for text, 30% for image
                    
                    with col1:
                        # Clean up the title and remove any special text
                        title = item.get('title', '').replace('[Read more]', '').strip()
                        
                        # Clean up the summary - safely handle None values
                        summary = item.get('summary', '')
                        if summary:  # Only process if summary exists
                            summary = summary.replace('In This Article:', '').replace('\n', ' ').strip()
                        else:
                            summary = "No summary available."
                        
                        # Use the published time from the news item instead of current time
                        published_time = item.get('published', datetime.now().strftime('%Y-%m-%d %H:%M'))
                        
                        st.markdown(f"""
                        ### {title}
                        <p style="color: #666; font-size: 0.8em;">{published_time}</p>
                        
                        {summary}
                        
                        <a href="{item.get('link', '#')}" target="_blank" style="color: #3b82f6; text-decoration: none;">Read Article</a>
                        """, unsafe_allow_html=True)
                    
                    if item.get('image'):
                        with col2:
                            st.image(item['image'], use_container_width=True)
                    
                    st.markdown("<hr style='margin: 2rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        else:
            st.info(f"No recent news available for {symbol}")