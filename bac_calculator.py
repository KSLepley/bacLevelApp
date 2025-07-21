"""
Blood Alcohol Content (BAC) Calculator
Real-time BAC monitoring system for wearable devices
"""

import numpy as np
from datetime import datetime, timedelta
import math

class BACCalculator:
    def __init__(self):
        # Widmark factors (average values)
        self.male_widmark_factor = 0.68
        self.female_widmark_factor = 0.55
        
        # Alcohol metabolism rate (average)
        self.metabolism_rate = 0.015  # BAC per hour
        
        # Drink database (standard drinks)
        self.drink_database = {
            'beer': {'alcohol_percent': 5.0, 'volume_oz': 12.0},
            'wine': {'alcohol_percent': 12.0, 'volume_oz': 5.0},
            'liquor': {'alcohol_percent': 40.0, 'volume_oz': 1.5},
            'cocktail': {'alcohol_percent': 15.0, 'volume_oz': 8.0}
        }
    
    def calculate_bac_widmark(self, weight_lbs, gender, drinks, hours_since_first_drink):
        """
        Calculate BAC using the Widmark formula
        BAC = (A / (r * W)) - (β * t)
        
        Where:
        A = total alcohol consumed (grams)
        r = Widmark factor (0.68 for males, 0.55 for females)
        W = body weight (grams)
        β = alcohol elimination rate (0.015 per hour)
        t = time since first drink (hours)
        """
        # Convert weight to grams
        weight_grams = weight_lbs * 453.592
        
        # Calculate total alcohol consumed (in grams)
        total_alcohol_grams = 0
        for drink in drinks:
            # Convert ounces to milliliters, then calculate alcohol content
            # 1 oz = 29.5735 ml
            # Alcohol density = 0.789 g/ml
            volume_ml = drink['volume_oz'] * 29.5735
            alcohol_ml = volume_ml * (drink['alcohol_percent'] / 100)
            alcohol_grams = alcohol_ml * 0.789
            total_alcohol_grams += alcohol_grams
        
        # Get appropriate Widmark factor
        widmark_factor = self.male_widmark_factor if gender.lower() == 'male' else self.female_widmark_factor
        
        # Calculate peak BAC (without metabolism)
        # The Widmark formula gives BAC as a decimal, but we need to convert to standard format
        # Standard BAC is typically expressed as 0.08 (8%) rather than 0.0008
        peak_bac = (total_alcohol_grams / (widmark_factor * weight_grams)) * 100
        
        # Apply metabolism over time
        # Note: Peak BAC typically occurs 30-60 minutes after consumption
        # For simplicity, we'll assume peak at 30 minutes and apply metabolism from there
        if hours_since_first_drink <= 0.5:  # Within 30 minutes
            # Still rising to peak
            bac = peak_bac * (hours_since_first_drink / 0.5)
        else:
            # Past peak, apply metabolism
            time_since_peak = hours_since_first_drink - 0.5
            bac = peak_bac - (self.metabolism_rate * time_since_peak)
        
        # Ensure BAC doesn't go below 0
        return max(0, bac)
    
    def estimate_bac_from_sensors(self, heart_rate, skin_conductance, temperature, 
                                baseline_hr, baseline_sc, baseline_temp, 
                                last_drink_time, weight_lbs, gender):
        """
        Estimate BAC using wearable sensor data
        This is a simplified model - real implementations would use more sophisticated algorithms
        """
        current_time = datetime.now()
        hours_since_drink = (current_time - last_drink_time).total_seconds() / 3600
        
        # Calculate deviations from baseline
        hr_deviation = (heart_rate - baseline_hr) / baseline_hr
        sc_deviation = (skin_conductance - baseline_sc) / baseline_sc
        temp_deviation = (temperature - baseline_temp) / baseline_temp
        
        # Simplified BAC estimation based on sensor deviations
        # This is a placeholder algorithm - real systems would use machine learning
        estimated_bac = 0
        
        if hr_deviation > 0.1:  # Heart rate increased by more than 10%
            estimated_bac += 0.02 * hr_deviation
        
        if sc_deviation > 0.15:  # Skin conductance increased
            estimated_bac += 0.015 * sc_deviation
        
        if temp_deviation > 0.02:  # Temperature increased
            estimated_bac += 0.01 * temp_deviation
        
        # Apply time decay
        estimated_bac *= math.exp(-self.metabolism_rate * hours_since_drink)
        
        return max(0, estimated_bac)
    
    def get_bac_effects(self, bac):
        """
        Return effects and recommendations based on BAC level
        """
        if bac < 0.02:
            return {
                'level': 'Sober',
                'effects': 'No significant effects',
                'recommendation': 'Safe to drive',
                'color': 'green'
            }
        elif bac < 0.05:
            return {
                'level': 'Mild Impairment',
                'effects': 'Slight euphoria, relaxation, decreased inhibition',
                'recommendation': 'Exercise caution',
                'color': 'yellow'
            }
        elif bac < 0.08:
            return {
                'level': 'Moderate Impairment',
                'effects': 'Impaired judgment, reduced coordination, slower reaction time',
                'recommendation': 'Do not drive',
                'color': 'orange'
            }
        elif bac < 0.15:
            return {
                'level': 'High Impairment',
                'effects': 'Significant impairment, poor coordination, slurred speech',
                'recommendation': 'Do not drive, seek safe transportation',
                'color': 'red'
            }
        else:
            return {
                'level': 'Severe Impairment',
                'effects': 'Severe impairment, risk of alcohol poisoning',
                'recommendation': 'Seek medical attention if needed',
                'color': 'darkred'
            }
    
    def calculate_sober_time(self, current_bac):
        """
        Calculate time until BAC returns to zero
        """
        if current_bac <= 0:
            return 0
        
        hours_to_sober = current_bac / self.metabolism_rate
        return hours_to_sober
    
    def add_drink(self, drink_type, volume_oz=None, alcohol_percent=None):
        """
        Add a drink to the tracking system
        """
        if drink_type in self.drink_database:
            drink_info = self.drink_database[drink_type].copy()
            if volume_oz:
                drink_info['volume_oz'] = volume_oz
            if alcohol_percent:
                drink_info['alcohol_percent'] = alcohol_percent
            return drink_info
        else:
            # Custom drink
            return {
                'alcohol_percent': alcohol_percent or 5.0,
                'volume_oz': volume_oz or 12.0
            } 