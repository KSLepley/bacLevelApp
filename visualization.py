"""
BAC Visualization Module
Real-time charts and graphs for BAC monitoring on wearable devices
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

class BACVisualizer:
    """Visualization tools for BAC monitoring"""
    
    def __init__(self):
        self.colors = {
            'sober': '#00FF00',      # Green
            'mild': '#FFFF00',       # Yellow
            'moderate': '#FFA500',   # Orange
            'high': '#FF0000',       # Red
            'severe': '#8B0000'      # Dark Red
        }
    
    def create_bac_gauge(self, bac_level, figsize=(8, 6)):
        """
        Create a circular gauge showing current BAC level
        Suitable for wearable device displays
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Define gauge parameters
        center = (0.5, 0.5)
        radius = 0.4
        
        # Create gauge background
        gauge = Circle(center, radius, fill=False, color='gray', linewidth=10)
        ax.add_patch(gauge)
        
        # Determine color based on BAC level
        if bac_level < 0.02:
            color = self.colors['sober']
        elif bac_level < 0.05:
            color = self.colors['mild']
        elif bac_level < 0.08:
            color = self.colors['moderate']
        elif bac_level < 0.15:
            color = self.colors['high']
        else:
            color = self.colors['severe']
        
        # Create BAC arc
        angle = min(bac_level * 1000, 180)  # Scale BAC to 0-180 degrees
        arc = plt.matplotlib.patches.Arc(center, 2*radius, 2*radius, 
                                       theta1=180, theta2=180-angle, 
                                       color=color, linewidth=10)
        ax.add_patch(arc)
        
        # Add BAC text
        ax.text(0.5, 0.4, f'{bac_level:.3f}', fontsize=24, ha='center', va='center', fontweight='bold')
        ax.text(0.5, 0.3, 'BAC', fontsize=16, ha='center', va='center')
        
        # Add scale markers
        for i, level in enumerate([0, 0.02, 0.05, 0.08, 0.15]):
            angle = 180 - (level * 1000)
            x = 0.5 + 0.35 * np.cos(np.radians(angle))
            y = 0.5 + 0.35 * np.sin(np.radians(angle))
            ax.text(x, y, f'{level:.2f}', fontsize=10, ha='center', va='center')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        plt.tight_layout()
        return fig
    
    def create_real_time_chart(self, data_history, figsize=(10, 6)):
        """
        Create real-time BAC chart with sensor data
        """
        if not data_history:
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(data_history)
        df['time'] = pd.to_datetime(df['timestamp'])
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
        
        # BAC chart
        ax1.plot(df['time'], df['bac'], 'b-', linewidth=2, label='BAC')
        ax1.axhline(y=0.08, color='r', linestyle='--', alpha=0.7, label='Legal Limit')
        ax1.axhline(y=0.05, color='orange', linestyle='--', alpha=0.7, label='Warning Level')
        ax1.set_ylabel('BAC Level')
        ax1.set_title('Real-time BAC Monitoring')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Sensor data
        ax2.plot(df['time'], df['heart_rate'], 'r-', label='Heart Rate (BPM)')
        ax2_twin = ax2.twinx()
        ax2_twin.plot(df['time'], df['skin_conductance'], 'g-', label='Skin Conductance')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Heart Rate (BPM)', color='r')
        ax2_twin.set_ylabel('Skin Conductance', color='g')
        ax2.legend(loc='upper left')
        ax2_twin.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_interactive_dashboard(self, data_history):
        """
        Create an interactive Plotly dashboard
        """
        if not data_history:
            return None
        
        df = pd.DataFrame(data_history)
        df['time'] = pd.to_datetime(df['timestamp'])
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('BAC Level', 'Heart Rate', 'Skin Conductance'),
            vertical_spacing=0.1
        )
        
        # BAC trace
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['bac'], mode='lines', name='BAC',
                      line=dict(color='blue', width=2)),
            row=1, col=1
        )
        
        # Add BAC threshold lines
        fig.add_hline(y=0.08, line_dash="dash", line_color="red", 
                     annotation_text="Legal Limit", row=1, col=1)
        fig.add_hline(y=0.05, line_dash="dash", line_color="orange", 
                     annotation_text="Warning", row=1, col=1)
        
        # Heart rate trace
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['heart_rate'], mode='lines', name='Heart Rate',
                      line=dict(color='red', width=2)),
            row=2, col=1
        )
        
        # Skin conductance trace
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['skin_conductance'], mode='lines', name='Skin Conductance',
                      line=dict(color='green', width=2)),
            row=3, col=1
        )
        
        fig.update_layout(height=800, title_text="Real-time BAC Monitoring Dashboard")
        return fig
    
    def create_wearable_display(self, current_status, figsize=(4, 6)):
        """
        Create a compact display suitable for wearable devices
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Background
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        
        # BAC level with color coding
        bac = current_status['bac']
        effects = current_status['effects']
        
        if bac < 0.02:
            color = self.colors['sober']
        elif bac < 0.05:
            color = self.colors['mild']
        elif bac < 0.08:
            color = self.colors['moderate']
        elif bac < 0.15:
            color = self.colors['high']
        else:
            color = self.colors['severe']
        
        # Main BAC display
        ax.text(0.5, 0.8, f'{bac:.3f}', fontsize=36, ha='center', va='center', 
               color=color, fontweight='bold')
        ax.text(0.5, 0.7, 'BAC', fontsize=16, ha='center', va='center', color='white')
        
        # Status
        ax.text(0.5, 0.5, effects['level'], fontsize=14, ha='center', va='center', 
               color=color, fontweight='bold')
        
        # Time to sober
        sober_time = current_status['sober_time_hours']
        if sober_time > 0:
            ax.text(0.5, 0.3, f'Sober in: {sober_time:.1f}h', fontsize=12, 
                   ha='center', va='center', color='white')
        
        # Sensor data (compact)
        sensors = current_status['sensors']
        ax.text(0.5, 0.1, f'HR: {sensors["heart_rate"]:.0f}', fontsize=10, 
               ha='center', va='center', color='lightgray')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        plt.tight_layout()
        return fig
    
    def create_streamlit_app(self, monitor):
        """
        Create a Streamlit web interface for the BAC monitor
        """
        st.set_page_config(page_title="BAC Monitor", layout="wide")
        
        st.title("🍺 Real-time BAC Monitor")
        st.markdown("---")
        
        # Sidebar controls
        st.sidebar.header("Controls")
        
        if st.sidebar.button("Start Monitoring"):
            monitor.start_monitoring()
        
        if st.sidebar.button("Stop Monitoring"):
            monitor.stop_monitoring()
        
        if st.sidebar.button("Reset Session"):
            monitor.reset_session()
        
        # Add drink section
        st.sidebar.header("Add Drink")
        drink_type = st.sidebar.selectbox("Drink Type", ["beer", "wine", "liquor", "cocktail"])
        volume = st.sidebar.number_input("Volume (oz)", min_value=1.0, max_value=32.0, value=12.0)
        alcohol_percent = st.sidebar.number_input("Alcohol %", min_value=1.0, max_value=100.0, value=5.0)
        
        if st.sidebar.button("Add Drink"):
            monitor.add_drink(drink_type, volume, alcohol_percent)
        
        # Main display
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Real-time BAC Chart")
            recent_data = monitor.get_recent_data(minutes=30)
            if recent_data:
                chart_fig = self.create_real_time_chart(recent_data)
                if chart_fig:
                    st.pyplot(chart_fig)
            else:
                st.info("No data available. Start monitoring to see real-time charts.")
        
        with col2:
            st.subheader("Current Status")
            status = monitor.get_current_status()
            
            # BAC gauge
            gauge_fig = self.create_bac_gauge(status['bac'], figsize=(6, 4))
            st.pyplot(gauge_fig)
            
            # Status info
            st.metric("BAC Level", f"{status['bac']:.3f}")
            st.metric("Status", status['effects']['level'])
            st.metric("Time to Sober", f"{status['sober_time_hours']:.1f} hours")
            
            # Sensor data
            st.subheader("Sensor Data")
            sensors = status['sensors']
            st.metric("Heart Rate", f"{sensors['heart_rate']:.0f} BPM")
            st.metric("Skin Conductance", f"{sensors['skin_conductance']:.1f} μS")
            st.metric("Temperature", f"{sensors['temperature']:.1f}°F")
        
        # Alerts section
        st.subheader("Alerts & Recommendations")
        effects = status['effects']
        st.info(f"**{effects['level']}**: {effects['effects']}")
        st.warning(f"**Recommendation**: {effects['recommendation']}")
        
        # Drink history
        if monitor.drinks:
            st.subheader("Drink History")
            drink_df = pd.DataFrame(monitor.drinks)
            drink_df['time'] = pd.to_datetime(drink_df['timestamp']).dt.strftime('%H:%M:%S')
            st.dataframe(drink_df[['time', 'alcohol_percent', 'volume_oz']]) 