# Domain-Based Authentication System (Kiogo Internship Assignment)

A secure, single-page login system with domain-based email restrictions and OTP verification.

Checkout the [live link](https://domain-login-kiogo.vercel.app) (Currently gmail.com is the only allowed domain)

## Features

- **Domain-Based Email Restriction**: Only users with emails from approved domains can register and log in
- **Email Verification**: One-time verification codes sent to users' emails
- **Passwordless Authentication**: Users authenticate using OTP codes rather than passwords
- **JWT-Based Authorization**: Secure token-based authentication system
- **React Frontend**: Clean, responsive UI built with React and Tailwind CSS

## Project Structure

The project consists of two main parts:

### Backend (Django)

- REST API built with Django REST Framework
- Custom JWT authentication
- Email OTP generation and verification
- Domain restriction management

### Frontend (React)

- Single-page application
- Responsive design with Tailwind CSS
- JWT token management
- Email and OTP verification flows

## Setup Instructions

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/singhchanmeet/KioGo-Assignment/
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

4. Run migrations:
```bash
python manage.py migrate
```

5. Add allowed domains:
```bash
python manage.py shell
```
```python
from api.models import AllowedDomains
AllowedDomains.objects.create(domain="example.com")
# Add more domains as needed
exit()
```

6. Run the development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## API Endpoints

- `POST /api/register`: Register or update a user with email (sends OTP)
- `POST /api/token/`: Verify OTP and obtain JWT tokens
- `POST /api/token/refresh/`: Refresh an expired access token
- `GET /api/user-details`: Get authenticated user details

## Environment Configuration

Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

## Usage Flow

1. User enters their email on the login page
2. If the domain is allowed, an OTP is sent to the email
3. User enters the OTP code
4. Upon successful verification, JWT tokens are issued
5. User is redirected to the dashboard
6. Access token is automatically refreshed when needed

## Development

### Adding New Allowed Domains

To add a new allowed domain:

```python
from api.models import AllowedDomains
AllowedDomains.objects.create(domain="newdomain.com")
```

### Customizing OTP Settings

OTP settings can be adjusted in `api/views.py`:

- OTP length and character set in the `generate_otp()` function
- Expiry time when creating/updating users

## Technologies

- **Backend**: Django, Django REST Framework, PyJWT
- **Frontend**: React, React Router, Axios, Tailwind CSS
- **Authentication**: Custom JWT implementation
- **Communication**: RESTful API
