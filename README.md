# Moonarch Token Scanner
 A script which leverages Selenium, BeautifulSoup, and undetected_chromedriver to continuously monitor the top gainers on [Moonarch](https://moonarch.app/), a tool which offers real-time data, insights to support users in making informed decisions. 
 The script retrieves token information, including age and analysis results, and filters potential gems based on specific criteria.
## Getting Started

### Key Features:
- Scrapes Moonarch's top gainers page for token data.
- Extracts token addresses and searches for additional information.
- Calculates token age and evaluates potential gems based on predefined conditions.
- Sends Telegram messages for identified potential gems(Not implemented yet)


### Installation
1. Clone the repository:
   git clone https://github.com/Eben001/nairaland_autorepy_bot.git
   cd moonarch
   [install a virtual environment if you wish](https://docs.python.org/3/library/venv.html)

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

### Usage
   Ensure the required dependencies are installed properly. 

3. Run the script:
   ```bash
   python main.py

### Fascinating Discovery
One fascinating discovering during this project was the need keep the Chrome DevTools open during the session. 
It's kinda quirky but it was essential for locating elements on the Moonarch website. Happy coding :)

### Disclaimer: 
Use this script responsibly. The script is intended for educational purposes only and does not guarantee investment success. 
It is not financial advice. Do your own research (DYOR) before making any investment decisions.
  
