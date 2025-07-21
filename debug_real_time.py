"""
Debug real-time monitor BAC calculation
"""

import time
from datetime import datetime
from real_time_monitor import RealTimeBACMonitor

def debug_real_time_bac():
    """Debug the real-time BAC calculation"""
    print("🔍 Debugging Real-time BAC Calculation")
    print("=" * 50)
    
    # Create monitor
    monitor = RealTimeBACMonitor(133, 'female')
    
    print("Initial state:")
    print(f"  Drinks: {len(monitor.drinks)}")
    print(f"  First drink time: {monitor.first_drink_time}")
    print(f"  Current BAC: {monitor.current_bac}")
    
    # Add a drink
    print(f"\nAdding 1 beer...")
    monitor.add_drink('beer')
    
    print(f"After adding drink:")
    print(f"  Drinks: {len(monitor.drinks)}")
    print(f"  First drink time: {monitor.first_drink_time}")
    print(f"  Last drink time: {monitor.last_drink_time}")
    print(f"  Current BAC: {monitor.current_bac}")
    
    # Check time calculation
    if monitor.first_drink_time:
        hours_since_first = (datetime.now() - monitor.first_drink_time).total_seconds() / 3600
        print(f"  Hours since first drink: {hours_since_first:.4f}")
    
    # Test direct BAC calculation
    print(f"\nTesting direct BAC calculation:")
    calculated_bac = monitor.bac_calculator.calculate_bac_widmark(
        monitor.weight_lbs, 
        monitor.gender, 
        monitor.drinks, 
        hours_since_first if monitor.first_drink_time else 0
    )
    print(f"  Direct calculation result: {calculated_bac:.6f}")
    
    # Add another drink
    print(f"\nAdding 1 shot...")
    monitor.add_drink('liquor')
    
    print(f"After adding second drink:")
    print(f"  Drinks: {len(monitor.drinks)}")
    print(f"  Current BAC: {monitor.current_bac}")
    
    # Check time calculation again
    if monitor.first_drink_time:
        hours_since_first = (datetime.now() - monitor.first_drink_time).total_seconds() / 3600
        print(f"  Hours since first drink: {hours_since_first:.4f}")
    
    # Test direct BAC calculation again
    calculated_bac = monitor.bac_calculator.calculate_bac_widmark(
        monitor.weight_lbs, 
        monitor.gender, 
        monitor.drinks, 
        hours_since_first if monitor.first_drink_time else 0
    )
    print(f"  Direct calculation result: {calculated_bac:.6f}")
    
    # Test with longer time
    print(f"\nTesting with 30 minutes elapsed:")
    calculated_bac_30min = monitor.bac_calculator.calculate_bac_widmark(
        monitor.weight_lbs, 
        monitor.gender, 
        monitor.drinks, 
        0.5  # 30 minutes
    )
    print(f"  BAC after 30 minutes: {calculated_bac_30min:.6f}")
    
    # Test with 1 hour elapsed
    print(f"\nTesting with 1 hour elapsed:")
    calculated_bac_1hr = monitor.bac_calculator.calculate_bac_widmark(
        monitor.weight_lbs, 
        monitor.gender, 
        monitor.drinks, 
        1.0  # 1 hour
    )
    print(f"  BAC after 1 hour: {calculated_bac_1hr:.6f}")

if __name__ == "__main__":
    debug_real_time_bac() 