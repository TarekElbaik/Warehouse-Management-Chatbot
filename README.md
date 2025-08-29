# 🏪 Warehouse Chatbot System

A comprehensive warehouse management chatbot system built with Rasa, FastAPI microservices, and a modern web interface. The system handles order tracking, rescheduling, and inventory management with intelligent intent classification.

## 📋 Table of Contents

- [System Overview](#system-overview)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Running the System](#running-the-system)
- [Usage Examples](#usage-examples)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

## 🏗️ System Overview

The chatbot system consists of multiple microservices:

1. **Rasa Core & Actions Server** - Main conversation engine and custom actions
2. **Classifier Service** - Intent classification using scikit-learn
3. **LLM Normalizer** - Text preprocessing and normalization
4. **Web Interface** - Modern chat UI for user interaction

### Features

- ✅ **Order Tracking** - Track order status and delivery information
- 📅 **Order Rescheduling** - Change delivery dates for existing orders
- 📦 **Inventory Management** - Check stock levels and product availability
- 🤖 **Smart Intent Classification** - Machine learning-powered conversation understanding
- 🌐 **Modern Web UI** - Responsive chat interface with real-time messaging

## 🔧 Prerequisites

Before starting, ensure you have the following installed:

### Required Software

- **Python 3.8+** (tested with Python 3.8-3.11)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### System Requirements

- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: ~2GB free space for dependencies
- **OS**: Windows 10+, macOS 10.15+, or Ubuntu 18.04+

## 🚀 Installation Guide

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd warehouse-chatbot
```

### Step 2: Create Virtual Environments

The project uses separate virtual environments for each service to avoid dependency conflicts.

```bash
# Create virtual environments
python -m venv .venv-rasa
python -m venv .venv-classifier
python -m venv .venv-llm
```

### Step 3: Install Dependencies

#### For Rasa Service

```bash
# Activate Rasa environment
# On Windows:
.venv-rasa\Scripts\activate
# On macOS/Linux:
source .venv-rasa/bin/activate

# Install Rasa dependencies
pip install -r rasa/requirements.txt

# Deactivate environment
deactivate
```

#### For Classifier Service

```bash
# Activate classifier environment
# On Windows:
.venv-classifier\Scripts\activate
# On macOS/Linux:
source .venv-classifier/bin/activate

# Install classifier dependencies
pip install -r services/classifier/requirements.txt

# Deactivate environment
deactivate
```

#### For LLM Service

```bash
# Activate LLM environment
# On Windows:
.venv-llm\Scripts\activate
# On macOS/Linux:
source .venv-llm/bin/activate

# Install LLM dependencies
pip install -r services/llm/requirements.txt

# Deactivate environment
deactivate
```

### Step 4: Train Models

#### Train the Classifier Model

```bash
# Activate classifier environment
# On Windows:
.venv-classifier\Scripts\activate
# On macOS/Linux:
source .venv-classifier/bin/activate

# Train the intent classification model
python services/classifier/train_classifier.py

deactivate
```

#### Train the Rasa Model

```bash
# Activate Rasa environment
# On Windows:
.venv-rasa\Scripts\activate
# On macOS/Linux:
source .venv-rasa/bin/activate

# Navigate to rasa directory and train
cd rasa
rasa train

# Go back to root directory
cd ..
deactivate
```

## 🏃‍♂️ Running the System

The system requires multiple services to be running simultaneously. You'll need **4 terminal windows**.

### Terminal 1: Classifier Service

```bash
# Activate classifier environment
# On Windows:
.venv-classifier\Scripts\activate
# On macOS/Linux:
source .venv-classifier/bin/activate

# Start classifier service
python services/classifier/app.py

# Service will run on: http://localhost:8001
```

### Terminal 2: LLM Normalizer Service

```bash
# Activate LLM environment
# On Windows:
.venv-llm\Scripts\activate
# On macOS/Linux:
source .venv-llm/bin/activate

# Start LLM normalizer service
python services/llm/app.py

# Service will run on: http://localhost:8002
```

### Terminal 3: Rasa Actions Server

```bash
# Activate Rasa environment
# On Windows:
.venv-rasa\Scripts\activate
# On macOS/Linux:
source .venv-rasa/bin/activate

# Start Rasa actions server
rasa run actions --actions actions --port 5055
```

### Terminal 4: Rasa Core Server

```bash
# Activate Rasa environment (same as Terminal 3)
# On Windows:
.venv-rasa\Scripts\activate
# On macOS/Linux:
source .venv-rasa/bin/activate

# Navigate to rasa directory
cd rasa

# Start Rasa server
rasa run --enable-api -p 5005 --endpoints endpoints.yml --credentials credentials.yml

# Rasa will run on: http://localhost:5005
```

### Step 5: Open Web Interface

1. Navigate to the `web/` directory
2. Open `index.html` in your web browser
3. The chat interface will connect to the Rasa server automatically

**Alternative:** Use a local web server:

```bash
# Navigate to web directory
cd web

# Using Python 3
python -m http.server 8080

# Then open: http://localhost:8080
```

## 💬 Usage Examples

Once all services are running, you can interact with the chatbot using these example phrases:

### Greeting
- "Hi"
- "Hello"
- "Good morning"

### Order Tracking
- "Where is order 1002?"
- "Track my order 1001"
- "What's the status of order 1003?"

### Order Rescheduling
- "Reschedule order 1002 to 2025-09-15"
- "Change delivery date for 1001 to 2025-10-01"
- "Move order 1003 to 2025-11-20"

### Inventory Checking
- "Check stock"
- "Do you have laptops?"
- "Is item3 available?"
- "Show me the inventory"

### Goodbye
- "Bye"
- "Thank you, goodbye"
- "See you later"

## 📚 API Documentation

### Rasa Webhook

**Endpoint:** `POST http://localhost:5005/webhooks/rest/webhook`

**Request:**
```json
{
  "sender": "user123",
  "message": "where is order 1002?"
}
```

**Response:**
```json
[
  {
    "recipient_id": "user123",
    "text": "✅ Order **1002** is currently *processing*.\n📦 Product: Charger (item2)\n📅 Expected delivery date: 29-08-2025."
  }
]
```

### Classifier Service

**Endpoint:** `POST http://localhost:8001/predict`

**Request:**
```json
{
  "text": "where is my order"
}
```

**Response:**
```json
{
  "intent": "track_order",
  "confidence": 0.89
}
```

### LLM Normalizer

**Endpoint:** `POST http://localhost:8002/normalize`

**Request:**
```json
{
  "text": "WHERE IS ORDER 1002???"
}
```

**Response:**
```json
{
  "normalized": "where is order 1002?"
}
```

## 🧪 Testing

### Run Unit Tests

```bash
# Install pytest in classifier environment
# On Windows:
.venv-classifier\Scripts\activate
# On macOS/Linux:
source .venv-classifier/bin/activate

pip install pytest
pytest tests/test_classifier.py

deactivate
```

### Run E2E Test Script

The project includes an automated end-to-end test script:

```bash
# Make script executable (macOS/Linux)
chmod +x scripts/e2e_test.sh

# Run E2E tests
./scripts/e2e_test.sh
```

### Manual Testing

1. Start all services as described above
2. Open the web interface
3. Test each conversation flow:
   - Greet → Track Order → Reschedule → Check Stock → Goodbye

## 🔧 Troubleshooting

### Common Issues

#### 1. "Model not found" Error
**Problem:** Classifier service returns model not found error.

**Solution:**
```bash
# Retrain the classifier model
source .venv-classifier/bin/activate  # or activate on Windows
python services/classifier/train_classifier.py
deactivate
```

#### 2. "Connection Refused" in Web Interface
**Problem:** Web interface can't connect to Rasa server.

**Solutions:**
- Ensure Rasa server is running on port 5005
- Check browser console for CORS errors
- Verify all 4 services are running

#### 3. Rasa Actions Not Working
**Problem:** Bot responds with default messages only.

**Solutions:**
- Ensure Rasa Actions server is running on port 5055
- Check `endpoints.yml` configuration
- Verify CSV files are in the correct `data/` directory

#### 4. Python Virtual Environment Issues
**Problem:** Virtual environments not activating properly.

**Solutions:**
```bash
# Recreate virtual environments
rm -rf .venv-*
python -m venv .venv-rasa
python -m venv .venv-classifier  
python -m venv .venv-llm

# Reinstall dependencies for each environment
```

#### 5. File Path Issues
**Problem:** CSV files not found errors in actions.

**Solution:**
- Ensure you're running from the project root directory
- Check that `data/orders.csv` and `data/inventory.csv` exist
- Update file paths in `rasa/actions.py` if needed

### Port Configuration

If you need to change ports, update these files:

- **Rasa Server Port (5005):** Change in `rasa run` command and `web/script.js`
- **Actions Server Port (5055):** Change in `rasa/endpoints.yml`
- **Classifier Service (8001):** Change in `services/classifier/app.py`
- **LLM Service (8002):** Change in `services/llm/app.py`

### Data Files

The system uses these CSV files in the `data/` directory:

- **`intents.csv`** - Training data for intent classification
- **`orders.csv`** - Order database (order_id, product_name, delivery_date, status)
- **`inventory.csv`** - Product inventory (item, quantity, price, display_name)
- **`test.csv`** - Sample test messages

## 📁 Project Structure

```
warehouse-chatbot/
├── data/                          # Data files
│   ├── intents.csv               # Training data for classifier
│   ├── inventory.csv             # Product inventory database  
│   ├── orders.csv                # Orders database
│   └── test.csv                  # Test messages
├── rasa/                         # Rasa chatbot configuration
│   ├── actions.py                # Custom Rasa actions
│   ├── config.yml                # Rasa pipeline configuration
│   ├── credentials.yml           # Channel configurations
│   ├── domain.yml                # Bot domain (intents, entities, responses)
│   ├── endpoints.yml             # External service endpoints
│   ├── requirements.txt          # Rasa dependencies
│   └── data/                     # Rasa training data
│       ├── nlu.yml               # Natural Language Understanding data
│       ├── rules.yml             # Conversation rules
│       └── stories.yml           # Conversation stories
├── services/                     # Microservices
│   ├── classifier/               # Intent classification service
│   │   ├── app.py                # FastAPI classifier application
│   │   ├── requirements.txt      # Classifier dependencies
│   │   └── train_classifier.py   # Model training script
│   └── llm/                      # LLM normalization service
│       ├── app.py                # FastAPI LLM application
│       └── requirements.txt      # LLM dependencies
├── web/                          # Web interface
│   ├── index.html                # Main HTML page
│   ├── script.js                 # JavaScript functionality
│   └── style.css                 # CSS styling
├── tests/                        # Test files
│   ├── test_classifier.py        # Classifier tests
│   └── test_e2e.py               # End-to-end tests
├── scripts/                      # Utility scripts
│   └── e2e_test.sh               # Automated E2E testing
├── LICENSE                       # MIT license
└── README.md                     # This file
```

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Ensure all dependencies are correctly installed
3. Verify all services are running on their respective ports
4. Check the terminal output for error messages

For additional help, please create an issue in the repository with:
- Your operating system
- Python version
- Full error messages
- Steps to reproduce the issue

---

**Happy Chatting! 🤖✨**
