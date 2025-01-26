# AI Chat Tool

A simple AI-powered chatbot application using **Flask (backend)** and **React (frontend)** that supports OpenAI (GPT) and Anthropic (Claude) models.

## 🚀 Features
- Supports multiple AI models from OpenAI and Anthropic.
- Clean and user-friendly UI with real-time response.
- Fully functional backend API with error handling.

---

## 📦 Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/<your-username>/ai-chat-tool.git
cd ai-chat-tool
```

### **2️⃣ Backend Setup**
#### **Install Dependencies**
```sh
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### **Set Up Environment Variables**
Create a `.env` file in the `backend` directory and add:
```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

#### **Run the Backend**
```sh
python app.py
```

---

### **3️⃣ Frontend Setup**
#### **Install Dependencies**
```sh
cd frontend
npm install
```

#### **Start the Frontend**
```sh
npm run dev
```

---

## 🎯 **Usage**
1. Open your browser and go to **`http://127.0.0.1:5173`**.
2. Select a model from the dropdown.
3. Enter a **System Prompt** (optional).
4. Type a **User Input** and click **Submit**.
5. The AI response will be displayed below.

---

## 🛠 **API Endpoints**
| Method | Endpoint    | Description |
|--------|------------|-------------|
| GET    | `/`        | Returns API status |
| GET    | `/models`  | Fetches available AI models |
| POST   | `/chat`    | Processes AI chat requests |