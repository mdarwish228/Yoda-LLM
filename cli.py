"""A simple CLI for interacting with a Yoda-themed chatbot using a fine-tuned language model."""

from transformers import AutoModelForCausalLM, AutoTokenizer

from model import YodaConversation
from util.prompt_util import prompt


def yoda_chatbot() -> None:
    """Run a simple CLI for chatting with a Yoda-themed AI model."""

    print("Yoda Chatbot: Loading model, please wait...")

    # You can change the model name to your preferred one
    model_name = (
        "unsloth/gemma-2-2b-it"  # Replace with your Yoda fine-tuned model if available
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Get Yoda system prompt
    yoda_conv = YodaConversation()

    print("Yoda Chatbot: Speak to me, you will. Type 'exit' to leave, you must.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Yoda Chatbot: Goodbye, you must say. May the Force be with you!")
            break
        yoda_conv.add_question(user_input)
        response = prompt(model, tokenizer, str(yoda_conv))
        yoda_conv.add_answer(response)
        print(f"Yoda: {response.strip()}")


if __name__ == "__main__":
    yoda_chatbot()
