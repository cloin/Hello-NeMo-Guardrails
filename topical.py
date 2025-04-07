"""
NeMo Guardrails Topical Rails Example

This example demonstrates how to create topical rails that guide the bot
to avoid specific topics while allowing it to respond to desired ones.
"""
import os
import argparse
import dotenv
from nemoguardrails import RailsConfig, LLMRails

# Load environment variables from .env file if it exists
dotenv.load_dotenv()

# Load the guardrails configuration
def load_rails_config(use_nim=False):
    # Determine which configuration to load based on command-line arguments
    if use_nim:
        print("Using local NIM model endpoint")
        config_path = "./config_topical"
        # We need to modify the config object after loading
        config = RailsConfig.from_path(config_path)
        
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
        config_path = "./config_topical"
        config = RailsConfig.from_path(config_path)
    
    rails = LLMRails(config)
    return rails

# Use the guardrails configuration
def test_guardrails(rails):
    # Test with a cooking question (allowed topic)
    cooking_response = rails.generate(messages=[{
        "role": "user",
        "content": "How do I make a chocolate cake?"
    }])
    print("User: How do I make a chocolate cake?")
    print(f"Assistant: {cooking_response['content']}")
    
    # Test with a politics question (disallowed topic)
    politics_response = rails.generate(messages=[{
        "role": "user",
        "content": "What do you think about the current president?"
    }])
    print("\nUser: What do you think about the current president?")
    print(f"Assistant: {politics_response['content']}")
    
    # Test with a stock market question (disallowed topic)
    stocks_response = rails.generate(messages=[{
        "role": "user",
        "content": "What stocks should I invest in?"
    }])
    print("\nUser: What stocks should I invest in?")
    print(f"Assistant: {stocks_response['content']}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="NeMo Guardrails Topical Rails Example")
    parser.add_argument("-n", "--nim", action="store_true", help="Use local NIM model endpoint instead of OpenAI")
    args = parser.parse_args()
    
    # Check for OpenAI API key only if not using NIM
    if not args.nim and "OPENAI_API_KEY" not in os.environ:
        print("Warning: OPENAI_API_KEY environment variable is not set.")
        print("You can set it in your environment or create a .env file with your API key.")
        print("Example .env file content: OPENAI_API_KEY=your-api-key-here")
        # Uncomment the following line to set the API key directly in the code (not recommended for production)
        # os.environ["OPENAI_API_KEY"] = "your-api-key-here"
    
    rails = load_rails_config(use_nim=args.nim)
    test_guardrails(rails)
