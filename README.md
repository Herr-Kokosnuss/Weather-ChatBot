# Weather Chat Bot

An intelligent weather assistant that combines OpenAI's GPT model with real-time weather data from OpenWeatherMap. Users can ask about weather conditions in natural language, and the bot responds with accurate, current weather information.

## Features

- Natural language processing for weather queries
- Real-time weather data integration
- Temperature display in Celsius
- Interactive chat interface
- Asynchronous operation for better performance
- Intelligent conversation memory
- Location extraction from natural language

## Prerequisites

- Python 3.7 or higher
- OpenAI API key
- OpenWeatherMap API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd weather-chat-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
```

## Usage

1. Run the bot:
```bash
python main.py
```

2. Start chatting! You can:
   - Ask about weather directly: "What's the weather in London?"
   - Use conversational queries: "Is it cold in New York today?"
   - Type 'quit' to exit the chat

Example conversation:
```
Chat Bot: Hello! Ask me about the weather by typing the city name or something like (What's the weather like in Berlin). (Type 'quit' anytime to exit)
You: How's the weather in Tokyo?
Chat Bot: In Tokyo, it's currently 22.3°C with partly cloudy conditions.
```

## Technical Details

### Architecture
- Asynchronous Python using `asyncio`
- OpenAI's GPT-4o-mini for natural language processing
- OpenWeatherMap API for real-time weather data
- Environment variable management with python-dotenv
- HTTP requests handled by aiohttp

### Key Components
1. **Weather API Integration** (`fetch_weather_from_api`):
   - Fetches real-time weather data
   - Converts temperatures from Kelvin to Celsius
   - Handles API responses and errors

2. **Chat Interface** (`chat_with_bot`):
   - Manages conversation flow
   - Handles user input/output
   - Maintains conversation context
   - Integrates GPT responses with weather data

## Error Handling

The application includes error handling for:
- Failed API requests
- Invalid location inputs
- Missing API keys
- Malformed responses
