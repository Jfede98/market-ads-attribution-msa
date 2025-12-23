# Market Ads Attribution Microservice

## 🚀 Overview

A Python/FastAPI microservice designed for digital advertising campaign attribution. Captures clicks from Meta Ads campaigns, validates and normalizes tracking parameters using configurable MongoDB templates, registers click events for traceability, and orchestrates intelligent redirection to WhatsApp Business.

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI
- **Database**: MongoDB (templates), Redis (session storage)
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker, Docker Compose
- **Architecture**: Modular microservice following enterprise standards

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Meta Ads      │───▶│  Attribution MSA │───▶│   WhatsApp      │
│   Campaign      │    │                  │    │   Business      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Session Store  │
                       │   (Redis/Cache)  │
                       └──────────────────┘
```

## 📋 Features

- **Campaign Attribution**: Captures fbclid, campaign_id, adset_id, ad_id from Meta Ads
- **Dynamic Validation**: Configurable parameter validation using MongoDB templates
- **Session Management**: Registers click events for precise ROI tracking
- **Smart Redirection**: Clean WhatsApp Business integration
- **API Documentation**: Complete Swagger/OpenAPI documentation
- **Error Handling**: Robust error management with fallback mechanisms
- **Docker Ready**: Multi-environment Docker configuration

## 🚦 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB
- Redis (or session storage service)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Jfede98/market-ads-attribution-msa.git
cd market-ads-attribution-msa
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the service**
```bash
python -m app.main
```

### Docker Deployment

```bash
# Development
docker build -f setup/dockerfile/dockerfile_dev -t market-ads-attribution-msa .

# Production
docker build -f setup/dockerfile/dockerfile_prod -t market-ads-attribution-msa .

# Run with Docker Compose
docker-compose up -d
```

## 📖 API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:2217/market-ads-attribution-api/v1/ui`
- **ReDoc**: `http://localhost:2217/market-ads-attribution-api/v1/redoc`

## 🔗 Example Usage

### Health Check
```bash
curl http://localhost:2217/market-ads-attribution-api/v1/health
```

### Meta Ads Redirect
```bash
# Basic example
http://localhost:2217/market-ads-attribution-api/v1/w/redirect?fbclid=IwAR1234567890&campaign_id=1234&adset_id=5678&ad_id=9012

# With UTM parameters
http://localhost:2217/market-ads-attribution-api/v1/w/redirect?fbclid=IwAR1234567890&campaign_id=1234&adset_id=5678&ad_id=9012&utm_source=facebook&utm_medium=cpc
```

## 📁 Project Structure

```
market-ads-attribution-msa/
├── app/
│   ├── api/          # REST endpoints
│   ├── models/       # Data models
│   ├── services/     # Business logic
│   ├── utils/        # Utilities
│   ├── config.py     # Configuration
│   └── main.py       # Main application
├── setup/
│   └── dockerfile/   # Docker configurations
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🔧 Configuration

Key environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `PORT` | Server port | `2217` |
| `CACHING_SERVICE_URL` | Session service URL | `https://api.example.com/v1` |
| `WHATSAPP_NUMBER` | Business WhatsApp number | `1234567890` |
| `MONGODB_URL` | MongoDB connection string | `mongodb://user:pass@host:port/db` |

## 🎯 Business Value

- **ROI Tracking**: Precise campaign attribution for marketing optimization
- **Lead Conversion**: Seamless user journey from ad click to WhatsApp engagement
- **Scalability**: Microservice architecture ready for multi-platform expansion
- **Maintainability**: Clean code following enterprise standards

## 🚀 Future Enhancements

- Google Ads integration
- TikTok Ads support
- Advanced analytics dashboard
- A/B testing capabilities

---

**Built with ❤️ using Python & FastAPI**