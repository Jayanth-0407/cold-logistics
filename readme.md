# 🚚 AI-Powered Cold Chain Logistics System

<img width="399" height="268" alt="image" src="https://github.com/user-attachments/assets/6e7bb3f8-f11d-43d3-b72b-e517f5a369a7" />





An enterprise-grade, microservices-based web application designed to optimize and secure cold chain logistics. This system uses machine learning to analyze geographical routes, fetch real-time weather data at route checkpoints, and predict environmental risks (Safe/Danger) for sensitive cargo like vaccines, milk, and electronics.

## 🏗 Architecture

This project is built using a decoupled microservices architecture, containerized with Docker, and deployed via a fully automated CI/CD pipeline.

* **Frontend (UI):** Streamlit (Hosted on Streamlit Community Cloud)
* **Backend (API):** FastAPI (Containerized via Docker, hosted on Microsoft Azure)
* **Machine Learning:** Scikit-Learn (Random Forest Classifier)
* **External APIs:** OpenRouteService (Routing), OpenWeatherMap (Weather Data)
* **DevOps / CI/CD:** GitHub Actions, Azure Container Registry (ACR), Azure App Service

## ✨ Key Features
* **Interactive Route Mapping:** Fetches highly accurate highway routes between Indian cities using OpenRouteService.
* **Real-Time Weather Checkpoints:** Samples geographical coordinates along the route and fetches live temperature and humidity data using OpenWeatherMap.
* **AI Risk Assessment:** Passes checkpoint data into a trained Scikit-Learn model to predict if the current weather poses a risk to the specific `cargo_type`.
* **Automated CI/CD Pipeline:** Pushes to the `main` branch trigger a GitHub Action that automatically builds a new Docker image, pushes it to Azure Container Registry, and triggers a webhook to restart the live Azure App Service with zero manual downtime.

## 💻 Tech Stack
* **Language:** Python 3.11.9
* **Frontend Framework:** Streamlit, Pandas
* **Backend Framework:** FastAPI, Uvicorn, Pydantic
* **Cloud Infrastructure:** Microsoft Azure App Service (Linux), Azure Container Registry
* **Containerization:** Docker

**1. Clone the repository**
```bash
git clone https://github.com/Jayanth-0407/cold-logistics.git
cd cold-logistics
