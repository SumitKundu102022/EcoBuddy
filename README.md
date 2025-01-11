# EcoBuddy: Personalized Carbon Footprint Tracker

## Overview
EcoBuddy is a personalized carbon footprint tracker that helps users calculate their carbon footprint, track their progress, and receive actionable tips to reduce their environmental impact. The application is built using Streamlit, Pandas, and Plotly for data visualization.

## Features
- **Carbon Footprint Calculator**: Calculate your monthly carbon footprint based on your daily habits, including transportation, electricity usage, diet, and waste generation.
- **Dynamic Month Display**: View your carbon footprint progress over the last three months and the current month.
- **Personalized Tips**: Receive personalized recommendations to reduce your carbon footprint based on your input.
- **Progress Tracker**: Track your carbon footprint over time with interactive charts.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/EcoBuddy.git
    cd EcoBuddy
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to access the EcoBuddy dashboard.

## File Structure
```
EcoBuddy/
│
├── app.py                  # Main application file
├── requirements.txt        # List of dependencies
├── utils/
│   └── chart_animations.py # Utility functions for chart animations
└── README.md               # Project documentation
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Streamlit for the web application framework
- Pandas for data manipulation
- Plotly for data visualization

## References
- [CarbonCentrik Calculator](https://github.com/AIAnytime/carboncentrik-calculator)
