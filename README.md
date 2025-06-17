# Senuoy Store - Online E-commerce Platform

An online store built with Django, featuring user authentication, shopping cart, order management, Stripe payment integration, Celery for email notifications, a loyalty system, multilingual support, newsletter, coupons, and more.

---

## Features

- ✅ User authentication (sign up, login, logout) with email activation for account verification  
- 🛒 Shopping cart & order management  
- 💳 Stripe integration for secure online payments  
- ✉️ Email notifications using Celery + RabbitMQ  
- 🎁 Loyalty system (earn points, redeem rewards)  
- 🌍 Multilingual support (English, Arabic, French)  
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

   ```bash
   git clone https://github.com/Senuoy-16/Ecommerce-Senuoy.git
   cd Ecommerce-Senuoy/src
