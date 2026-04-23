# Simple IoT Project

## Description
Simple IoT system with Flask, MQTT, and PostgreSQL

## ER Diagram
![ER Diagram](docs/digramDB.png)

## API List
### Authentication
- POST /login - Login and get JWT token

### Users
- GET /users - Get all users
- POST /users - Create new user
- PUT /users/{id} - Update user
- DELETE /users/{id} - Delete user

### Devices
- GET /devices - Get all devices
- POST /devices - Create new device
- PUT /devices/{id} - Update device
- DELETE /devices/{id} - Delete device

### Telemetry
- GET /telemetry - Get all telemetry data
- GET /telemetry?device_id= - Get telemetry for specific device

## System Diagram
![System Diagram](docs/SystemDigram.png)

## How to Run

Follow these steps to run the project:

### Requirements
- Docker Desktop
- Python 3.10+
- pip

---

### 1. Start Docker Services
This will run PostgreSQL, MQTT Broker, and Telemetry Service.
```bash
cd service
docker compose up --build
```

### 2. Run API Server
```bash
cd api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 3. Run Device Emulator
```bash
cd device_emulatour
docker build -t device_emu .
docker run --env-file .env --network service_default device_emu
```

### 4. Open Application
```text
http://localhost:5000
```

### 5. Login Example
Email: admin@test.com
Password: 123456

