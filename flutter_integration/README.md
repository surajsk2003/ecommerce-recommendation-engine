# SmartCommerce Flutter App

AI-powered mobile e-commerce app with advanced recommendation features.

## Features

- AI-powered product recommendations
- Voice search and commands
- Offline functionality
- Real-time personalization
- Firebase integration
- Cross-platform (iOS/Android)

## Setup

```bash
# Install dependencies
flutter pub get

# Run code generation
flutter packages pub run build_runner build

# Run the app
flutter run
```

## Architecture

- **State Management**: Provider pattern
- **Networking**: Dio with offline caching
- **AI Services**: On-device personalization
- **Voice**: Speech-to-text and text-to-speech
- **Analytics**: Firebase Analytics
- **Storage**: Secure local storage

## API Integration

The app connects to the Django backend at `http://localhost:8000` for:
- Product recommendations
- User interactions tracking
- Real-time updates
- AI-powered features