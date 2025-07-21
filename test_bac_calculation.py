"""
Test BAC calculation with realistic values
"""

from bac_calculator import BACCalculator

def test_realistic_bac():
    """Test BAC calculation with realistic drinking scenarios"""
    calculator = BACCalculator()
    
    print("🍺 Testing Realistic BAC Calculations")
    print("=" * 50)
    
    # Test 1: 133 lb female, 1 standard drink (12 oz beer, 5% alcohol)
    print("\nTest 1: 133 lb female, 1 beer (12 oz, 5% alcohol)")
    drinks = [{'volume_oz': 12.0, 'alcohol_percent': 5.0}]
    bac = calculator.calculate_bac_widmark(133, 'female', drinks, 0.5)  # 30 minutes after
    print(f"   BAC after 30 minutes: {bac:.3f}")
    
    # Test 2: 133 lb female, 1 shot (1.5 oz, 40% alcohol)
    print("\nTest 2: 133 lb female, 1 shot (1.5 oz, 40% alcohol)")
    drinks = [{'volume_oz': 1.5, 'alcohol_percent': 40.0}]
    bac = calculator.calculate_bac_widmark(133, 'female', drinks, 0.5)
    print(f"   BAC after 30 minutes: {bac:.3f}")
    
    # Test 3: 133 lb female, 2 beers
    print("\nTest 3: 133 lb female, 2 beers")
    drinks = [
        {'volume_oz': 12.0, 'alcohol_percent': 5.0},
        {'volume_oz': 12.0, 'alcohol_percent': 5.0}
    ]
    bac = calculator.calculate_bac_widmark(133, 'female', drinks, 1.0)  # 1 hour after
    print(f"   BAC after 1 hour: {bac:.3f}")
    
    # Test 4: 133 lb female, 1 beer + 1 shot
    print("\nTest 4: 133 lb female, 1 beer + 1 shot")
    drinks = [
        {'volume_oz': 12.0, 'alcohol_percent': 5.0},
        {'volume_oz': 1.5, 'alcohol_percent': 40.0}
    ]
    bac = calculator.calculate_bac_widmark(133, 'female', drinks, 1.0)
    print(f"   BAC after 1 hour: {bac:.3f}")
    
    # Test 5: 160 lb male, 3 beers
    print("\nTest 5: 160 lb male, 3 beers")
    drinks = [
        {'volume_oz': 12.0, 'alcohol_percent': 5.0},
        {'volume_oz': 12.0, 'alcohol_percent': 5.0},
        {'volume_oz': 12.0, 'alcohol_percent': 5.0}
    ]
    bac = calculator.calculate_bac_widmark(160, 'male', drinks, 1.5)
    print(f"   BAC after 1.5 hours: {bac:.3f}")
    
    # Test 6: Show alcohol content calculations
    print("\n" + "=" * 50)
    print("Alcohol Content Calculations:")
    print("=" * 50)
    
    # 1 beer (12 oz, 5% alcohol)
    volume_ml = 12.0 * 29.5735  # 354.88 ml
    alcohol_ml = volume_ml * 0.05  # 17.74 ml
    alcohol_grams = alcohol_ml * 0.789  # 14.0 grams
    print(f"1 beer (12 oz, 5%): {alcohol_grams:.1f} grams of alcohol")
    
    # 1 shot (1.5 oz, 40% alcohol)
    volume_ml = 1.5 * 29.5735  # 44.36 ml
    alcohol_ml = volume_ml * 0.40  # 17.74 ml
    alcohol_grams = alcohol_ml * 0.789  # 14.0 grams
    print(f"1 shot (1.5 oz, 40%): {alcohol_grams:.1f} grams of alcohol")
    
    # 1 glass of wine (5 oz, 12% alcohol)
    volume_ml = 5.0 * 29.5735  # 147.87 ml
    alcohol_ml = volume_ml * 0.12  # 17.74 ml
    alcohol_grams = alcohol_ml * 0.789  # 14.0 grams
    print(f"1 wine (5 oz, 12%): {alcohol_grams:.1f} grams of alcohol")
    
    print("\nNote: All standard drinks contain approximately 14 grams of alcohol!")

if __name__ == "__main__":
    test_realistic_bac() 