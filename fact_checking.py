"""
Simple Fact Checking with Basic Knowledge Retrieval

This example demonstrates a basic approach to fact checking and
knowledge retrieval in NeMo Guardrails.
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
        # Load the base configuration
        config = RailsConfig.from_path("./config_fact_checking")
        
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
        config = RailsConfig.from_path("./config_fact_checking")
    
    rails = LLMRails(config)
    return rails

# Use the guardrails configuration
def test_guardrails(rails):
    # Test with a question about NVIDIA
    nvidia_response = rails.generate(messages=[{
        "role": "user",
        "content": "Who founded NVIDIA and when?"
    }])
    print("User: Who founded NVIDIA and when?")
    print(f"Assistant: {nvidia_response['content']}")
    
    # Test with a question about NeMo Guardrails
    nemo_response = rails.generate(messages=[{
        "role": "user",
        "content": "What is NeMo Guardrails and when was it released?"
    }])
    print("\nUser: What is NeMo Guardrails and when was it released?")
    print(f"Assistant: {nemo_response['content']}")
    
    # Test with a question that's not in our knowledge base
    unknown_response = rails.generate(messages=[{
        "role": "user",
        "content": "What is NVIDIA's financial performance in 2023?"
    }])
    print("\nUser: What is NVIDIA's financial performance in 2023?")
    print(f"Assistant: {unknown_response['content']}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="NeMo Guardrails Fact Checking Example")
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
