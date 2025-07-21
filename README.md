# 🍺 Real-time BAC Monitoring System

A comprehensive Python application for real-time Blood Alcohol Content (BAC) monitoring, designed for wearable devices like Apple Watch. This system combines traditional BAC calculation methods with simulated sensor data to provide accurate, real-time alcohol level tracking.

## 🌟 Features

### Core Functionality
- **Real-time BAC calculation** using the Widmark formula
- **Sensor-based estimation** using simulated wearable device sensors
- **Continuous monitoring** with 1-second update intervals
- **Safety alerts** with customizable thresholds
- **Drink tracking** with comprehensive database

### Visualization & Interface
- **Interactive web dashboard** using Streamlit
- **Real-time charts** with Plotly
- **BAC gauge display** suitable for wearable devices
- **Command-line interface** for testing and development
- **Wearable-optimized displays** with compact layouts

### Safety Features
- **Multi-level alerts** (Warning, Danger, Critical)
- **Time-to-sober calculations**
- **Effect descriptions** based on BAC levels
- **Recommendations** for safe behavior
- **Session management** with reset capabilities

## 🏗️ Architecture

### Core Components

1. **`bac_calculator.py`** - Core BAC calculation engine
   - Widmark formula implementation
   - Sensor-based estimation algorithms
   - Effect classification and recommendations

2. **`real_time_monitor.py`** - Real-time monitoring system
   - Continuous data collection
   - Sensor simulation
   - Alert management
   - Thread-safe operations

3. **`visualization.py`** - Data visualization tools
   - BAC gauges and charts
   - Wearable device displays
   - Interactive dashboards

4. **`main.py`** - Command-line application
   - Interactive demo mode
   - Simulation mode
   - Wearable demo

5. **`web_app.py`** - Streamlit web interface
   - Modern web dashboard
   - Real-time updates
   - User-friendly controls

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd bacLevelApp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python main.py
   ```

## 🚀 Usage

### Quick Start

1. **Run the main application**
   ```bash
   python main.py
   ```

2. **Choose your preferred mode:**
   - **Interactive Demo** - Command-line interface for testing
   - **Simulation** - Automated drinking pattern demonstration
   - **Wearable Demo** - Compact display simulation
   - **Web Interface** - Full-featured web dashboard

### Web Interface

1. **Launch the Streamlit app**
   ```bash
   streamlit run web_app.py
   ```

2. **Set up your profile** in the sidebar
   - Enter your weight and gender
   - These affect BAC calculations

3. **Start monitoring**
   - Click "Start" to begin real-time monitoring
   - Add drinks as you consume them
   - Monitor your BAC levels and sensor data

### Command-Line Interface

```bash
python main.py
```

Available commands in interactive mode:
- `start` - Start monitoring
- `stop` - Stop monitoring
- `add <drink>` - Add a drink (beer/wine/liquor/cocktail)
- `status` - Show current status
- `chart` - Show real-time chart
- `gauge` - Show BAC gauge
- `reset` - Reset session
- `quit` - Exit program

## 🔬 Technical Details

### BAC Calculation Methods

1. **Widmark Formula**
   ```
   BAC = (A / (r * W)) - (β * t)
   ```
   Where:
   - A = total alcohol consumed (grams)
   - r = Widmark factor (0.68 for males, 0.55 for females)
   - W = body weight (grams)
   - β = alcohol elimination rate (0.015 per hour)
   - t = time since first drink (hours)

2. **Sensor-Based Estimation**
   - Heart rate monitoring
   - Skin conductance measurement
   - Temperature tracking
   - Baseline comparison algorithms

### Sensor Simulation

The system simulates wearable device sensors:
- **Heart Rate**: Baseline 70 BPM, increases with alcohol
- **Skin Conductance**: Baseline 5.0 μS, increases with alcohol
- **Temperature**: Baseline 98.6°F, affected by alcohol

### Alert Thresholds

- **Warning**: BAC ≥ 0.05 (0.05%)
- **Danger**: BAC ≥ 0.08 (0.08%) - Legal driving limit
- **Critical**: BAC ≥ 0.15 (0.15%)

## 📊 BAC Effects Reference

| BAC Level | Status | Effects | Recommendation |
|-----------|--------|---------|----------------|
| < 0.02 | Sober | No significant effects | Safe to drive |
| 0.02-0.05 | Mild Impairment | Slight euphoria, relaxation | Exercise caution |
| 0.05-0.08 | Moderate Impairment | Impaired judgment, reduced coordination | Do not drive |
| 0.08-0.15 | High Impairment | Significant impairment, poor coordination | Seek safe transportation |
| > 0.15 | Severe Impairment | Severe impairment, risk of alcohol poisoning | Seek medical attention |

## 🛠️ Development

### Project Structure
```
bacLevelApp/
├── bac_calculator.py      # Core BAC calculation engine
├── real_time_monitor.py   # Real-time monitoring system
├── visualization.py       # Data visualization tools
├── main.py               # Command-line application
├── web_app.py            # Streamlit web interface
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Adding New Features

1. **New Sensor Types**
   - Extend `SensorSimulator` class in `real_time_monitor.py`
   - Update `estimate_bac_from_sensors` method in `bac_calculator.py`

2. **New Drink Types**
   - Add to `drink_database` in `BACCalculator` class
   - Update web interface drink selection

3. **Custom Visualizations**
   - Extend `BACVisualizer` class in `visualization.py`
   - Add new chart types and displays

## ⚠️ Important Notes

### Safety Disclaimer
This application is for educational and demonstration purposes only. It should not be used as a substitute for professional medical advice or as a tool for making decisions about driving or operating machinery.

### Accuracy Limitations
- BAC calculations are estimates based on mathematical models
- Individual metabolism varies significantly
- Sensor data is simulated and may not reflect real-world conditions
- Always err on the side of caution when making safety decisions

### Legal Considerations
- BAC levels above 0.08% are illegal for driving in most jurisdictions
- Local laws may vary - always check your local regulations
- This tool does not provide legal advice

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New features
- Documentation improvements
- Performance optimizations

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Widmark formula for BAC calculation
- Streamlit for the web interface framework
- Plotly for interactive visualizations
- Matplotlib for static charts and displays

---

**Remember**: Always drink responsibly and never drive under the influence of alcohol. This tool is designed to promote safety and awareness, not to enable risky behavior. 