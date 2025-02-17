# Import all the necessary libraries and functions from other classes.
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from streamlit.components.v1 import html
import pandas as pd

# Function to create a card (black purple based theme). You pass the icon for the card, title and the description.
def create_feature_card(icon, title, description):
   return f'''
       <div class="feature-card" style="
           background: linear-gradient(145deg, rgba(32, 32, 40, 0.9), rgba(23, 23, 30, 0.9));
           border-radius: 20px;
           padding: 1.5rem;
           border: 1px solid rgba(147, 51, 234, 0.2);
           margin-bottom: 0.9rem;
           display: block;  /* This Ensures block-level behavior */
           box-shadow: 0 4px 20px rgba(147, 51, 234, 0.1);
           transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
           position: relative;
           overflow: hidden;
           backdrop-filter: blur(10px);
       " onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 8px 30px rgba(147, 51, 234, 0.2)'"
          onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 20px rgba(147, 51, 234, 0.1)'">
           <div class="icon-pulse" style="
               font-size: 2.5rem;
               margin-bottom: 0.8rem;
               animation: pulse 2s infinite;
           ">{icon}</div>
           <h3 style="
               color: #a855f7;
               font-size: 1.4rem;
               margin-bottom: 0.7rem;
               font-weight: 600;
               background: linear-gradient(90deg, #a855f7, #d946ef);
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
           ">
               {title}
           </h3>
           <p style="
               color: #94a3b8;
               line-height: 1.6;
               font-size: 1.1rem;
           ">
               {description}
           </p>
           <div class="card-glow"></div>
       </div>
   '''


# Creating stats card which ttakes label, value and change as parameters.
def create_stat_card(label, value, change):
    return f'''
        <div class="stat-card" style="
            background: linear-gradient(145deg, rgba(32, 32, 40, 0.9), rgba(23, 23, 30, 0.9));
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(147, 51, 234, 0.2);
            box-shadow: 0 4px 20px rgba(147, 51, 234, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
        " onmouseover="this.style.transform='scale(1.02)'"
           onmouseout="this.style.transform='scale(1)'">
            <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem;">{label}</div>
            <div style="
                font-size: 1.8rem;
                font-weight: 700;
                background: linear-gradient(90deg, #a855f7, #d946ef);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">{value}</div>
            <div style="font-size: 0.9rem; color: #22c55e;">↑ {change}</div>
        </div>
    '''
# Main welcome page function.
def welcome_page():

    st.markdown("""
        <style>
        /* Optimize image loading */
        img {
            loading: lazy;
            will-change: transform;  /* Optimize animation performance */
        }
        
        /* Preload gradients */
        .stApp {
            background-image: linear-gradient(135deg, #0a0a0f 0%, #17171d 100%);
            contain: content;  /* Improve paint performance */
        }
        
        /* Optimize animations */
        @keyframes float {
            from { transform: translateY(0); }
            to { transform: translateY(-10px); }
        }
        
        /* Use hardware acceleration for animations */
        .animated-element {
            transform: translateZ(0);
            backface-visibility: hidden;
            perspective: 1000px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        /* Use CSS transitions instead of JS for hover effects */
        .modern-button {
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                        box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .modern-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(147, 51, 234, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Basic styles with animations (black-purple theme)
    st.markdown("""
        <style>
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #17171d 100%);
            background-size: 200% 200%;
            animation: gradient 15s ease infinite;
        }
        
        .hero-section {
            background: linear-gradient(145deg, rgba(32, 32, 40, 0.9), rgba(23, 23, 30, 0.9));
            border-radius: 32px;
            padding: 4rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid rgba(147, 51, 234, 0.2);
            box-shadow: 0 8px 32px rgba(147, 51, 234, 0.1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(147, 51, 234, 0.1) 0%, transparent 60%);
            animation: rotate 20s linear infinite;
        }
        
        .modern-button {
            background: linear-gradient(90deg, #a855f7, #d946ef);
            color: white;
            padding: 0.9rem 2rem;
            border-radius: 16px;
            border: none;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: inline-block;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(147, 51, 234, 0.2);
        }
        
        .modern-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(147, 51, 234, 0.4);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin: 1.5rem 0;
        }
        
        .card-glow {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at var(--mouse-x) var(--mouse-y), 
                                    rgba(147, 51, 234, 0.1) 0%, 
                                    transparent 60%);
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
        }
        
        .feature-card:hover .card-glow {
            opacity: 1;
        }
        
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(23, 23, 30, 0.9);
        }
        
        ::-webkit-scrollbar-thumb {
            background: #a855f7;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #d946ef;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #a855f7, #d946ef) !important;
            color: white !important;
            border: none !important;
            padding: 0.9rem 2rem !important;
            border-radius: 16px !important;
            font-weight: 600 !important;
            letter-spacing: 1px !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 20px rgba(147, 51, 234, 0.2) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 30px rgba(147, 51, 234, 0.4) !important;
        }
        </style>
        
        <script>
        document.addEventListener('mousemove', function(e) {
            document.querySelectorAll('.feature-card').forEach(card => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', x + 'px');
                card.style.setProperty('--mouse-y', y + 'px');
            });
        });
        </script>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown('''
        <div class="hero-section">
            <h1 style="
                font-size: 4rem;
                font-weight: 800;
                margin-bottom: 1.5rem;
                background: linear-gradient(90deg, #a855f7, #d946ef);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: float 6s ease-in-out infinite;
            ">
                Welcome to Finch
            </h1>
            <p style="
                font-size: 1.4rem;
                color: rgba(255, 255, 255, 0.9);
                margin-bottom: 2.5rem;
                line-height: 1.6;
            ">
                Elevate Your Trading Experience with AI-Powered Insights
            </p>
        </div>
    ''', unsafe_allow_html=True)

    # Login/Register Buttons
    login_col, register_col = st.columns(2)

   # Updating the current page based on the user's behaviour.
    with login_col:
        if st.button("🔐 Login", key="login_button", use_container_width=True, type="primary"):
            st.session_state.current_page = 'login'
            st.rerun()

    with register_col:
        if st.button("✨ Register", key="register_button", use_container_width=True):
            st.session_state.current_page = 'register'
            st.rerun()


    # Main Content Layout
    col1, col2 = st.columns([5, 7])

    with col1:
        # Feature Cards. Calling the feature card function below.
        features_container = st.container()
        
        features_container.markdown(
            create_feature_card(
                "🚀",
                "Smart Trading",
                "AI-powered insights and real-time market analysis to optimize your trades"
            ),
            unsafe_allow_html=True
        )
        
        features_container.markdown(
            create_feature_card(
                "📊",
                "Advanced Analytics",
                "Professional-grade tools and detailed market analysis at your fingertips"
            ),
            unsafe_allow_html=True
        )
        
        features_container.markdown(
            create_feature_card(
                "🛡️",
                "Enterprise Security",
                "Bank-grade encryption and advanced security protocols to protect your assets"
            ),
            unsafe_allow_html=True
        )

   # Using streamlit components v1 html lib to load the html code in streamlit properly. This library handles code well in certain situation.
    with col2:
        st.components.v1.html(
            """
            <div style="
                display: flex;
                flex-direction: column;
                height: 650px;
            ">
                <!-- Top Card -->
                <div style="
                    background: linear-gradient(145deg, rgba(17, 17, 25, 0.95), rgba(24, 24, 32, 0.95));
                    border-radius: 24px;
                    padding: 2.5rem;
                    border: 1px solid rgba(147, 51, 234, 0.2);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    margin-bottom: 1rem;
                ">
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 2.5rem;
                    ">
                        <div style="
                            font-size: 1.5rem;
                            font-weight: 600;
                            color: #a855f7;
                        ">Market Pulse</div>
                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 0.5rem;
                            color: #a855f7;
                            font-size: 0.9rem;
                        ">
                            ✨ Live
                        </div>
                    </div>

                    <div style="
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 1.5rem;
                        margin-bottom: 2.5rem;
                    ">
                        <div style="
                            background: rgba(15, 15, 20, 0.6);
                            padding: 2rem;
                            border-radius: 16px;
                        ">
                            <div style="
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                margin-bottom: 1rem;
                            ">
                                <span style="color: #94a3b8;">BTC/USD</span>
                                <span style="color: #22c55e;">↑ +2.4%</span>
                            </div>
                            <div style="
                                font-size: 2rem;
                                font-weight: 600;
                                color: #ffffff;
                                margin-bottom: 0.5rem;
                            ">$48,532</div>
                            <div style="color: #64748b; font-size: 0.9rem;">Updated just now</div>
                        </div>

                        <div style="
                            background: rgba(15, 15, 20, 0.6);
                            padding: 2rem;
                            border-radius: 16px;
                        ">
                            <div style="
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                margin-bottom: 1rem;
                            ">
                                <span style="color: #94a3b8;">24h Volume</span>
                                <span style="color: #a855f7;">$</span>
                            </div>
                            <div style="
                                font-size: 2rem;
                                font-weight: 600;
                                color: #ffffff;
                                margin-bottom: 0.5rem;
                            ">$1.2B</div>
                            <div style="color: #64748b; font-size: 0.9rem;">Across all pairs</div>
                        </div>
                    </div>

                    <div style="
                        display: grid;
                        grid-template-columns: repeat(3, 1fr);
                        gap: 1rem;
                    ">
                        <div style="
                            background: rgba(15, 15, 20, 0.6);
                            padding: 1.75rem;
                            border-radius: 16px;
                            text-align: center;
                        ">
                            <div style="font-size: 1.5rem; font-weight: 600; color: #ffffff; margin-bottom: 0.5rem;">12.4K</div>
                            <div style="color: #64748b; font-size: 0.9rem;">Active Traders</div>
                        </div>

                        <div style="
                            background: rgba(15, 15, 20, 0.6);
                            padding: 1.75rem;
                            border-radius: 16px;
                            text-align: center;
                        ">
                            <div style="font-size: 1.5rem; font-weight: 600; color: #ffffff; margin-bottom: 0.5rem;">5.2K</div>
                            <div style="color: #64748b; font-size: 0.9rem;">Open Orders</div>
                        </div>

                        <div style="
                            background: rgba(15, 15, 20, 0.6);
                            padding: 1.75rem;
                            border-radius: 16px;
                            text-align: center;
                        ">
                            <div style="font-size: 1.5rem; font-weight: 600; color: #ffffff; margin-bottom: 0.5rem;">892</div>
                            <div style="color: #64748b; font-size: 0.9rem;">New Users</div>
                        </div>
                    </div>
                </div>
            """,
            height=500
        )

        # Stats Section using columns
        stat1, stat2, stat3 = st.columns(3)
        
        with stat1:
            st.markdown(create_stat_card("24h Volume", "$18.5M", "12.3%"), unsafe_allow_html=True)
            
        with stat2:
            st.markdown(create_stat_card("Market Cap", "$245.8M", "8.7%"), unsafe_allow_html=True)
            
        with stat3:
            st.markdown(create_stat_card("Active Traders", "12.4K", "5.2%"), unsafe_allow_html=True)

    # Why Choose Finch Section
    st.markdown('''
        <div style="
            background: linear-gradient(145deg, rgba(32, 32, 40, 0.9), rgba(23, 23, 30, 0.9));
            border-radius: 24px;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid rgba(147, 51, 234, 0.2);
            box-shadow: 0 8px 32px rgba(147, 51, 234, 0.1);
        ">
            <h2 style="
                color: #f8fafc;
                font-size: 2.5rem;
                text-align: center;
                margin-bottom: 2rem;
                background: linear-gradient(90deg, #a855f7, #d946ef);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">
                Why Choose Finch?
            </h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
    ''', unsafe_allow_html=True)

   # Columns with few information about Finch.
    col1, col2, col3, col4 = st.columns(4)
   
    with col1:
        st.markdown(create_feature_card("💡", "AI-Powered", 
                   "Advanced algorithms for smarter trading decisions"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_feature_card("⚡", "Real-Time", 
                   "Instant market updates and notifications"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_feature_card("🎯", "Precision", 
                   "Accurate analysis and predictions"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_feature_card("🔒", "Secure", 
                   "Enterprise-grade security protocols"), unsafe_allow_html=True)
