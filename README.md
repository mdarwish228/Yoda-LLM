# Yoda Chat Bot

A conversational AI chatbot that responds in the style of Yoda from Star Wars, built with Python and Transformers.

## Features

- **Yoda-style responses**: The bot responds in Yoda's unique speaking style and grammar
- **Modern UI**: Clean, responsive graphical interface with dark theme
- **Real-time chat**: Interactive chat interface with loading indicators
- **MVC Architecture**: Well-structured codebase following Model-View-Controller pattern
- **Async operations**: Non-blocking UI with threaded model operations

## Architecture

The application follows the MVC (Model-View-Controller) pattern:

- **Model** (`model/ui/yoda_model.py`): Handles LLM operations and conversation management
- **View** (`view/yoda_view.py`): Manages the user interface and user interactions
- **Controller** (`controller/yoda_controller.py`): Coordinates between Model and View