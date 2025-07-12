# NBP Currency Exchange Rate Archiver

This is a command-line application written in Python for fetching, storing, and managing daily currency exchange rates from the official National Bank of Poland (NBP) API.

---

## Features

- 📥 **Fetch Current Rates**  
  Downloads the latest 'Table A' exchange rates from the NBP API.

- 🗃️ **Local Database**  
  Stores historical rate data in a local SQLite database (`kursy_walut.db`) for persistent archiving.

- 🔍 **Search Archive**  
  Allows users to search the historical data for a specific currency by its code (e.g. USD, EUR).

- 💱 **Currency Calculator**  
  Converts a given amount from PLN to a target currency based on the latest available exchange rate.

- 📄 **CSV Export**  
  Exports the entire historical database to a file named `archiwum_kursow.csv`.

---

## Setup and Installation

Clone the repository:

```bash
git clone https://github.com/your-username/currency-cli.git
cd currency-cli
```

(Replace `your-username` with your actual GitHub username.)

Create and activate a virtual environment:

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## How to Run

Once setup is complete, run the application with:

```bash
python main.py
```

This will launch the interactive command-line menu. Follow the on-screen prompts to:

- Fetch current exchange rates
- Browse historical data
- Search by currency code
- Convert PLN to another currency
- Export to CSV

---

## Project Structure

```plaintext
currency-cli/
├── main.py               # Main script for menu interface and logic
├── kursy_walut.db        # SQLite database (created on first run)
├── archiwum_kursow.csv   # Exported CSV file (optional)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Developed by **mateuszvdl**  
Contributions, feedback, and pull requests are welcome!
