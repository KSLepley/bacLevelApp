"""
Debug BAC calculation step by step
"""

from bac_calculator import BACCalculator

def debug_bac_calculation():
    """Debug the BAC calculation step by step"""
    calculator = BACCalculator()
    
    print("🔍 Debugging BAC Calculation")
    print("=" * 50)
    
    # Test case: 133 lb female, 1 beer
    weight_lbs = 133
    gender = 'female'
    drinks = [{'volume_oz': 12.0, 'alcohol_percent': 5.0}]
    hours_since_first_drink = 0.5
    
    print(f"Input parameters:")
    print(f"  Weight: {weight_lbs} lbs")
    print(f"  Gender: {gender}")
    print(f"  Drinks: {drinks}")
    print(f"  Hours since first drink: {hours_since_first_drink}")
    print()
    
    # Step 1: Convert weight to grams
    weight_grams = weight_lbs * 453.592
    print(f"Step 1: Weight conversion")
    print(f"  {weight_lbs} lbs × 453.592 = {weight_grams:.0f} grams")
    print()
    
    # Step 2: Calculate alcohol content
    total_alcohol_grams = 0
    for i, drink in enumerate(drinks):
        volume_ml = drink['volume_oz'] * 29.5735
        alcohol_ml = volume_ml * (drink['alcohol_percent'] / 100)
        alcohol_grams = alcohol_ml * 0.789
        total_alcohol_grams += alcohol_grams
        
        print(f"Step 2.{i+1}: Drink {i+1} alcohol calculation")
        print(f"  Volume: {drink['volume_oz']} oz × 29.5735 = {volume_ml:.1f} ml")
        print(f"  Alcohol: {volume_ml:.1f} ml × {drink['alcohol_percent']/100:.2f} = {alcohol_ml:.1f} ml")
        print(f"  Weight: {alcohol_ml:.1f} ml × 0.789 = {alcohol_grams:.1f} grams")
        print()
    
    print(f"Total alcohol consumed: {total_alcohol_grams:.1f} grams")
    print()
    
    # Step 3: Get Widmark factor
    widmark_factor = calculator.female_widmark_factor if gender.lower() == 'female' else calculator.male_widmark_factor
    print(f"Step 3: Widmark factor")
    print(f"  {gender} Widmark factor: {widmark_factor}")
    print()
    
    # Step 4: Calculate BAC using improved Widmark formula
    A = total_alcohol_grams
    r = widmark_factor
    W = weight_grams
    beta = calculator.metabolism_rate
    t = hours_since_first_drink
    
    print(f"Step 4: Improved Widmark formula")
    
    # Calculate peak BAC
    peak_bac = (A / (r * W)) * 100
    print(f"  Peak BAC = (A / (r × W)) × 100 = ({A:.1f} / ({r} × {W:.0f})) × 100")
    print(f"  Peak BAC = ({A:.1f} / {r * W:.0f}) × 100 = {peak_bac:.6f}")
    
    # Apply time-based metabolism
    if t <= 0.5:  # Within 30 minutes
        bac = peak_bac * (t / 0.5)
        print(f"  Within 30 minutes: BAC = {peak_bac:.6f} × ({t:.1f} / 0.5) = {bac:.6f}")
    else:
        time_since_peak = t - 0.5
        bac = peak_bac - (beta * time_since_peak)
        print(f"  Past peak: BAC = {peak_bac:.6f} - ({beta} × {time_since_peak:.1f}) = {bac:.6f}")
    
    print()
    
    # Final result
    final_bac = max(0, bac)
    print(f"Final BAC: {final_bac:.3f}")
    
    # Expected BAC for 1 standard drink
    print(f"\nExpected BAC for 1 standard drink (14g alcohol):")
    print(f"  Typical range: 0.02-0.03 for average person")
    print(f"  Our calculation: {final_bac:.3f}")
    
    if final_bac < 0.01:
        print("❌ BAC is too low - there's still an issue!")
    else:
        print("✅ BAC calculation looks reasonable!")

if __name__ == "__main__":
    debug_bac_calculation() 