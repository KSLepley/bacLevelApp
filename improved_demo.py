"""
Improved Interactive BAC Demo
Shows realistic BAC progression and explains alcohol absorption
"""

import time
import threading
from datetime import datetime, timedelta
from real_time_monitor import RealTimeBACMonitor
from visualization import BACVisualizer

def improved_demo():
    """Run an improved demonstration of the BAC monitoring system"""
    print("🍺 Improved BAC Monitoring System Demo")
    print("=" * 60)
    print("\nThis demo shows realistic BAC progression over time.")
    print("Note: Alcohol takes 30-60 minutes to reach peak BAC levels.")
    print("=" * 60)
    
    # Get user profile
    print("\nPlease enter your profile:")
    weight = float(input("Weight (lbs): "))
    gender = input("Gender (male/female): ").lower()
    
    # Initialize monitor
    monitor = RealTimeBACMonitor(weight, gender)
    visualizer = BACVisualizer()
    
    print(f"\nBAC Monitor initialized for {gender} weighing {weight} lbs")
    print("\nCommands:")
    print("  'add <drink>' - Add a drink (beer/wine/liquor/cocktail)")
    print("  'status' - Show current status")
    print("  'alert' - Check current alert status")
    print("  'chart' - Show real-time chart")
    print("  'gauge' - Show BAC gauge")
    print("  'time <minutes>' - Simulate time passing (e.g., 'time 30')")
    print("  'cooldown <seconds>' - Set alert cooldown (e.g., 'cooldown 60')")
    print("  'reset' - Reset session")
    print("  'quit' - Exit program")
    
    # Start monitoring in background
    monitor.start_monitoring()
    
    # Background thread to show BAC progression (less frequent)
    def show_bac_progression():
        """Show BAC progression over time"""
        while monitor.is_monitoring:
            time.sleep(30)  # Update every 30 seconds (less frequent)
            if monitor.drinks:
                status = monitor.get_current_status()
                if status['bac'] > 0.001:  # Only show if BAC is detectable
                    print(f"\n[Auto-update] BAC: {status['bac']:.3f} - {status['effects']['level']}")
    
    # Start background thread
    progression_thread = threading.Thread(target=show_bac_progression, daemon=True)
    progression_thread.start()
    
    try:
        while True:
            command = input("\n> ").strip().lower()
            
            if command == 'quit':
                break
            elif command.startswith('add '):
                drink_type = command.split()[1]
                if drink_type in ['beer', 'wine', 'liquor', 'cocktail']:
                    monitor.add_drink(drink_type)
                    print(f"Added {drink_type}")
                    
                    # Show immediate status
                    status = monitor.get_current_status()
                    print(f"Immediate BAC: {status['bac']:.3f}")
                    print(f"Note: BAC will rise over the next 30-60 minutes as alcohol is absorbed.")
                    
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
                
                if monitor.drinks:
                    print(f"\nDrinks consumed: {len(monitor.drinks)}")
                    if monitor.first_drink_time:
                        elapsed = (datetime.now() - monitor.first_drink_time).total_seconds() / 60
                        print(f"Time since first drink: {elapsed:.1f} minutes")
            
            elif command == 'alert':
                monitor.check_alerts_manually()
            
            elif command.startswith('cooldown '):
                try:
                    seconds = int(command.split()[1])
                    monitor.set_alert_cooldown(seconds)
                except (ValueError, IndexError):
                    print("Usage: cooldown <seconds> (e.g., 'cooldown 60')")
            
            elif command.startswith('time '):
                try:
                    minutes = int(command.split()[1])
                    print(f"Simulating {minutes} minutes passing...")
                    
                    # Manually adjust the first drink time to simulate time passing
                    if monitor.first_drink_time:
                        monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=minutes)
                        monitor._update_bac()
                        
                        status = monitor.get_current_status()
                        print(f"BAC after {minutes} minutes: {status['bac']:.3f}")
                        print(f"Status: {status['effects']['level']}")
                    else:
                        print("No drinks added yet.")
                        
                except (ValueError, IndexError):
                    print("Usage: time <minutes> (e.g., 'time 30')")
            
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

def quick_demo():
    """Quick demonstration with automatic time progression"""
    print("🍺 Quick BAC Demo (Automatic)")
    print("=" * 50)
    
    monitor = RealTimeBACMonitor(150, 'female')
    visualizer = BACVisualizer()
    
    monitor.start_monitoring()
    
    print("Adding 1 beer...")
    monitor.add_drink('beer')
    status = monitor.get_current_status()
    print(f"Immediate BAC: {status['bac']:.3f}")
    
    print("\nSimulating 30 minutes passing...")
    if monitor.first_drink_time:
        monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=30)
        monitor._update_bac()
    
    status = monitor.get_current_status()
    print(f"BAC after 30 minutes: {status['bac']:.3f}")
    print(f"Status: {status['effects']['level']}")
    
    print("\nAdding 1 shot...")
    monitor.add_drink('liquor')
    status = monitor.get_current_status()
    print(f"Immediate BAC: {status['bac']:.3f}")
    
    print("\nSimulating 1 hour total...")
    if monitor.first_drink_time:
        monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=30)
        monitor._update_bac()
    
    status = monitor.get_current_status()
    print(f"Final BAC: {status['bac']:.3f}")
    print(f"Status: {status['effects']['level']}")
    print(f"Recommendation: {status['effects']['recommendation']}")
    
    monitor.stop_monitoring()

if __name__ == "__main__":
    print("Choose demo type:")
    print("1. Interactive demo (manual control)")
    print("2. Quick demo (automatic)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        improved_demo()
    elif choice == "2":
        quick_demo()
    else:
        print("Invalid choice") 