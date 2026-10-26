# Customer Assist — Warranty Claim Assistant

An AI-powered warranty claim processing system built with **CrewAI**, **Streamlit**, **Ollama**, and **MySQL**. It coordinates a multi-agent sequential pipeline to authenticate customers, verify product serial numbers, evaluate warranty validity, visually inspect uploaded product photos for physical damage, and automatically process claims.

---

## Requirements & Tech Stack

| Component | Version / Runtime | Purpose |
| :--- | :--- | :--- |
| **CrewAI** | `>=1.15.16` | Multi-agent autonomous workflow orchestration |
| **Pydantic** | `>=2.12.5` | Strict data validation & structured task output models |
| **W&B Weave** | `>=0.54.0` | Agent tracing, logging, and LLM observability |
| **Streamlit** | `>=1.66.1` | Web UI for claim intake, file uploads, and status display |
| **Ollama** | Local runtime | Local LLM inference (`minicpm5:2b` text + `qwen3-vl:2b` vision) |
| **PyMySQL / SQLAlchemy** | `>=1.2.0` | Relational database connection and query execution |
| **Pandas** | `>=3.0.6` | Data transformation, string cleaning & CSV management |
| **uv / Python** | `>=3.12` | High-performance Python package and environment manager |

---

## Architecture & Workflow

The system coordinates 6 specialized agents sequentially:

```
[Customer / Streamlit UI]
           │
           ▼
1. Intake Agent             ──► Identifies customer & purchase records via database tools
           │
           ▼
2. Validation Agent         ──► Validates serial number, delivery status & warranty active window
           │
           ▼
3. Damage Inspection Agent  ──► Inspects uploaded photo using vision AI to detect physical damage/abuse
           │
           ▼
4. Claim Agent              ──► Assesses eligibility (active warranty + no physical damage) & logs claim
           │
           ▼
5. Resolution Agent         ──► Formulates resolution recommendation & draft response
           │
           ▼
6. Communication Agent      ──► Delivers customer-ready final status and next steps
```

---

## Agents & Assigned Tools

| Agent | Role | Tools Used |
| :--- | :--- | :--- |
| **Intake Agent** | Customer Support Intake Specialist | `FindCustomerTool`<br>`CustomerPurchasesTool`<br>`VerifySerialTool` |
| **Validation Agent** | Warranty Verification Specialist | `VerifySerialTool`<br>`WarrantyStatusTool`<br>`OrderDeliveryTool` |
| **Damage Inspection Agent** | Product Damage Inspector | `DamageInspectionTool` (Ollama `qwen3-vl:2b`) |
| **Claim Agent** | Warranty Claims Processor | `CreateClaimTool`<br>`ClaimStatusTool`<br>`ClaimHistoryTool` |
| **Resolution Agent** | Warranty Case Resolution Assistant | Synthesizes validation, damage inspection & claim history |
| **Communication Agent** | Customer Communication Specialist | Formats final customer response and instructions |

---

## Prerequisites

- **Python**: `>=3.12` (managed via `uv`)
- **MySQL**: Running locally on port `3306`
- **Ollama**: Running locally with configured text and vision models:
  ```bash
  # Text model for agents and reasoning
  ollama run maternion/minicpm5:2b

  # Vision model for image damage inspection
  ollama run qwen3-vl:2b
  ```

---

## Quick Start

### 1. Installation
Clone the repository and install dependencies:
```bash
uv sync
```

### 2. Environment Configuration
Ensure your `.env` contains the required environment variables:
```env
OPENAI_API_KEY=NA
CREWAI_TELEMETRY_OPT_OUT=True
FABRICATE_API_KEY=your_tonic_fabricate_key
```

### 3. Database Initialization
Ensure MySQL has `local_infile` enabled for CSV loading:
```sql
SET GLOBAL local_infile = 1;
```

### 4. Run Application
Start the Streamlit web interface:
```bash
uv run streamlit run main.py
```

---

## Project Structure

```text
cust_assist/
├── artifacts/
│   └── data_ingestion/       # Source CSV datasets (customers, orders, etc.)
├── logs/                     # Application & execution logs (logging.log)
├── uploads/                  # Temporary storage for customer-uploaded product photos
├── src/cust_assist/
│   ├── config/
│   │   ├── agents.yaml       # Agent roles, goals & backstories
│   │   └── tasks.yaml        # Task definitions & validation criteria
│   ├── database/
│   │   ├── connection.py     # MySQL connection manager
│   │   ├── create_tables.py  # DDL schema definitions
│   │   └── insert_tables.py  # Data loading logic (LOAD DATA LOCAL INFILE)
│   ├── tools/                # Custom database query tools & vision inspection tool
│   │   ├── calculate_warranty_status.py
│   │   ├── check_order_delivery.py
│   │   ├── create_warranty_claim.py
│   │   ├── damage_inspection.py
│   │   ├── find_all_purchases.py
│   │   ├── find_customer.py
│   │   ├── show_claim_history.py
│   │   ├── show_product_details.py
│   │   ├── track_claim_status.py
│   │   └── verify_serial_number.py
│   ├── agents.py             # CrewBase orchestration & 6-agent sequential pipeline
│   └── logger.py             # Centralized logging configuration (writes to logs/logging.log)
├── .env                      # Environment variables
├── main.py                   # Streamlit UI, Weave init & file uploader entry point
├── pyproject.toml            # Project dependencies & metadata
└── README.md
```
