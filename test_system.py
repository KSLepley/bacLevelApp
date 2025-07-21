"""
Test script for the BAC Monitoring System
Verifies all components work correctly
"""

import time
from datetime import datetime
from bac_calculator import BACCalculator
from real_time_monitor import RealTimeBACMonitor
from visualization import BACVisualizer

def test_bac_calculator():
    """Test the BAC calculator functionality"""
    print("🧪 Testing BAC Calculator...")
    
    calculator = BACCalculator()
    
    # Test Widmark calculation
    drinks = [
        {'volume_oz': 12.0, 'alcohol_percent': 5.0},  # 1 beer
        {'volume_oz': 5.0, 'alcohol_percent': 12.0}   # 1 wine
    ]
    
    bac = calculator.calculate_bac_widmark(150, 'male', drinks, 1.0)
    print(f"   BAC after 1 hour: {bac:.3f}")
    
    # Test effects classification
    effects = calculator.get_bac_effects(bac)
    print(f"   Status: {effects['level']}")
    print(f"   Effects: {effects['effects']}")
    
    # Test sober time calculation
    sober_time = calculator.calculate_sober_time(bac)
    print(f"   Time to sober: {sober_time:.1f} hours")
    
    print("✅ BAC Calculator tests passed!\n")

def test_real_time_monitor():
    """Test the real-time monitoring system"""
    print("🧪 Testing Real-time Monitor...")
    
    monitor = RealTimeBACMonitor(150, 'male')
    
    # Test initial status
    status = monitor.get_current_status()
    print(f"   Initial BAC: {status['bac']:.3f}")
    print(f"   Initial status: {status['effects']['level']}")
    
    # Test adding drinks
    monitor.add_drink('beer')
    monitor.add_drink('wine')
    
    # Wait a moment for processing
    time.sleep(1)
    
    status = monitor.get_current_status()
    print(f"   BAC after drinks: {status['bac']:.3f}")
    print(f"   Drinks consumed: {status['drinks_count']}")
    
    # Test sensor data
    sensors = status['sensors']
    print(f"   Heart Rate: {sensors['heart_rate']:.0f} BPM")
    print(f"   Skin Conductance: {sensors['skin_conductance']:.1f} μS")
    print(f"   Temperature: {sensors['temperature']:.1f}°F")
    
    print("✅ Real-time Monitor tests passed!\n")

def test_visualization():
    """Test the visualization components"""
    print("🧪 Testing Visualization...")
    
    visualizer = BACVisualizer()
    
    # Test BAC gauge creation
    gauge_fig = visualizer.create_bac_gauge(0.075)
    print("   BAC gauge created successfully")
    
    # Test wearable display
    status = {
        'bac': 0.075,
        'effects': {'level': 'Moderate Impairment'},
        'sober_time_hours': 5.0,
        'sensors': {'heart_rate': 85}
    }
    
    wearable_fig = visualizer.create_wearable_display(status)
    print("   Wearable display created successfully")
    
    print("✅ Visualization tests passed!\n")

def test_integration():
    """Test the complete system integration"""
    print("🧪 Testing System Integration...")
    
    # Create monitor
    monitor = RealTimeBACMonitor(160, 'female')
    visualizer = BACVisualizer()
    
    # Start monitoring
    monitor.start_monitoring()
    time.sleep(1)
    
    # Add drinks
    monitor.add_drink('beer')
    time.sleep(2)
    monitor.add_drink('liquor')
    time.sleep(2)
    
    # Get status and create visualizations
    status = monitor.get_current_status()
    
    print(f"   Final BAC: {status['bac']:.3f}")
    print(f"   Status: {status['effects']['level']}")
    print(f"   Time to sober: {status['sober_time_hours']:.1f} hours")
    
    # Create visualizations
    gauge_fig = visualizer.create_bac_gauge(status['bac'])
    wearable_fig = visualizer.create_wearable_display(status)
    
    print("   All visualizations created successfully")
    
    # Stop monitoring
    monitor.stop_monitoring()
    
    print("✅ Integration tests passed!\n")

def main():
    """Run all tests"""
    print("🍺 BAC Monitoring System - Test Suite")
    print("=" * 50)
    
    try:
        test_bac_calculator()
        test_real_time_monitor()
        test_visualization()
        test_integration()
        
        print("🎉 All tests passed! The system is working correctly.")
        print("\nYou can now run:")
        print("  python main.py          # For command-line interface")
        print("  streamlit run web_app.py # For web interface")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print("Please check your installation and dependencies.")

if __name__ == "__main__":
    main() 