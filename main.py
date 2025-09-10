"""Main UI entry point for the Yoda Chat Bot application."""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import local modules after path modification
from controller import YodaController  # noqa: E402
from model.ui import YodaModel  # noqa: E402
from view import YodaView  # noqa: E402


def main() -> None:
    """Main entry point for the Yoda Chat Bot UI application."""
    try:
        # Create the main window
        root = tk.Tk()

        # Initialize MVC components
        model = YodaModel()
        view = YodaView(root)
        controller = YodaController(model, view)

        # Set window icon and title
        root.title("Yoda Chat Bot")

        # Center the window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")

        # Handle window closing
        def on_closing() -> None:
            """Handle application closing."""
            if controller.is_model_generating():
                # Show confirmation dialog if model is generating
                result = messagebox.askyesno(
                    "Exit", "Yoda is still thinking. Are you sure you want to exit?"
                )
                if result:
                    root.destroy()
            else:
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Start the UI
        print("Starting Yoda Chat Bot UI...")
        view.run()

    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
