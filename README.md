# AI Life Management System (Ai-LMS)

A comprehensive AI-powered platform for managing all aspects of life including finances, health, tasks, investments, reminders, emails, and life balance.

## Features

- **Finance Module**: Track transactions, analyze spending patterns, create budgets, receive budget recommendations, and manage auto-save and auto-invest features.

- **Health Module**: Monitor sleep, exercise, meals, stress, and run health experiments to track what works for you.

- **Task Management**: Organize tasks with automatic scheduling, smart prioritization, and delegation features.

- **Portfolio Manager**: Track investments, analyze portfolio allocation, and receive investment recommendations.

- **Memory Assistant**: Manage reminders, events, contacts, birthdays, gift ideas, and receive personalized news briefings.

- **Email and Call Handler**: Auto-categorize communications, draft email responses, and transcribe calls.

- **Life Balancer**: Track balance across different life areas, manage goals, schedule "me time", and predict burnout risk.

## Project Structure

```
ai-lms/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── database.py                # Database connection and session management
│   ├── models.py                  # SQLAlchemy database models
│   │
│   ├── finance_module.py          # Finance tracking and budgeting functionality
│   ├── health_module.py           # Health tracking and analytics
│   ├── task_module.py             # Task management and scheduling
│   ├── portfolio_module.py        # Investment portfolio management
│   │
│   ├── ai_engine/                 # AI-powered analysis and recommendations
│   │   ├── __init__.py
│   │   ├── common.py              # Shared AI utilities
│   │   ├── finance_ai.py          # Financial analysis and recommendations
│   │   └── ... (more AI modules)
│   │
│   ├── integrations/              # External service integrations
│       ├── __init__.py
│       ├── market_service.py      # Financial market data integration
│       └── ... (more integration services)
│
├── tests/                         # Unit and integration tests
│
├── frontend/                      # Frontend application (to be implemented)
│
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore file
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration for container builds
└── docker-compose.yml            # Docker configuration for deployment
```

## Installation and Setup

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/markthepioneer/Ai-LMS-Project.git
   cd Ai-LMS-Project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration values
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API at `http://localhost:8000` and the API documentation at `http://localhost:8000/docs`

### Docker Deployment

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

2. Access the API at `http://localhost:80` and the API documentation at `http://localhost:80/docs`

## API Documentation

The API is built with FastAPI and includes automatic documentation:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any improvements or bug fixes.

## License

This project is open-source and available under the MIT License.
