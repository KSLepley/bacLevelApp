"""
Manual Time Simulation Demo
Shows how to manually add theoretical time to the BAC monitoring system
"""

import time
from datetime import datetime, timedelta
from real_time_monitor import RealTimeBACMonitor

def manual_time_demo():
    """Demonstrate manual time simulation"""
    print("🕐 Manual Time Simulation Demo")
    print("=" * 50)
    
    # Create monitor
    monitor = RealTimeBACMonitor(150, 'female')
    monitor.start_monitoring()
    
    print("Adding 1 beer...")
    monitor.add_drink('beer')
    
    # Show immediate BAC
    status = monitor.get_current_status()
    print(f"Immediate BAC: {status['bac']:.3f}")
    
    # Method 1: Simulate 30 minutes passing
    print("\n--- Simulating 30 minutes passing ---")
    if monitor.first_drink_time:
        # Move the first drink time back by 30 minutes
        monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=30)
        monitor._update_bac()  # Recalculate BAC
    
    status = monitor.get_current_status()
    print(f"BAC after 30 minutes: {status['bac']:.3f}")
    print(f"Status: {status['effects']['level']}")
    
    # Method 2: Simulate 1 hour total
    print("\n--- Simulating 1 hour total ---")
    if monitor.first_drink_time:
        # Move the first drink time back by another 30 minutes (1 hour total)
        monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=30)
        monitor._update_bac()
    
    status = monitor.get_current_status()
    print(f"BAC after 1 hour: {status['bac']:.3f}")
    print(f"Status: {status['effects']['level']}")
    
    # Add another drink
    print("\n--- Adding another drink ---")
    monitor.add_drink('liquor')
    
    status = monitor.get_current_status()
    print(f"BAC after adding liquor: {status['bac']:.3f}")
    print(f"Status: {status['effects']['level']}")
    
    # Method 3: Simulate 2 hours total
    print("\n--- Simulating 2 hours total ---")
    if monitor.first_drink_time:
        # Move the first drink time back by another 60 minutes (2 hours total)
        monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=60)
        monitor._update_bac()
    
    status = monitor.get_current_status()
    print(f"BAC after 2 hours: {status['bac']:.3f}")
    print(f"Status: {status['effects']['level']}")
    print(f"Time to sober: {status['sober_time_hours']:.1f} hours")
    
    monitor.stop_monitoring()

def time_simulation_examples():
    """Show different time simulation examples"""
    print("\n" + "=" * 50)
    print("TIME SIMULATION EXAMPLES")
    print("=" * 50)
    
    monitor = RealTimeBACMonitor(160, 'male')
    monitor.start_monitoring()
    
    # Add drinks
    monitor.add_drink('beer')
    monitor.add_drink('beer')
    monitor.add_drink('wine')
    
    print("Added 3 drinks (2 beers + 1 wine)")
    
    # Test different time scenarios
    time_scenarios = [
        (15, "15 minutes"),
        (30, "30 minutes (peak absorption)"),
        (60, "1 hour"),
        (90, "1.5 hours"),
        (120, "2 hours"),
        (180, "3 hours"),
        (240, "4 hours")
    ]
    
    for minutes, description in time_scenarios:
        if monitor.first_drink_time:
            # Reset to original time
            original_time = monitor.first_drink_time + timedelta(minutes=sum([m for m, _ in time_scenarios[:time_scenarios.index((minutes, description))]]))
            monitor.first_drink_time = original_time - timedelta(minutes=minutes)
            monitor._update_bac()
            
            status = monitor.get_current_status()
            print(f"{description:20} | BAC: {status['bac']:.3f} | {status['effects']['level']}")
    
    monitor.stop_monitoring()

if __name__ == "__main__":
    manual_time_demo()
    time_simulation_examples() 