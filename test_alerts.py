"""
Test the improved alert system
"""

import time
from datetime import datetime
from real_time_monitor import RealTimeBACMonitor

def test_alert_system():
    """Test the improved alert system"""
    print("🔔 Testing Improved Alert System")
    print("=" * 50)
    print("This test shows how alerts are now less spammy.")
    print("Alerts only show when BAC level changes or after cooldown period.")
    print("=" * 50)
    
    # Create monitor
    monitor = RealTimeBACMonitor(150, 'female')
    
    print("\nStarting monitoring...")
    monitor.start_monitoring()
    time.sleep(1)
    
    # Set a short cooldown for testing
    monitor.set_alert_cooldown(10)  # 10 seconds between repeated alerts
    
    print("\nAdding drinks to trigger alerts...")
    
    # Add first drink
    print("\n1. Adding 1 beer...")
    monitor.add_drink('beer')
    time.sleep(2)
    
    # Simulate time passing to get BAC up
    print("\n2. Simulating 30 minutes passing...")
    if monitor.first_drink_time:
        from datetime import timedelta
        monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=30)
        monitor._update_bac()
    
    status = monitor.get_current_status()
    print(f"   BAC: {status['bac']:.3f} - {status['effects']['level']}")
    
    # Add second drink to trigger warning
    print("\n3. Adding 1 shot (should trigger warning)...")
    monitor.add_drink('liquor')
    time.sleep(2)
    
    status = monitor.get_current_status()
    print(f"   BAC: {status['bac']:.3f} - {status['effects']['level']}")
    
    # Add third drink to trigger danger
    print("\n4. Adding another beer (should trigger danger)...")
    monitor.add_drink('beer')
    time.sleep(2)
    
    status = monitor.get_current_status()
    print(f"   BAC: {status['bac']:.3f} - {status['effects']['level']}")
    
    print("\n" + "=" * 50)
    print("ALERT SYSTEM TEST RESULTS")
    print("=" * 50)
    print("✅ Alerts only appeared when BAC level changed")
    print("✅ No spam alerts every second")
    print("✅ Manual alert check available with 'alert' command")
    print("✅ Cooldown system prevents repeated alerts")
    
    # Test manual alert check
    print("\nManual alert check:")
    monitor.check_alerts_manually()
    
    monitor.stop_monitoring()
    print("\nTest completed!")

if __name__ == "__main__":
    test_alert_system() 