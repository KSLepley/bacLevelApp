"""
Streamlit Web Application for BAC Monitoring
Modern web interface for real-time BAC tracking
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import threading
from real_time_monitor import RealTimeBACMonitor
from visualization import BACVisualizer

# Page configuration
st.set_page_config(
    page_title="BAC Monitor",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .status-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .danger-card {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'monitor' not in st.session_state:
    st.session_state.monitor = None
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = BACVisualizer()
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

def initialize_monitor():
    """Initialize the BAC monitor with user profile"""
    if st.session_state.monitor is None:
        weight = st.session_state.get('weight', 150)
        gender = st.session_state.get('gender', 'male')
        st.session_state.monitor = RealTimeBACMonitor(weight, gender)

def start_monitoring():
    """Start the monitoring process"""
    if st.session_state.monitor and not st.session_state.monitoring:
        st.session_state.monitor.start_monitoring()
        st.session_state.monitoring = True
        st.success("Monitoring started!")

def stop_monitoring():
    """Stop the monitoring process"""
    if st.session_state.monitor and st.session_state.monitoring:
        st.session_state.monitor.stop_monitoring()
        st.session_state.monitoring = False
        st.success("Monitoring stopped!")

def reset_session():
    """Reset the current session"""
    if st.session_state.monitor:
        st.session_state.monitor.reset_session()
        st.success("Session reset!")

def add_drink():
    """Add a drink to the tracking system"""
    if st.session_state.monitor:
        drink_type = st.session_state.drink_type
        volume = st.session_state.drink_volume
        alcohol_percent = st.session_state.drink_alcohol_percent
        
        st.session_state.monitor.add_drink(drink_type, volume, alcohol_percent)
        st.success(f"Added {drink_type}!")

# Main header
st.markdown('<h1 class="main-header">🍺 Real-time BAC Monitor</h1>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.header("⚙️ Setup & Controls")
    
    # User profile
    st.subheader("👤 User Profile")
    weight = st.number_input("Weight (lbs)", min_value=80, max_value=300, value=150, key="weight")
    gender = st.selectbox("Gender", ["male", "female"], key="gender")
    
    # Initialize monitor when profile changes
    if st.session_state.monitor is None or (weight != st.session_state.get('weight', 150) or 
                                          gender != st.session_state.get('gender', 'male')):
        # No need to assign to st.session_state.weight or st.session_state.gender
        initialize_monitor()
    
    st.markdown("---")
    
    # Monitoring controls
    st.subheader("🎛️ Monitoring Controls")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Start", on_click=start_monitoring, disabled=st.session_state.monitoring):
            pass
    
    with col2:
        if st.button("⏹️ Stop", on_click=stop_monitoring, disabled=not st.session_state.monitoring):
            pass
    
    if st.button("🔄 Reset Session", on_click=reset_session):
        pass
    
    st.markdown("---")
    
    # Add drink section
    st.subheader("🍺 Add Drink")
    
    drink_type = st.selectbox(
        "Drink Type",
        ["beer", "wine", "liquor", "cocktail"],
        key="drink_type"
    )
    
    # Default values based on drink type
    defaults = {
        "beer": (12.0, 5.0),
        "wine": (5.0, 12.0),
        "liquor": (1.5, 40.0),
        "cocktail": (8.0, 15.0)
    }
    
    default_volume, default_alcohol = defaults[drink_type]
    
    volume = st.number_input(
        "Volume (oz)",
        min_value=0.5,
        max_value=32.0,
        value=default_volume,
        step=0.5,
        key="drink_volume"
    )
    
    alcohol_percent = st.number_input(
        "Alcohol %",
        min_value=1.0,
        max_value=100.0,
        value=default_alcohol,
        step=0.5,
        key="drink_alcohol_percent"
    )
    
    if st.button("➕ Add Drink", on_click=add_drink):
        pass

# Main content area
if st.session_state.monitor:
    # Get current status
    status = st.session_state.monitor.get_current_status()
    
    # Top row - Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            "Current BAC",
            f"{status['bac']:.3f}",
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            "Status",
            status['effects']['level'],
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            "Time to Sober",
            f"{status['sober_time_hours']:.1f}h",
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            "Drinks Consumed",
            status['drinks_count'],
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # BAC Gauge
    st.subheader("📊 BAC Gauge")
    gauge_fig = st.session_state.visualizer.create_bac_gauge(status['bac'], figsize=(8, 6))
    st.pyplot(gauge_fig)
    
    # Main content columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Real-time Monitoring")
        
        # Get recent data
        recent_data = st.session_state.monitor.get_recent_data(minutes=30)
        
        if recent_data and len(recent_data) > 1:
            # Create interactive chart
            df = pd.DataFrame(recent_data)
            df['time'] = pd.to_datetime(df['timestamp'])
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('BAC Level', 'Sensor Data'),
                vertical_spacing=0.1,
                row_heights=[0.7, 0.3]
            )
            
            # BAC trace
            fig.add_trace(
                go.Scatter(
                    x=df['time'], 
                    y=df['bac'], 
                    mode='lines', 
                    name='BAC',
                    line=dict(color='blue', width=3)
                ),
                row=1, col=1
            )
            
            # Add threshold lines
            fig.add_hline(y=0.08, line_dash="dash", line_color="red", 
                         annotation_text="Legal Limit (0.08)", row=1, col=1)
            fig.add_hline(y=0.05, line_dash="dash", line_color="orange", 
                         annotation_text="Warning (0.05)", row=1, col=1)
            
            # Sensor data
            fig.add_trace(
                go.Scatter(
                    x=df['time'], 
                    y=df['heart_rate'], 
                    mode='lines', 
                    name='Heart Rate',
                    line=dict(color='red', width=2)
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['time'], 
                    y=df['skin_conductance'], 
                    mode='lines', 
                    name='Skin Conductance',
                    line=dict(color='green', width=2),
                    yaxis='y3'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                height=500,
                showlegend=True,
                title_text="Real-time BAC and Sensor Monitoring"
            )
            
            # Update y-axes
            fig.update_yaxes(title_text="BAC Level", row=1, col=1)
            fig.update_yaxes(title_text="Heart Rate (BPM)", row=2, col=1)
            fig.update_yaxes(title_text="Skin Conductance (μS)", row=2, col=1, secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No monitoring data available yet. Start monitoring to see real-time charts.")
    
    with col2:
        st.subheader("📱 Sensor Data")
        
        sensors = status['sensors']
        
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Heart Rate", f"{sensors['heart_rate']:.0f} BPM")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Skin Conductance", f"{sensors['skin_conductance']:.1f} μS")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Temperature", f"{sensors['temperature']:.1f}°F")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Monitoring status
        st.subheader("🔍 Monitoring Status")
        if st.session_state.monitoring:
            st.success("✅ Active")
        else:
            st.error("❌ Inactive")
    
    # Alerts and recommendations
    st.subheader("⚠️ Alerts & Recommendations")
    
    effects = status['effects']
    bac_level = status['bac']
    
    if bac_level >= 0.15:
        st.markdown('<div class="danger-card">', unsafe_allow_html=True)
        st.error(f"🚨 CRITICAL: BAC {bac_level:.3f} - {effects['recommendation']}")
        st.markdown('</div>', unsafe_allow_html=True)
    elif bac_level >= 0.08:
        st.markdown('<div class="danger-card">', unsafe_allow_html=True)
        st.error(f"⚠️ DANGER: BAC {bac_level:.3f} - {effects['recommendation']}")
        st.markdown('</div>', unsafe_allow_html=True)
    elif bac_level >= 0.05:
        st.markdown('<div class="alert-card">', unsafe_allow_html=True)
        st.warning(f"⚠️ WARNING: BAC {bac_level:.3f} - {effects['recommendation']}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.info(f"✅ SAFE: BAC {bac_level:.3f} - {effects['effects']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Drink history
    if st.session_state.monitor.drinks:
        st.subheader("🍺 Drink History")
        
        drink_df = pd.DataFrame(st.session_state.monitor.drinks)
        drink_df['time'] = pd.to_datetime(drink_df['timestamp']).dt.strftime('%H:%M:%S')
        drink_df['date'] = pd.to_datetime(drink_df['timestamp']).dt.strftime('%Y-%m-%d')
        
        # Display drink history
        display_df = drink_df[['date', 'time', 'alcohol_percent', 'volume_oz']].copy()
        display_df.columns = ['Date', 'Time', 'Alcohol %', 'Volume (oz)']
        
        st.dataframe(display_df, use_container_width=True)
        
        # Drink statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Drinks", len(drink_df))
        
        with col2:
            total_volume = drink_df['volume_oz'].sum()
            st.metric("Total Volume", f"{total_volume:.1f} oz")
        
        with col3:
            avg_alcohol = drink_df['alcohol_percent'].mean()
            st.metric("Avg Alcohol %", f"{avg_alcohol:.1f}%")

else:
    st.info("Please set up your profile in the sidebar to begin monitoring.")

# Auto-refresh
if st.session_state.monitoring:
    time.sleep(1)
    st.experimental_rerun() 