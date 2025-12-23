# Microservicio Market Ads Attribution 

## 🚀 Resumen

Microservicio desarrollado en Python/FastApi especificamente para poder ser parte de la campaña de publicidad llamada atrribution. Captura los clics que vienen desde las campañas de Meta Ads, valida y normaliza los parametros de trackeo usando plantillas de MongoDB configurables, luego registra eventos clics para su trazabilidad para finalmente redirigir al usuario al chatbot de WhatsApp. 

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI
- **Base de datos**: MongoDB (templates), Redis (session storage)
- **Documentación**: Swagger/OpenAPI
- **Container**: Docker, Docker Compose
- **Arquitectura**: Microservicio modular siguiendo los lineamientos de la empresa

## 🏗️ Arquitectura

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

- **Campaign Attribution**: Captura fbclid, campaign_id, adset_id, ad_id de Meta Ads
- **Dynamic Validation**: Parametro de validacion configurable usando plantillas de MongoDB
- **Session Management**: Registra eventos clics para trackeo ROI de forma precisa
- **Smart Redirection**: Integracion a WhatsApp Business
- **API Documentation**: Documentacion completa en Swagger/OpenAPI
- **Error Handling**: Manejo de errores con mecanicas fallback
- **Docker Ready**: Configuracion multi-environment en Docker 

## 🚦 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB
- Redis (or session storage service)

### Instalacion

1. **Clonar el repository**
```bash
git clone https://github.com/Jfede98/market-ads-attribution-msa.git
cd market-ads-attribution-msa
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar ambiente**
```bash
cp .env.example .env
# Edita .env con tu configuracion
```

4. **Corre el servicio**
```bash
python -m app.main
```

### Docker Deployment

```bash
# Dev
docker build -f setup/dockerfile/dockerfile_dev -t market-ads-attribution-msa .

# Produccion
docker build -f setup/dockerfile/dockerfile_prod -t market-ads-attribution-msa .

# Corre con Docker Compose
docker-compose up -d
```

## 📖 Documentacion de API

Una vez que este corriendo, acceder a la documentacion interactiva del API:

- **Swagger UI**: `http://localhost:2217/market-ads-attribution-api/v1/ui`
- **ReDoc**: `http://localhost:2217/market-ads-attribution-api/v1/redoc`

## 🔗 Ejemplo de Uso

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

## 📁 Estructura del Proyecto 

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

## 🔧 Configuracion

Key environment variables:

| Variable | Descripcion | Ejemplo |
|----------|-------------|---------|
| `PORT` | Server port | `2217` |
| `CACHING_SERVICE_URL` | Session service URL | `https://api.example.com/v1` |
| `WHATSAPP_NUMBER` | Business WhatsApp number | `1234567890` |
| `MONGODB_URL` | MongoDB connection string | `mongodb://user:pass@host:port/db` |

## 🎯 Valor de Negocio

- **ROI Tracking**: Servicio de attribution para optimizacion de campaña de marketing
- **Conversion de Leads**: Journey de usuario desde el clic a un ad hasta el contacto por WhatsApp de forma organica
- **Escalabilidad**: Arquitectura del microservicio lista para expansion multiplataforma
- **Mantenibilidad**: Codigo limpio siguiendo estadares empresariales

## 🚀 Futuras Mejoras

- Integracion con Google Ads
- Soporte de TikTok Ads
- Dashboard para analitica
- Capacidad de testing A/B

---

**Built with ❤️ using Python & FastAPI**
