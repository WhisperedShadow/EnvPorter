# EnvPorter

EnvPorter is a simple tool that allows users to log in, store API keys, and export them as `.env` files for various technologies like React, Vite, and more. It helps developers manage environment variables efficiently.

## 🚀 Features

- 🔐 **User Authentication** – Secure login and access control
- 📦 **Store API Keys** – Save environment variables securely in a database
- 📤 **Export `.env` Files** – Generate `.env` files for different frameworks
- 🔄 **Manage Keys Easily** – Add, update, or delete stored keys

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Flask
- **Database:** MySQL
- **Authentication:** Flask-Login
- **Deployment:** Vercel 

## 📄 Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/whisperedshadow/envporter.git
   cd envporter
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt 
   ```
3. Set up environment variables:
   ```sh
   SQL_LINK=your_database_url
   MAIL_API_KEY=your_mailjet_api_key
   MAIL_SECRET_KEY=your_mailjet_secret_key
   FROM_MAIL=your_email
   TO_MAIL=recipient_email
   ```
   Fill in the required values.
4. Start the development server:
   ```sh
   python app.py  
   ```
   Or use:
   ```sh
   flask run  
   ```

## 📦 Exporting Environment Variables

1. **Add API keys** in the dashboard.
2. **Select technology** (React, Vite, etc.).
3. **Download the `.env` file** with properly formatted variables.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## 📧 Contact
For any queries, reach out to [My Portfolio](https://durai-pon-singh.me).
