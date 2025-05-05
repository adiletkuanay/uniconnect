# UniConnect Kazakhstan

A comprehensive university application platform for Kazakhstan, similar to Common App, designed to streamline the university application process.

## Features

- User Registration & Authentication
- Profile & Dashboard Management
- University & Program Listings
- Application Form & Document Upload
- Recommendation Letters & Essays
- Admin & University Dashboards
- Real-time Application Tracking
- AI-Powered University Recommendations
- One-Click Multiple Applications
- Scholarship & Financial Aid Matching

## Installation

1. Clone the repository
2. Create a virtual environment:
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
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

- `uniconnect/` - Main project configuration
- `users/` - User authentication and profile management
- `universities/` - University and program listings
- `applications/` - Application form and document management
- `dashboard/` - User and admin dashboards
- `core/` - Common utilities and shared functionality

## Development Plan

The project follows a 9-week development plan, with each week focusing on specific features:

- Week 3: User Authentication & Profile Management
- Week 4: Application Form Submission
- Week 5: Document Upload & Verification
- Week 6: Smart Autofill for Application Forms
- Week 7: Real-Time Application Status Tracking
- Week 8: AI-Powered University Recommendations
- Week 9: One-Click Apply to Multiple Universities
- Week 10: Scholarship & Financial Aid Matching
- Week 11: Personalized Dashboard with Deadlines & Reminders

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details 