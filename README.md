# Pizza Planet

Pizza Planet is a full-stack web application built as a technical exercise for the Full Stack Developer role at StrongMind. The application simulates a real-world environment where pizza store owners can manage available toppings and pizza chefs can create and manage pizzas using those toppings.

## Overview

Pizza Planet is designed with self-organized work principles in mind. The application supports two distinct user roles:

- **Owner:**  
  Manages the list of available toppings. Owners can add, update, and delete toppings. Duplicate toppings are not allowed.

- **Chef:**  
  Creates and manages pizzas using the available toppings. Chefs can create, update, and delete pizzas and assign toppings via a checkbox interface.

## Features

### Manage Toppings (Owner)
- View a list of available toppings.
- Add new toppings.
- Edit existing toppings.
- Delete toppings.
- Prevent duplicate entries.

### Manage Pizzas (Chef)
- View a list of pizzas along with their toppings.
- Create new pizzas by selecting available toppings from a dropdown with checkboxes.
- Update existing pizzas (including topping selections).
- Delete pizzas.
- Prevent duplicate pizza names.

## Technology Stack

- **Backend:** Python, Flask, SQLAlchemy  
- **Frontend:** Tailwind CSS  
- **Authentication:** Flask-Login  
- **WSGI Server:** Gunicorn  
- **Deployment:** Heroku

## Installation

### Prerequisites
- Python 3.10 (or later)
- Git
- Virtual environment (e.g., `venv`)

### Steps to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tjf2015/PizzaPlanet.git
   cd PizzaPlanet
