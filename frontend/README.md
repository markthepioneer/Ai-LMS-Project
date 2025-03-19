# Ai-LMS Frontend

This is the frontend application for the AI Life Management System (Ai-LMS). It's built with React, TypeScript, and uses modern UI libraries to create a beautiful and intuitive user experience.

## Technology Stack

- **React**: A JavaScript library for building user interfaces
- **TypeScript**: For type safety and better developer experience
- **React Router**: For navigation and routing
- **Tailwind CSS**: For styling and responsive design
- **Chart.js**: For data visualization
- **Axios**: For API requests
- **React Query**: For data fetching, caching, and state management
- **React Hook Form**: For form handling
- **Zod**: For schema validation

## Getting Started

### Prerequisites

- Node.js 16.x or higher
- npm 8.x or higher

### Installation

1. Clone the repository and navigate to the frontend directory:
   ```bash
   git clone https://github.com/markthepioneer/Ai-LMS-Project.git
   cd Ai-LMS-Project/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file for environment variables:
   ```bash
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm start
   ```

## Project Structure

```
frontend/
├── public/             # Static files
├── src/                # Source code
│   ├── api/            # API service calls
│   ├── assets/         # Images, fonts, etc.
│   ├── components/     # Reusable components
│   │   ├── common/     # Common UI components
│   │   ├── finance/    # Finance module components 
│   │   ├── health/     # Health module components
│   │   └── ...         # Other module-specific components
│   ├── contexts/       # React contexts
│   ├── hooks/          # Custom React hooks
│   ├── layouts/        # Page layouts
│   ├── pages/          # Page components
│   ├── styles/         # Global styles
│   ├── types/          # TypeScript types
│   ├── utils/          # Utility functions
│   ├── App.tsx         # Main App component
│   └── index.tsx       # Entry point
├── package.json
└── tsconfig.json
```

## Features

- **Dashboard**: Overview of all life areas and quick access to modules
- **Finance Management**: Budget tracking, expense analysis, and financial planning
- **Health Tracking**: Sleep, exercise, and meal tracking with insights
- **Task Management**: Task organization, scheduling, and prioritization
- **Portfolio Management**: Investment tracking and performance analysis  
- **Memory Assistant**: Contact management, reminders, and events
- **Email Management**: Email organization, templates, and analytics
- **Life Balance**: Life area satisfaction tracking and goal management

## Available Scripts

- `npm start`: Start the development server
- `npm run build`: Build the application for production
- `npm test`: Run tests
- `npm run lint`: Run ESLint
