"""
Main BAC Monitoring Application
Demonstrates the real-time BAC monitoring system
"""

import time
import threading
from datetime import datetime
from real_time_monitor import RealTimeBACMonitor
from visualization import BACVisualizer

def demo_mode():
    """Run a demonstration of the BAC monitoring system"""
    print("🍺 BAC Monitoring System Demo")
    print("=" * 50)
    
    # Get user profile
    print("\nPlease enter your profile:")
    weight = float(input("Weight (lbs): "))
    gender = input("Gender (male/female): ").lower()
    
    # Initialize monitor
    monitor = RealTimeBACMonitor(weight, gender)
    visualizer = BACVisualizer()
    
    print(f"\nBAC Monitor initialized for {gender} weighing {weight} lbs")
    print("\nCommands:")
    print("  'start' - Start monitoring")
    print("  'stop' - Stop monitoring")
    print("  'add <drink>' - Add a drink (beer/wine/liquor/cocktail)")
    print("  'status' - Show current status")
    print("  'chart' - Show real-time chart")
    print("  'gauge' - Show BAC gauge")
    print("  'reset' - Reset session")
    print("  'quit' - Exit program")
    
    # Start monitoring in background
    monitor.start_monitoring()
    
    try:
        while True:
            command = input("\n> ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'start':
                monitor.start_monitoring()
                print("Monitoring started")
            elif command == 'stop':
                monitor.stop_monitoring()
                print("Monitoring stopped")
            elif command.startswith('add '):
                drink_type = command.split()[1]
                if drink_type in ['beer', 'wine', 'liquor', 'cocktail']:
                    monitor.add_drink(drink_type)
                    print(f"Added {drink_type}")
                else:
                    print("Invalid drink type. Use: beer, wine, liquor, or cocktail")
            elif command == 'status':
                status = monitor.get_current_status()
                print(f"\nCurrent BAC: {status['bac']:.3f}")
                print(f"Status: {status['effects']['level']}")
                print(f"Effects: {status['effects']['effects']}")
                print(f"Recommendation: {status['effects']['recommendation']}")
                print(f"Time to sober: {status['sober_time_hours']:.1f} hours")
                print(f"Heart Rate: {status['sensors']['heart_rate']:.0f} BPM")
            elif command == 'chart':
                recent_data = monitor.get_recent_data(minutes=30)
                if recent_data:
                    fig = visualizer.create_real_time_chart(recent_data)
                    fig.show()
                else:
                    print("No data available yet")
            elif command == 'gauge':
                status = monitor.get_current_status()
                fig = visualizer.create_bac_gauge(status['bac'])
                fig.show()
            elif command == 'reset':
                monitor.reset_session()
                print("Session reset")
            else:
                print("Unknown command")
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        monitor.stop_monitoring()

def simulation_mode():
    """Run a simulation with predefined drinking pattern"""
    print("🍺 BAC Monitoring Simulation")
    print("=" * 50)
    
    # Initialize monitor for simulation
    monitor = RealTimeBACMonitor(160, 'male')  # 160 lb male
    visualizer = BACVisualizer()
    
    print("Starting simulation for 160 lb male...")
    monitor.start_monitoring()
    
    # Simulation timeline
    timeline = [
        (0, "Starting simulation"),
        (5, "Adding first beer"),
        (15, "Adding second beer"),
        (45, "Adding wine"),
        (75, "Adding liquor shot"),
        (105, "Monitoring continues..."),
        (135, "Simulation complete")
    ]
    
    drinks = ['beer', 'beer', 'wine', 'liquor']
    drink_index = 0
    
    previous_time = 0
    for time_minutes, message in timeline:
        print(f"\n[{time_minutes:3d} min] {message}")
        
        # Simulate time progression by adjusting the first drink time
        if time_minutes > 0 and monitor.first_drink_time:
            # Move the first drink time back by the time difference since last event
            from datetime import timedelta
            time_diff = time_minutes - previous_time
            monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=time_diff)
            monitor._update_bac()
        
        if drink_index < len(drinks):
            monitor.add_drink(drinks[drink_index])
            drink_index += 1
        
        # Show status
        status = monitor.get_current_status()
        print(f"   BAC: {status['bac']:.3f} - {status['effects']['level']}")
        print(f"   HR: {status['sensors']['heart_rate']:.0f} BPM")
        
        # Wait for next event
        if time_minutes < 135:
            time.sleep(30)  # 30 seconds between events
        
        previous_time = time_minutes
    
    # Show final results
    print("\n" + "=" * 50)
    print("SIMULATION RESULTS")
    print("=" * 50)
    
    final_status = monitor.get_current_status()
    print(f"Final BAC: {final_status['bac']:.3f}")
    print(f"Status: {final_status['effects']['level']}")
    print(f"Time to sober: {final_status['sober_time_hours']:.1f} hours")
    
    # Show charts
    recent_data = monitor.get_recent_data(minutes=60)
    if recent_data:
        print("\nGenerating charts...")
        
        # BAC gauge
        gauge_fig = visualizer.create_bac_gauge(final_status['bac'])
        gauge_fig.savefig('bac_gauge.png', dpi=150, bbox_inches='tight')
        print("Saved: bac_gauge.png")
        
        # Real-time chart
        chart_fig = visualizer.create_real_time_chart(recent_data)
        chart_fig.savefig('bac_chart.png', dpi=150, bbox_inches='tight')
        print("Saved: bac_chart.png")
        
        # Interactive dashboard
        dashboard_fig = visualizer.create_interactive_dashboard(recent_data)
        if dashboard_fig:
            dashboard_fig.write_html('bac_dashboard.html')
            print("Saved: bac_dashboard.html")
    
    monitor.stop_monitoring()

def wearable_demo():
    """Demonstrate wearable device interface"""
    print("⌚ Wearable Device BAC Monitor Demo")
    print("=" * 50)
    
    monitor = RealTimeBACMonitor(150, 'female')
    visualizer = BACVisualizer()
    
    monitor.start_monitoring()
    
    # Simulate drinking session
    print("Starting wearable demo...")
    time.sleep(2)
    
    monitor.add_drink('beer')
    time.sleep(3)
    
    monitor.add_drink('wine')
    time.sleep(3)
    
    # Show wearable display
    status = monitor.get_current_status()
    wearable_fig = visualizer.create_wearable_display(status)
    wearable_fig.savefig('wearable_display.png', dpi=150, bbox_inches='tight', 
                        facecolor='black')
    print("Saved: wearable_display.png")
    
    monitor.stop_monitoring()

def main():
    """Main application entry point"""
    print("🍺 Blood Alcohol Content (BAC) Monitoring System")
    print("=" * 60)
    print("\nChoose a mode:")
    print("1. Interactive Demo - Command-line interface")
    print("2. Simulation - Automated drinking pattern")
    print("3. Wearable Demo - Compact display simulation")
    print("4. Web Interface - Streamlit dashboard")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        demo_mode()
    elif choice == '2':
        simulation_mode()
    elif choice == '3':
        wearable_demo()
    elif choice == '4':
        print("\nTo run the web interface:")
        print("1. Install Streamlit: pip install streamlit")
        print("2. Run: streamlit run web_app.py")
        print("\nOr run this command:")
        print("streamlit run web_app.py")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main() 