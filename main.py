"""Main entry point for the Yoda Chat Bot application."""

from typing import NoReturn

from transformers import AutoModelForCausalLM, AutoTokenizer

from model.yoda_conversation import YodaConversation
from util.prompt_util import prompt


def main() -> NoReturn:
    """Run the main Yoda Chat Bot application.

    Initializes the model, tokenizer, and conversation handler,
    then enters an interactive chat loop with the user.
    """
    conversation = YodaConversation()

    model_id = "unsloth/gemma-2-2b-it"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

    print("Yoda Chat Bot - Ask me anything! (Type 'quit' or 'exit' to stop)")
    print("-" * 50)

    while True:
        try:
            # Get user input
            user_question = input("\nYou: ").strip()

            # Check for empty input
            if not user_question:
                continue

            # Check for exit commands
            if user_question.lower() in ["quit", "exit", "bye", "goodbye"]:
                print("Yoda: Farewell, young one. May the force be with you.")
                break

            # Add question to conversation
            conversation.add_question(user_question)

            # Get bot response
            print("Yoda: ", end="", flush=True)
            answer = prompt(model, tokenizer, str(conversation))
            conversation.add_answer(answer)

            # Print the response
            print(answer.strip())

        except KeyboardInterrupt:
            print("\n\nYoda: Interrupted, you have been. Goodbye, young one.")
            break
        except EOFError:
            print("\n\nYoda: End of input, I sense. Farewell.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Yoda: Confused, I am. Try again, you should.")


if __name__ == "__main__":
    main()
