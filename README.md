# market-feed-exporter

market-feed-exporter is a CLI tool allowing to export ODL market feeds into a .CSV file.

## Usage
1. Clone the repository:
```bash
git clone https://github.com/vbessonov/market-feed-exporter.git
```

2. Activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
``` 

3. Install poetry:
```bash
pip install poetry
```

4. Install the package:
```bash
poetry install
```

5. Run the exporter:
```bash
python -m market_feed_exporter \
  --feed-url https://market.feedbooks.com/api/libraries/harvest.json \
  --feed-login <LOGIN> \
  --feed-password <PASSWORD> \
  --output-file output.csv
```