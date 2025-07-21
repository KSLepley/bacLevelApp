"""
Demonstration of realistic BAC calculations
"""

import time
from datetime import datetime
from real_time_monitor import RealTimeBACMonitor
from visualization import BACVisualizer

def demo_realistic_bac():
    """Demonstrate realistic BAC monitoring"""
    print("🍺 Realistic BAC Monitoring Demonstration")
    print("=" * 60)
    
    # Create monitor for 133 lb female
    monitor = RealTimeBACMonitor(133, 'female')
    visualizer = BACVisualizer()
    
    print("Starting monitoring for 133 lb female...")
    monitor.start_monitoring()
    time.sleep(1)
    
    # Initial status
    status = monitor.get_current_status()
    print(f"\nInitial status:")
    print(f"  BAC: {status['bac']:.3f}")
    print(f"  Status: {status['effects']['level']}")
    
    # Add first drink
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Adding 1 beer...")
    monitor.add_drink('beer')
    time.sleep(2)
    
    status = monitor.get_current_status()
    print(f"  BAC: {status['bac']:.3f} (immediate)")
    print(f"  Status: {status['effects']['level']}")
    print(f"  Effects: {status['effects']['effects']}")
    
    # Simulate 30 minutes passing
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Simulating 30 minutes elapsed...")
    # Manually update the first drink time to simulate time passing
    if monitor.first_drink_time:
        from datetime import timedelta
        monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=30)
        monitor._update_bac()
    
    status = monitor.get_current_status()
    print(f"  BAC: {status['bac']:.3f} (after 30 min)")
    print(f"  Status: {status['effects']['level']}")
    print(f"  Effects: {status['effects']['effects']}")
    
    # Add second drink
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Adding 1 shot...")
    monitor.add_drink('liquor')
    time.sleep(2)
    
    status = monitor.get_current_status()
    print(f"  BAC: {status['bac']:.3f} (immediate)")
    print(f"  Status: {status['effects']['level']}")
    print(f"  Effects: {status['effects']['effects']}")
    print(f"  Recommendation: {status['effects']['recommendation']}")
    
    # Simulate 1 hour total elapsed
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Simulating 1 hour total elapsed...")
    if monitor.first_drink_time:
        monitor.first_drink_time = monitor.first_drink_time - timedelta(minutes=30)
        monitor._update_bac()
    
    status = monitor.get_current_status()
    print(f"  BAC: {status['bac']:.3f} (after 1 hour)")
    print(f"  Status: {status['effects']['level']}")
    print(f"  Effects: {status['effects']['effects']}")
    print(f"  Recommendation: {status['effects']['recommendation']}")
    
    # Add third drink
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Adding another beer...")
    monitor.add_drink('beer')
    time.sleep(2)
    
    status = monitor.get_current_status()
    print(f"  BAC: {status['bac']:.3f}")
    print(f"  Status: {status['effects']['level']}")
    print(f"  Effects: {status['effects']['effects']}")
    print(f"  Recommendation: {status['effects']['recommendation']}")
    print(f"  Time to sober: {status['sober_time_hours']:.1f} hours")
    
    # Show sensor data
    sensors = status['sensors']
    print(f"\nSensor Data:")
    print(f"  Heart Rate: {sensors['heart_rate']:.0f} BPM")
    print(f"  Skin Conductance: {sensors['skin_conductance']:.1f} μS")
    print(f"  Temperature: {sensors['temperature']:.1f}°F")
    
    # Create visualizations
    print(f"\nGenerating visualizations...")
    gauge_fig = visualizer.create_bac_gauge(status['bac'])
    gauge_fig.savefig('realistic_bac_gauge.png', dpi=150, bbox_inches='tight')
    print("  Saved: realistic_bac_gauge.png")
    
    wearable_fig = visualizer.create_wearable_display(status)
    wearable_fig.savefig('realistic_wearable_display.png', dpi=150, bbox_inches='tight', facecolor='black')
    print("  Saved: realistic_wearable_display.png")
    
    # Show drink history
    print(f"\nDrink History:")
    for i, drink in enumerate(monitor.drinks, 1):
        time_str = drink['timestamp'].strftime('%H:%M:%S')
        print(f"  {i}. {drink['alcohol_percent']}% alcohol, {drink['volume_oz']} oz at {time_str}")
    
    # Final summary
    print(f"\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Total drinks consumed: {len(monitor.drinks)}")
    print(f"Current BAC: {status['bac']:.3f} ({status['bac']*100:.1f}%)")
    print(f"Status: {status['effects']['level']}")
    print(f"Recommendation: {status['effects']['recommendation']}")
    print(f"Time to sober: {status['sober_time_hours']:.1f} hours")
    
    if status['bac'] >= 0.08:
        print("🚨 WARNING: BAC is at or above legal driving limit!")
    elif status['bac'] >= 0.05:
        print("⚠️  CAUTION: BAC is approaching legal limit")
    else:
        print("✅ BAC is below legal limit")
    
    monitor.stop_monitoring()
    print(f"\nMonitoring stopped.")

if __name__ == "__main__":
    demo_realistic_bac() 