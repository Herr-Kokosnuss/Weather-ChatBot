"""
Weather Chat Bot Application

This application combines OpenAI's GPT model with OpenWeatherMap API to create
an interactive weather assistant. Users can ask about weather conditions in natural
language, and the bot responds with current weather information.

Requirements:
    - OpenAI API key
    - OpenWeatherMap API key
    - Python 3.7+
"""

import asyncio
import os
from typing import Dict, Any
import aiohttp
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables from .env file
load_dotenv(override=True)


async def fetch_weather_from_api(location: str) -> Dict[str, Any]:
    """
    Fetch current weather data for a given location using OpenWeatherMap API.

    Args:
        location (str): Name of the city or location (e.g., 'London,UK')

    Returns:
        Dict[str, Any]: Dictionary containing:
            - conditions (str): Weather description (e.g., 'partly cloudy')
            - temperature (float): Current temperature in Celsius

    Raises:
        aiohttp.ClientError: If the API request fails
        KeyError: If the response doesn't contain expected data
    """
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={location}&appid={os.getenv('OPENWEATHERMAP_API_KEY')}"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    # Convert temperature from Kelvin to Celsius
    temp_k = data["main"]["temp"]
    temp = temp_k - 273.15  

    conditions = data["weather"][0]["description"]
    return {"conditions": conditions, "temperature": round(temp, 1)}

async def chat_with_bot():
    """
    Run the interactive weather chat bot.

    This function initializes the chat session and handles the conversation loop.
    It uses OpenAI's GPT model to process user inputs and generate responses,
    integrating real-time weather data when needed.

    The bot can:
        1. Understand natural language questions about weather
        2. Extract location information from user queries
        3. Fetch real-time weather data
        4. Respond in a conversational manner

    The session continues until the user types 'quit'.
    """
    # Initialize OpenAI client with API key
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Set up initial conversation with system prompt
    messages = [
        {
            "role": "system",
            "content": "You are a helpful weather assistant. When users ask about weather, extract the location from the user's message and respond with weather information in Celsius."
        }
    ]
    
    print("Chat Bot: Hello! Ask me about the weather by typing the city name or something like (What's the weather like in Berlin). (Type 'quit' anytime to exit)")
    
    while True:
        # Get user input and handle quit command
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Chat Bot: Goodbye!")
            break
            
        # Add user message to conversation history
        messages.append({"role": "user", "content": user_input})
        
        # First API call: Process user input and potentially call weather function
        response = await client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=messages,
            functions=[{
                "name": "fetch_weather_from_api",
                "description": "Get the current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city e.g. 'Berlin, Germany' or 'Barcelona, Spain'"
                        }
                    },
                    "required": ["location"]
                }
            }],
            function_call="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Handle function calling if weather data is needed
        if assistant_message.function_call:
            # Extract function arguments and call weather API
            function_args = eval(assistant_message.function_call.arguments)
            weather_data = await fetch_weather_from_api(**function_args)
            
            # Add weather data to conversation history
            messages.append({
                "role": "function",
                "name": "fetch_weather_from_api",
                "content": str(weather_data)
            })
            
            # Second API call: Generate response using weather data
            second_response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            
            print(f"Chat Bot: {second_response.choices[0].message.content}")
            messages.append({"role": "assistant", "content": second_response.choices[0].message.content})
        else:
            # Handle direct responses (non-weather queries)
            print(f"Chat Bot: {assistant_message.content}")
            messages.append({"role": "assistant", "content": assistant_message.content})

if __name__ == "__main__":
    asyncio.run(chat_with_bot())
