# Senuoy Store - Online E-commerce Platform

An online store built with Django, featuring user authentication, shopping cart, order management, Stripe payment integration, Celery for email notifications, a loyalty system, multilingual support, newsletter, coupons, and more.

---

## Features

- ✅ User authentication (sign up, login, logout) with email activation for account verification  
- 🛒 Shopping cart & order management  
- 💳 Stripe integration for secure online payments  
- ✉️ Email notifications using Celery + RabbitMQ  
- 🎁 Loyalty system (earn points, redeem rewards)  
- 🌍 Multilingual support (French, Arabic)  
- 📰 Newsletter subscription  
- 🎟️ Coupons and discounts  
- 🔐 Customized Django admin panel  
  - Signals to send welcome emails on account creation  
  - Hidden admin panel for regular users  
- 📄 User account dashboard  
  - Update profile info  
  - View order history with payment status and ordered products 

---

## Getting Started

### Prerequisites

  - Python 3.10+  
  - Docker (for RabbitMQ)  
  - Stripe account for payment processing  

### Installation


1. **Clone the repository**
     ```
     git clone https://github.com/Senuoy-16/Ecommerce-Senuoy.git
     cd Ecommerce-Senuoy/src
     ```

2. **Create and activate a virtual environment**
    ```
    python -m venv env
    env\Scripts\activate      # Windows
    source env/bin/activate
    ```


3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Setup RabbitMQ with Docker**
    ```
    docker pull rabbitmq
    docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
    ```

5. **Configure Stripe**
    - Create a Stripe account at stripe.com
  
    - Obtain your API keys (publishable and secret keys)
  
    - Setup webhooks in Stripe dashboard to your server URL (e.g., /stripe/webhook/)
  
    - Add your Stripe keys and webhook secret to your .env file
  
      ```
      stripe login
      stripe listen forward stripe listen --forward-to localhost:8000/stripe/webhook/
      ```


6. **Running Celery**

    Start Celery worker
        ```
        celery -A src worker -l info --pool=solo
        ```
    Make sure RabbitMQ is running before starting Celery.

7. **run the migration**
    ```
    bash
    python manage.py makemigrations
    python manage.py migrate
    ```

9. **run the sever**
     ```
     python manage.py runserver
     ```

10. **License**

    MIT License © 2025 Senuoy

