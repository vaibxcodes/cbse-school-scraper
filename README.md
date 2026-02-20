# 🏫 CBSE School Scraper

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Automation](https://img.shields.io/badge/Web-Scraping-orange)

A multi-threaded Python scraper that extracts complete CBSE affiliated school details from the official SARAS portal.

This tool allows you to download **state-wise CBSE school data** using a simple state code.

---

## 🎯 Why This Project?

This project demonstrates:

- Web scraping automation
- Multi-threaded data processing
- CLI-based execution
- Containerization using Docker
- Volume mounting for persistent storage
- Clean project structuring
- DevOps workflow (Git + Docker)

---

## 🚀 What This Project Does

The CBSE SARAS portal provides school affiliation data via a web interface.

This project automates:

- Form submission
- Anti-forgery (CSRF) token handling
- School list extraction
- Detail page crawling
- Multi-threaded scraping
- Structured CSV export

All using pure Python.

---

## ✨ Features

- ✅ State-wise school data extraction
- ✅ Automatic CSRF token handling
- ✅ Multi-threaded detail page scraping
- ✅ Fast performance (thousands of schools)
- ✅ Structured CSV output
- ✅ Docker support
- ✅ Clean project structure
- ✅ Scalable for all Indian states

---

## 🛠 Tech Stack

- Python 3.12
- requests
- beautifulsoup4
- pandas
- concurrent.futures (ThreadPoolExecutor)
- Docker

---

## 📂 Project Structure

```text
cbse-school-scraper/
│
├── scraper.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
├── .gitignore
└── output/
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/vaibxcodes/cbse-school-scraper.git
cd cbse-school-scraper
```

---

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required Python dependencies defined in `requirements.txt`.

---

# ▶️ Usage (Local Python)

Run the scraper by passing the **state code**:

```bash
python scraper.py <STATE_CODE>
```

---

## 🔹 Example Usage

```bash
python scraper.py 05   # Bihar
python scraper.py 09   # Uttar Pradesh
python scraper.py 27   # Delhi
python scraper.py 35   # Uttarakhand
```

---

## 📌 Common State Codes

| State | Code |
|--------|------|
| Bihar | 05 |
| Uttar Pradesh | 09 |
| Delhi | 27 |
| Uttarakhand | 35 |
| Rajasthan | 08 |
| Maharashtra | 17 |
| Gujarat | 24 |

*(Additional state codes can be identified from the CBSE SARAS portal.)*

---

# 🐳 Docker Usage

You can run this scraper without installing Python locally using Docker.

---

## 🔹 Build Docker Image

```bash
docker build -t cbse-scraper .
```

---

## 🔹 Run Scraper (with output mounted)

```bash
docker run -v $(pwd)/output:/app/output cbse-scraper <STATE_CODE>
```

### Example:

```bash
docker run -v $(pwd)/output:/app/output cbse-scraper 05
```

The CSV file will be saved inside your local `output/` directory.

---

# 📥 Output

After successful execution, the scraper generates a structured CSV file inside the `output/` directory:

```
output/state_<STATE_CODE>_school_details.csv
```

Example:

```
output/state_05_school_details.csv
```

The CSV contains detailed school information such as:

- School Name
- Affiliation Number
- State
- District
- Address
- Website
- Principal Name
- Year of Foundation
- And more

---

# ⚡ Performance

- Uses multi-threading (5 workers)
- Efficiently handles thousands of schools
- Optimized for large states (e.g., Uttar Pradesh, Bihar)
- Significantly faster than sequential scraping

---

# 🧠 How It Works Internally

1. Fetches verification token from SARAS portal
2. Submits state-wise form request
3. Extracts school listing table
4. Collects detail page URLs
5. Scrapes detail pages in parallel
6. Exports structured CSV file

---

# ⚠️ Disclaimer

This project is intended for:

- Educational purposes
- Automation learning
- Research use

Please use responsibly and avoid excessive automated requests that may overload the target server.

---

# 👨‍💻 Author

**Vaibhav Patil**  
DevOps & Automation Enthusiast 🚀

---

# 🌟 Future Improvements

- PostgreSQL storage support
- Logging & retry mechanism
- CLI argument parsing with argparse
- All-India automated scraper mode
- REST API wrapper
- CI/CD integration
- Scheduled execution using cron containers
