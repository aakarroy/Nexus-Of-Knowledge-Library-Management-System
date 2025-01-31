# Nexus of Knowledge - Library Management System

## Introduction

Nexus of Knowledge is a **Library Management System** designed using **Tkinter (Python GUI)** with **MySQL** as the database. It provides an intuitive user interface to manage books, users, and transactions efficiently. The system supports, email notifications, and database connectivity.

## Features

- **User-friendly GUI** with Tkinter\
  Provides an interactive and visually appealing interface for easy navigation and usage.

- **MySQL Database Integration** for efficient book & user management\
  Ensures reliable storage and retrieval of book records, user details, and transactions.
  
- **Email Notifications** using Gmail SMTP\
  Automatically sends email confirmations and reminders for book issuances and due dates.

- **Book Issuing & Returning System**\
  Allows users to borrow books with an automated system for tracking due dates and penalties.

- **Secure Database Connection**\
  Implements a secure connection to prevent unauthorized access and ensure data integrity.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- MySQL Server
- Required Python Libraries:
  ```bash
  pip install mysql-connector-python tk
  ```

## Setup & Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/aakarroy/Nexus-Of-Knowledge-Library-Management-System.git
   ```
2. Update **database credentials** in the script:
   ```python
   con = c.connect(host='localhost', user='root', password='your_password', database='library')
   ```
3. Run the script:
   ```bash
   python "Library Management UI.py"
   ```

## How It Works

- The system allows librarians to add, issue, and return books.
- Users receive email notifications when books are issued or due.
- The database manages book records and user details.

## Email Configuration

To enable email notifications via Gmail:

1. Enable **Less Secure Apps** in your Gmail account.
2. Update your Gmail credentials in the script:
   ```python
   sender_email = "your-email@gmail.com"
   app_password = "your-app-password"
   ```
## Contributions

Feel free to fork this repository, create a new branch, and submit pull requests!

