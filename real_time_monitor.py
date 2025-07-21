"""
Real-time BAC Monitoring System
Simulates wearable device sensors and provides continuous BAC tracking
"""

import threading
import time
import queue
import random
from datetime import datetime, timedelta
import numpy as np
from bac_calculator import BACCalculator

class SensorSimulator:
    """Simulates wearable device sensors"""
    
    def __init__(self):
        # Baseline values (normal ranges)
        self.baseline_heart_rate = 70  # BPM
        self.baseline_skin_conductance = 5.0  # microsiemens
        self.baseline_temperature = 98.6  # Fahrenheit
        
        # Current values
        self.current_heart_rate = self.baseline_heart_rate
        self.current_skin_conductance = self.baseline_skin_conductance
        self.current_temperature = self.baseline_temperature
        
        # Alcohol effect simulation
        self.alcohol_effect = 0.0  # 0.0 to 1.0 scale
        
    def update_sensors(self, bac_level):
        """
        Update sensor readings based on current BAC level
        """
        # Simulate alcohol effects on heart rate
        hr_increase = bac_level * 20  # BAC of 0.1 increases HR by ~2 BPM
        self.current_heart_rate = self.baseline_heart_rate + hr_increase + random.uniform(-2, 2)
        
        # Simulate alcohol effects on skin conductance
        sc_increase = bac_level * 3.0  # Alcohol increases skin conductance
        self.current_skin_conductance = self.baseline_skin_conductance + sc_increase + random.uniform(-0.5, 0.5)
        
        # Simulate alcohol effects on temperature
        temp_change = bac_level * 2.0  # Alcohol can affect body temperature
        self.current_temperature = self.baseline_temperature + temp_change + random.uniform(-0.5, 0.5)
        
        # Add some realistic noise
        self.current_heart_rate = max(50, min(120, self.current_heart_rate))
        self.current_skin_conductance = max(1.0, self.current_skin_conductance)
        self.current_temperature = max(95.0, min(102.0, self.current_temperature))

class RealTimeBACMonitor:
    """Main real-time BAC monitoring system"""
    
    def __init__(self, weight_lbs, gender):
        self.bac_calculator = BACCalculator()
        self.sensor_simulator = SensorSimulator()
        
        # User profile
        self.weight_lbs = weight_lbs
        self.gender = gender
        
        # Drink tracking
        self.drinks = []
        self.first_drink_time = None
        self.last_drink_time = None
        
        # Real-time data
        self.current_bac = 0.0
        self.bac_history = []
        self.sensor_history = []
        
        # Monitoring control
        self.is_monitoring = False
        self.monitor_thread = None
        self.data_queue = queue.Queue()
        
        # Alert thresholds
        self.alert_thresholds = {
            'warning': 0.05,
            'danger': 0.08,
            'critical': 0.15
        }
        
        # Alert state tracking (to prevent spam)
        self.last_alert_level = None
        self.last_alert_time = None
        self.alert_cooldown = 30  # seconds between repeated alerts
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            print("BAC monitoring started...")
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("BAC monitoring stopped.")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Update current BAC
                self._update_bac()
                
                # Update sensor readings
                self.sensor_simulator.update_sensors(self.current_bac)
                
                # Record data
                timestamp = datetime.now()
                data_point = {
                    'timestamp': timestamp,
                    'bac': self.current_bac,
                    'heart_rate': self.sensor_simulator.current_heart_rate,
                    'skin_conductance': self.sensor_simulator.current_skin_conductance,
                    'temperature': self.sensor_simulator.current_temperature
                }
                
                self.bac_history.append(data_point)
                self.sensor_history.append(data_point)
                
                # Check for alerts
                self._check_alerts()
                
                # Add to queue for external access
                self.data_queue.put(data_point)
                
                # Sleep for 5 seconds (less frequent updates to reduce spam)
                time.sleep(5)
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(1)
    
    def _update_bac(self):
        """Update current BAC using both calculation methods"""
        if not self.drinks:
            self.current_bac = 0.0
            return
        
        # Calculate time since first drink
        hours_since_first = 0
        if self.first_drink_time:
            hours_since_first = (datetime.now() - self.first_drink_time).total_seconds() / 3600
        
        # Method 1: Widmark formula (more accurate for known consumption)
        calculated_bac = self.bac_calculator.calculate_bac_widmark(
            self.weight_lbs, self.gender, self.drinks, hours_since_first
        )
        
        # Method 2: Sensor-based estimation (for real-time monitoring)
        if self.last_drink_time:
            sensor_bac = self.bac_calculator.estimate_bac_from_sensors(
                self.sensor_simulator.current_heart_rate,
                self.sensor_simulator.current_skin_conductance,
                self.sensor_simulator.current_temperature,
                self.sensor_simulator.baseline_heart_rate,
                self.sensor_simulator.baseline_skin_conductance,
                self.sensor_simulator.baseline_temperature,
                self.last_drink_time,
                self.weight_lbs,
                self.gender
            )
            
            # Combine both methods (weighted average)
            self.current_bac = 0.7 * calculated_bac + 0.3 * sensor_bac
        else:
            self.current_bac = calculated_bac
    
    def _check_alerts(self):
        """Check for BAC level alerts with smart throttling"""
        effects = self.bac_calculator.get_bac_effects(self.current_bac)
        current_time = datetime.now()
        
        # Determine current alert level
        current_alert_level = None
        if self.current_bac >= self.alert_thresholds['critical']:
            current_alert_level = 'critical'
        elif self.current_bac >= self.alert_thresholds['danger']:
            current_alert_level = 'danger'
        elif self.current_bac >= self.alert_thresholds['warning']:
            current_alert_level = 'warning'
        
        # Only send alert if:
        # 1. Alert level has changed, OR
        # 2. It's been more than cooldown time since last alert
        should_alert = False
        
        if current_alert_level != self.last_alert_level:
            # Alert level changed - always alert
            should_alert = True
        elif (current_alert_level and 
              (not self.last_alert_time or 
               (current_time - self.last_alert_time).total_seconds() > self.alert_cooldown)):
            # Same alert level but cooldown has passed
            should_alert = True
        
        if should_alert and current_alert_level:
            if current_alert_level == 'critical':
                self._send_alert("CRITICAL", f"BAC: {self.current_bac:.3f} - {effects['recommendation']}")
            elif current_alert_level == 'danger':
                self._send_alert("DANGER", f"BAC: {self.current_bac:.3f} - {effects['recommendation']}")
            elif current_alert_level == 'warning':
                self._send_alert("WARNING", f"BAC: {self.current_bac:.3f} - {effects['recommendation']}")
            
            # Update alert state
            self.last_alert_level = current_alert_level
            self.last_alert_time = current_time
    
    def _send_alert(self, level, message):
        """Send alert (in real implementation, this would trigger notifications)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level} ALERT: {message}")
    
    def add_drink(self, drink_type, volume_oz=None, alcohol_percent=None):
        """Add a drink to the tracking system"""
        drink_info = self.bac_calculator.add_drink(drink_type, volume_oz, alcohol_percent)
        drink_info['timestamp'] = datetime.now()
        
        self.drinks.append(drink_info)
        
        if not self.first_drink_time:
            self.first_drink_time = datetime.now()
        
        self.last_drink_time = datetime.now()
        
        # Update BAC immediately after adding drink
        self._update_bac()
        
        print(f"Added drink: {drink_type} at {self.last_drink_time.strftime('%H:%M:%S')}")
    
    def get_current_status(self):
        """Get current BAC status and effects"""
        effects = self.bac_calculator.get_bac_effects(self.current_bac)
        sober_time = self.bac_calculator.calculate_sober_time(self.current_bac)
        
        return {
            'bac': self.current_bac,
            'effects': effects,
            'sober_time_hours': sober_time,
            'sensors': {
                'heart_rate': self.sensor_simulator.current_heart_rate,
                'skin_conductance': self.sensor_simulator.current_skin_conductance,
                'temperature': self.sensor_simulator.current_temperature
            },
            'drinks_count': len(self.drinks),
            'time_since_last_drink': (datetime.now() - self.last_drink_time).total_seconds() / 60 if self.last_drink_time else 0
        }
    
    def get_recent_data(self, minutes=30):
        """Get recent monitoring data"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_data = [point for point in self.bac_history if point['timestamp'] > cutoff_time]
        return recent_data
    
    def reset_session(self):
        """Reset the current drinking session"""
        self.drinks = []
        self.first_drink_time = None
        self.last_drink_time = None
        self.current_bac = 0.0
        self.bac_history = []
        self.sensor_history = []
        self.last_alert_level = None
        self.last_alert_time = None
        print("Session reset - starting fresh monitoring")
    
    def check_alerts_manually(self):
        """Manually check and display current alert status"""
        effects = self.bac_calculator.get_bac_effects(self.current_bac)
        
        if self.current_bac >= self.alert_thresholds['critical']:
            print(f"🚨 CRITICAL ALERT: BAC {self.current_bac:.3f} - {effects['recommendation']}")
        elif self.current_bac >= self.alert_thresholds['danger']:
            print(f"⚠️  DANGER ALERT: BAC {self.current_bac:.3f} - {effects['recommendation']}")
        elif self.current_bac >= self.alert_thresholds['warning']:
            print(f"⚠️  WARNING: BAC {self.current_bac:.3f} - {effects['recommendation']}")
        else:
            print(f"✅ SAFE: BAC {self.current_bac:.3f} - {effects['effects']}")
    
    def set_alert_cooldown(self, seconds):
        """Set the cooldown time between repeated alerts"""
        self.alert_cooldown = seconds
        print(f"Alert cooldown set to {seconds} seconds") 