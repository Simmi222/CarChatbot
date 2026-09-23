#  AI Car Mechanic Chatbot

A full-stack AI-powered car mechanic chatbot that helps users troubleshoot car problems, analyze vehicle images, generate diagnosis, and book mechanic services.

##  Architecture

React (Vite) → Django REST API → SQLite + Gemini AI

### Frontend
- React + Vite
- Axios
- Chat interface
- Image upload
- Diagnosis display
- Mechanic booking

### run frontend
- cd Frontend
- npm install
- npm run dev

### Backend
- Django
- Django REST Framework
- SQLite
- Gemini AI / Vision
- Modular apps for Chat, Media, Diagnosis and Booking

## ✨ Features

-  Car troubleshooting chatbot
-  Gemini AI fallback for unknown/complex car questions
-  Vehicle image analysis using Gemini Vision
-  Diagnosis with severity and recommendations
-  Mechanic booking
-  Conversation history and context
-  Rejects unrelated questions

##  APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/chat/` | Chat with mechanic |
| POST | `/api/upload/` | Upload media |
| POST | `/api/diagnosis/` | Generate diagnosis |
| POST | `/api/booking/` | Create booking |
| GET | `/api/booking/{id}/` | Get booking |

##  Tech Stack

- **Frontend:** React, Vite, Axios
- **Backend:** Python, Django, DRF
- **Database:** SQLite
- **AI:** Google Gemini
- **Deployment:** Vercel + AWS

## ⚙️ Local Setup

### Backend

```bash
cd Backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver