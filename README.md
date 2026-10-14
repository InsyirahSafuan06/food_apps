# GreenFork Food App (Python + HTML + CSS)

A responsive food-ordering demo inspired by the provided Figma Food Apps splash screen (forest green `#185d0d`, cream `#efe9d8`, berry accents, rounded food photography, and bold mono headings).

## Features
- Figma-inspired welcome / splash screen
- Menu with category filters and search
- Add items to a session-based basket
- Update quantities and remove items
- Checkout form and order confirmation screen
- Responsive layout for desktop and mobile

## Run on Windows
1. Install Python 3.10 or later.
2. Extract this folder.
3. Open Command Prompt / PowerShell inside the folder.
4. Install Flask:
   ```powershell
   py -m pip install -r requirements.txt
   ```
5. Start the app:
   ```powershell
   py app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

Food photos load from Unsplash, and the font loads from Google Fonts, so those visual elements require internet access. Checkout is a demonstration only: it does not charge a payment method or save orders to a permanent database. Change `app.secret_key` before deployment and do not use Flask debug mode in production.
