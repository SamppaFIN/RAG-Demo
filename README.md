# 🍭 AI Candy Store - Interactive RAG Demo

*[Suomi](#finnish-version) | [English](#english-version)*

---

## English Version

### 🎯 Overview

Welcome to the **AI Candy Store** - an interactive, educational demonstration of **Retrieval-Augmented Generation (RAG)** that makes learning about AI both fun and visually engaging! 

This project walks users through each step of the RAG pipeline using a playful candy store theme, complete with:
- ✨ **Step-by-step RAG visualization** with beautiful animations
- 🌍 **Bilingual support** (English 🇬🇧 & Finnish 🇫🇮)
- 🌙 **Dark/Light mode** with smooth transitions
- 📱 **Responsive design** for desktop and mobile
- 🍬 **Real RAG implementation** using vector databases and AI

### 🏗️ Architecture

```
📁 Project Structure
├── 🔧 backend/          # FastAPI server with RAG logic
│   ├── main.py          # API endpoints
│   ├── rag_service.py   # RAG pipeline implementation
│   └── requirements.txt # Python dependencies
├── 🎨 frontend/         # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── utils/       # Utilities & translations
│   │   └── App.tsx      # Main application
│   └── package.json     # Node.js dependencies
└── 📖 README.md         # This file
```

### 🚀 Quick Start

#### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional)
# Copy .env.example to .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here (optional - fallback responses provided)

# Start the FastAPI server
python main.py
```

The backend will be available at `http://localhost:8000`

#### 2. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 🎮 How to Use

1. **Open your browser** to `http://localhost:3000`
2. **Choose your language** (English/Finnish) and theme (Light/Dark)
3. **Ask a question** about candies (e.g., "What's the sweetest candy?")
4. **Watch the magic happen** as the system:
   - 🔄 Processes your query
   - 🧠 Converts it to vector embeddings
   - 🔍 Searches the candy database
   - 📝 Prepares context for AI
   - ✨ Generates your personalized answer
5. **Explore the candy collection** and try different questions!

### 🛠️ Technical Features

#### Backend (FastAPI + Python)
- **FastAPI** for high-performance async API
- **ChromaDB** for vector storage and similarity search
- **Sentence Transformers** for text embeddings
- **OpenAI API** integration (with fallback responses)
- **Structured logging** and error handling

#### Frontend (React + TypeScript)
- **React 18** with TypeScript for type safety
- **Framer Motion** for smooth animations
- **Tailwind CSS** for modern styling
- **Responsive design** with mobile-first approach
- **Accessibility features** (keyboard navigation, screen reader support)

### 🌟 RAG Pipeline Explained

Each step is visualized with real-time animations:

1. **Query Processing** 🔄
   - User input sanitization and preparation
   - Language detection and normalization

2. **Vector Embedding** 🧠
   - Text-to-vector conversion using Sentence Transformers
   - 384-dimensional embeddings for semantic understanding

3. **Vector Search** 🔍
   - Similarity search through candy database
   - Top-K retrieval with confidence scores

4. **Context Preparation** 📝
   - Relevant context assembly from search results
   - Structured data formatting for AI consumption

5. **AI Generation** ✨
   - LLM-powered response generation
   - Context-aware answers with personality

### 🎨 Customization

#### Adding New Candies
Edit the candy data in `backend/rag_service.py`:

```python
self.candies_data = [
    {
        "id": "new_candy",
        "name": "Your Candy Name",
        "name_fi": "Karkkisi Nimi",
        "description": "Description in English",
        "description_fi": "Kuvaus suomeksi",
        # ... other properties
    }
]
```

#### Theme Customization
Modify colors in `frontend/tailwind.config.js`:

```javascript
colors: {
  candy: {
    pink: '#FF6B9D',    // Primary accent
    blue: '#4ECDC4',    // Secondary accent
    // ... add your colors
  }
}
```

### 🌍 Internationalization

The app supports English and Finnish out of the box. To add more languages:

1. Add translations to `frontend/src/utils/translations.ts`
2. Update the language selector in `App.tsx`
3. Add backend translations in `rag_service.py`

### 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### 📦 Deployment

#### Using Docker
```bash
# Build and run with Docker Compose
docker-compose up --build
```

#### Manual Deployment
1. Build frontend: `npm run build`
2. Serve static files with FastAPI
3. Deploy to your preferred platform (Vercel, Heroku, AWS, etc.)

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- **OpenAI** for GPT models and embeddings
- **Hugging Face** for Sentence Transformers
- **Framer Motion** for beautiful animations
- **Tailwind CSS** for utility-first styling
- **ChromaDB** for vector database functionality

---

## Finnish Version

### 🎯 Katsaus

Tervetuloa **AI Karkkikauppaan** - interaktiiviseen, opettavaiseen **Retrieval-Augmented Generation (RAG)** -demonstraatioon, joka tekee AI:n oppimisesta hauskaa ja visuaalisesti kiinnostavaa!

Tämä projekti opastaa käyttäjiä jokaisen RAG-putken vaiheen läpi leikkisän karkkikauppa-teeman avulla:
- ✨ **Vaiheittainen RAG-visualisointi** kauniilla animaatioilla
- 🌍 **Kaksikielinen tuki** (englanti 🇬🇧 & suomi 🇫🇮)
- 🌙 **Tumma/Vaalea tila** sujuvilla siirtymillä
- 📱 **Responsiivinen suunnittelu** työpöydälle ja mobiilille
- 🍬 **Todellinen RAG-toteutus** vektoritietokantojen ja AI:n avulla

### 🚀 Pika-aloitus

#### Edellytykset
- **Python 3.8+**
- **Node.js 16+**
- **npm tai yarn**

#### 1. Backend-asennus

```bash
# Siirry backend-hakemistoon
cd backend

# Luo virtuaaliympäristö
python -m venv venv

# Aktivoi virtuaaliympäristö
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Asenna riippuvuudet
pip install -r requirements.txt

# Käynnistä FastAPI-palvelin
python main.py
```

#### 2. Frontend-asennus

```bash
# Siirry frontend-hakemistoon (uudessa terminaalissa)
cd frontend

# Asenna riippuvuudet
npm install

# Käynnistä kehityspalvelin
npm start
```

### 🎮 Käyttöohjeet

1. **Avaa selain** osoitteessa `http://localhost:3000`
2. **Valitse kieli** (englanti/suomi) ja teema (vaalea/tumma)
3. **Kysy kysymys** karkeista (esim. "Mikä on makein karkki?")
4. **Katso taikuutta** kun järjestelmä:
   - 🔄 Käsittelee kysymyksesi
   - 🧠 Muuntaa sen vektoriupotuksiksi
   - 🔍 Hakee karkkitietokannasta
   - 📝 Valmistelee kontekstin AI:lle
   - ✨ Luo henkilökohtaisen vastauksesi

### 🛠️ Tekniset ominaisuudet

- **FastAPI + Python** backend RAG-logiikalla
- **React + TypeScript** frontend tyyppiturvallisuudella
- **ChromaDB** vektoritallennukseen
- **Framer Motion** sujuviin animaatioihin
- **Tailwind CSS** moderniin tyylittelyyn
- **OpenAI API** integraatio varavastausten kanssa

### 🤝 Osallistuminen

Olemme iloisia kaikista osallistujista! Katso englanninkielinen osio yksityiskohtaisista ohjeista.

---

## 🔗 Hyödylliset linkit

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Framer Motion Documentation](https://www.framer.com/motion/)

## 📞 Tuki

Jos kohtaat ongelmia tai sinulla on kysymyksiä:
1. Tarkista [Issues](../../issues) -osio
2. Luo uusi issue kuvaamalla ongelmaasi
3. Mukavia RAG-kokeiluja! 🍭✨
