# 🛡️ Mail Inspector

This is a **Flask-based web application** that allows users to upload `.eml` email files and analyze their phishing risk using **Groq AI API**. The AI assigns a **phishing score (0-10)** and provides a brief **overview** along with a **detailed explanation**.

---

## 📂 Directory Structure

```
/phishing-analyzer
│── /static
│   ├── /css       # CSS files (if needed)
│   ├── /js        # JavaScript files
│   │   └── script.js  # Handles UI updates and file upload logic
│── /templates
│   └── index.html  # Main UI template for file upload & results
│── /uploads        # Stores uploaded .eml files
│── config.ini      # Stores API Key
│── main.py         # Flask backend application
│── requirements.txt # Dependencies list
│── README.md       # Project documentation
```

---

## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/krishnagopaljha/mailinspector
cd phishing-analyzer
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

---

## 🔑 Getting the Groq API Key

To use the **Groq AI API**, follow these steps:

1. Go to **[Groq AI Platform](https://console.groq.com/)** and **sign up/login**.
2. Navigate to **API Keys** section.
3. **Generate a new API key**.
4. Copy the API key and paste it into **config.ini**.

---

## ⚙️ Configuring API Key

Create a file named **config.ini** in the project root and add:
```ini
[groq]
api_key = YOUR_GROQ_API_KEY_HERE
```

Replace `YOUR_GROQ_API_KEY_HERE` with the actual API key.

---

## 🚀 Running the Application

### **1️⃣ Start Flask Server**
```sh
python main.py
```

### **2️⃣ Access the App**
Open your browser and visit:
```
http://0.0.0.0:5000
```

This allows **network access**, so other devices on the same network can access the tool.


