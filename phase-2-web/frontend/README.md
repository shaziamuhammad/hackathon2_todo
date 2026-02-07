# Secure Todo Frontend

This is the frontend for the secure todo application built with React and TypeScript.

## Features

- JWT-based authentication
- Responsive dashboard UI
- Task management (CRUD operations)
- Real-time task status updates
- Empty states, loading states, and error handling

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Start the development server:
```bash
npm start
```

The app will run on `http://localhost:3000`.

## Environment Variables

- `REACT_APP_API_URL`: The URL of the backend API (defaults to `http://localhost:8000`)

## Scripts

- `npm start`: Start the development server
- `npm run build`: Build the app for production
- `npm test`: Run tests
- `npm run eject`: Eject from Create React App (irreversible)