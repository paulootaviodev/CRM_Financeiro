# CRM Financeiro

**Accelerate the development of a CRM for financial institutions.**

This project provides a robust foundation for developers looking to build a **Customer Relationship Management (CRM) system** tailored for financial institutions. It includes essential features to streamline client management, loan proposals, and sales tracking.

---

## Features

| Feature                | Description                                      |
|------------------------|--------------------------------------------------|
| **Landing Page**       | Simulate credit offers for potential clients.    |
| **Blog**               | Publish updates, news, and financial insights.   |
| **Sales Dashboard**    | Monitor sales performance and key metrics.      |
| **Client Management**  | Register and manage client profiles.            |
| **Loan Proposal Management** | Create, review, and track loan proposals. |
| **Email Confirmation** | Send loan proposal confirmations via email. |
| **Installment Management** | Track and manage loan installments.          |
| **Search & Filtering** | Advanced search and filtering across all sections. |
| **Encrypted Field Search** | Uses `django-eose` to optimize searches in encrypted fields. |
| **User & Permissions** | Role-based access control and user management. |

---

## Getting Started

### Prerequisites
- Python 3.10+
- Django 5.0+
- MySQL (recommended)
- Redis

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/paulootaviodev/CRM_Financeiro.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your `.env` file with database and email settings.
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Running Tests
Please make sure you have Google Chrome installed on your system before running the tests. This is required for Selenium to work properly.

Alternatively, you can use a different browser, but you will need to update the configuration settings in the tests to match your chosen browser.

---

## Customization Notes

### Cloudflare Turnstile
If you are **not** using Cloudflare Turnstile for CAPTCHA validation, comment out or remove the following code in `landing_page/views.py`:
```python
# CAPTCHA validation using Cloudflare Turnstile
turnstile_response = request.POST.get("cf-turnstile-response", "")
if not validate_turnstile(turnstile_response):
    return JsonResponse({"success": False}, status=400)
```

### Credit Simulation API
If you do **not** have a credit simulation API, comment out the following code and adjust the variables accordingly:
```python
# Make the API request
response = send_data_to_api(payload, API_URL)
```

---

## Contributing
This project is a work in progress, and contributions are welcome! Feel free to open issues or submit pull requests.

---

## License
MIT © 2025 [Paulo Otávio Castoldi](https://github.com/paulootaviodev)
