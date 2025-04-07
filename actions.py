"""
Minimal Working Custom Actions Example for NeMo Guardrails

This example creates a minimal configuration that uses custom actions.
"""
import os
import datetime
import argparse
import dotenv
from nemoguardrails import RailsConfig, LLMRails
from nemoguardrails.actions import action

# Load environment variables from .env file if it exists
dotenv.load_dotenv()

# Define custom actions
@action(name="get_current_time")
async def get_current_time():
    """Get the current time."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return current_time

@action(name="get_current_date")
async def get_current_date():
    """Get the current date."""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return current_date

@action(name="get_weather")
async def get_weather(location="Santa Clara"):
    """Get fake weather data for demonstration purposes."""
    return f"Sunny and 72°F in {location}"


# Use the guardrails configuration
def test_guardrails(use_nim=False):
    # Determine which configuration to load based on command-line arguments
    if use_nim:
        print("Using local NIM model endpoint")
        # Load the base configuration
        config = RailsConfig.from_path("./config_actions")
        
        # Replace the model configuration with NIM settings when using --nim/-n
        from nemoguardrails.rails.llm.config import Model
        
        nim_model = Model(
            type="main",
            engine="nim",
            model="meta/llama-3.1-8b-instruct",
            parameters={"base_url": "http://localhost:8000/v1"}
        )
        
        config.models = [nim_model]
    else:
        print("Using OpenAI model endpoint")
        # Load the default OpenAI configuration
        config = RailsConfig.from_path("./config_actions")
    
    # Create the rails with the appropriate configuration
    rails = LLMRails(config)
    
    # Test with time question
    time_response = rails.generate(messages=[{
        "role": "user",
        "content": "What time is it?"
    }])
    print("User: What time is it?")
    print(f"Assistant: {time_response['content']}")
    
    # Test with date question
    date_response = rails.generate(messages=[{
        "role": "user",
        "content": "What date is it today?"
    }])
    print("\nUser: What date is it today?")
    print(f"Assistant: {date_response['content']}")
    
    # Test with weather question
    weather_response = rails.generate(messages=[{
        "role": "user",
        "content": "How's the weather?"
    }])
    print("\nUser: How's the weather?")
    print(f"Assistant: {weather_response['content']}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="NeMo Guardrails Actions Example")
    parser.add_argument("-n", "--nim", action="store_true", help="Use local NIM model endpoint instead of OpenAI")
    args = parser.parse_args()
    
    # Check for OpenAI API key only if not using NIM
    if not args.nim and "OPENAI_API_KEY" not in os.environ:
        print("Warning: OPENAI_API_KEY environment variable is not set.")
        print("You can set it in your environment or create a .env file with your API key.")
        print("Example .env file content: OPENAI_API_KEY=your-api-key-here")
        # Uncomment the following line to set the API key directly in the code (not recommended for production)
        # os.environ["OPENAI_API_KEY"] = "your-api-key-here"
    
    test_guardrails(use_nim=args.nim)
