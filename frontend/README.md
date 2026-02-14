# College Chatbot Frontend

Modern React frontend for the College RAG Chatbot built with Vite.

## Features

- 🎨 **Modern UI/UX** - Professional dark theme with gradients and animations
- 💬 **Real-time Chat** - Interactive chat interface with typing indicators
- 📊 **System Monitoring** - Live health and statistics display
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🔍 **Source Citations** - Shows document sources with relevance scores
- 💡 **Suggested Questions** - Quick-start questions for users

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Axios** - HTTP client for API calls
- **CSS3** - Modern styling with animations

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will start at: **http://localhost:3000**

### 3. Build for Production

```bash
npm run build
```

## API Integration

The frontend connects to the FastAPI backend running at `http://localhost:8000` through a Vite proxy configuration.

### Endpoints Used:

- `POST /chat` - Send questions and receive answers
- `GET /health` - Check system health status
- `GET /stats` - Get document statistics
- `GET /` - API information

## Project Structure

```
frontend/
├── src/
│   ├── services/
│   │   └── api.js          # API service layer
│   ├── App.jsx             # Main application component
│   ├── App.css             # Application styles
│   ├── main.jsx            # React entry point
│   └── index.css           # Global styles
├── index.html              # HTML template
├── vite.config.js          # Vite configuration
└── package.json            # Dependencies
```

## Usage

1. **Start Backend**: Make sure the FastAPI server is running on port 8000
2. **Start Frontend**: Run `npm run dev` in the frontend directory
3. **Open Browser**: Navigate to http://localhost:3000
4. **Ask Questions**: Type your question or select from suggested questions

## Features Explained

### Chat Interface
- Clean, modern chat UI with message bubbles
- User messages on the right, bot responses on the left
- Timestamps for each message
- Smooth scrolling to latest messages

### Source Display
- Each bot response shows source documents
- Relevance score percentage for each source
- Expandable source content preview
- File path for reference

### Sidebar
- **System Status**: Real-time health monitoring
  - Vector DB status
  - Ollama availability
  - Overall system health
- **Document Stats**: Total indexed chunks
- **Suggested Questions**: Quick-start queries

### Responsive Design
- Desktop: Full sidebar visible
- Mobile: Collapsible sidebar with toggle button
- Adaptive layout for all screen sizes

## Customization

### Change Theme Colors

Edit the CSS variables in `src/App.css`:

```css
:root {
  --primary-color: #6366f1;
  --secondary-color: #8b5cf6;
  --background: #0f172a;
  /* ... more variables */
}
```

### Modify Suggested Questions

Edit the `suggestedQuestions` array in `src/App.jsx`:

```javascript
const suggestedQuestions = [
  "Your custom question here",
  // ... more questions
];
```

### Change API URL

Edit `vite.config.js` to change the backend URL:

```javascript
proxy: {
  '/api': {
    target: 'http://your-backend-url:8000',
    // ...
  }
}
```

## Troubleshooting

### Frontend can't connect to backend
- Ensure FastAPI server is running on port 8000
- Check CORS settings in backend `main.py`
- Verify proxy configuration in `vite.config.js`

### Build errors
- Delete `node_modules` and run `npm install` again
- Clear Vite cache: `npm run dev -- --force`

### Styling issues
- Hard refresh browser (Ctrl+Shift+R)
- Clear browser cache

## Production Deployment

### Build the app:
```bash
npm run build
```

### Serve the built files:
```bash
npm run preview
```

Or deploy the `dist/` folder to any static hosting service (Vercel, Netlify, etc.)

## License

Part of the College RAG Chatbot project.
