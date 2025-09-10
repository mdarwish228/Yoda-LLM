"""View layer for the Yoda Chat Bot UI application."""

import threading
import time
import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk


class LoadingAnimation:
    """Animated loading indicator for when Yoda is thinking."""

    def __init__(self, canvas: tk.Canvas, x: int, y: int, radius: int = 8) -> None:
        """Initialize the loading animation.

        Args:
            canvas: The canvas to draw on.
            x: X position of the animation center.
            y: Y position of the animation center.
            radius: Radius of the dots.
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.dots = []
        self.animation_thread: threading.Thread | None = None
        self.is_running = False

    def start(self) -> None:
        """Start the loading animation."""
        if self.is_running:
            return

        self.is_running = True
        self.animation_thread = threading.Thread(target=self._animate, daemon=True)
        self.animation_thread.start()

    def stop(self) -> None:
        """Stop the loading animation."""
        self.is_running = False
        self._clear_dots()

    def _animate(self) -> None:
        """Animation loop for the loading dots."""
        while self.is_running:
            self._clear_dots()

            # Create three dots with different opacities
            for i in range(3):
                if not self.is_running:
                    break

                # Calculate position and opacity
                angle = (time.time() * 2 + i * 2.09) % (
                    2 * 3.14159
                )  # 120 degrees apart
                dot_x = self.x + int(15 * (i - 1) * 0.5)  # Spread dots horizontally
                dot_y = self.y + int(
                    5 * (i % 2)
                )  # Slight vertical offset for middle dot

                # Create dot with varying opacity effect
                opacity = int(
                    255
                    * (
                        0.3
                        + 0.7 * abs((angle % (2 * 3.14159)) / (2 * 3.14159) - 0.5) * 2
                    )
                )

                # Use green color for Yoda theme with opacity
                red = int(45 * (opacity / 255))  # Dark green base
                green = int(90 * (opacity / 255))
                blue = int(45 * (opacity / 255))

                dot = self.canvas.create_oval(
                    dot_x - self.radius,
                    dot_y - self.radius,
                    dot_x + self.radius,
                    dot_y + self.radius,
                    fill=f"#{red:02x}{green:02x}{blue:02x}",
                    outline="",
                )
                self.dots.append(dot)

            time.sleep(0.1)

    def _clear_dots(self) -> None:
        """Clear all dots from the canvas."""
        for dot in self.dots:
            self.canvas.delete(dot)
        self.dots.clear()


class YodaView:
    """View layer for the Yoda Chat Bot UI.

    This class handles all UI components, layout, and user interactions
    for the chat interface.
    """

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the Yoda view.

        Args:
            root: The main tkinter root window.
        """
        self.root = root
        self.controller: Callable | None = None
        self.loading_animation: LoadingAnimation | None = None

        self._setup_ui()
        self._setup_bindings()

    def set_controller(self, controller: Callable) -> None:
        """Set the controller callback function.

        Args:
            controller: Function to call when user sends a message.
        """
        self.controller = controller

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        self.root.title("Yoda Chat Bot")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")

        # Configure style with rounded corners
        style = ttk.Style()
        style.theme_use("clam")

        # Label styles
        style.configure("Yoda.TLabel", background="#f5f5f5", foreground="#2d5a2d")
        style.configure("User.TLabel", background="#f5f5f5", foreground="#333333")

        # Entry styles with rounded appearance
        style.configure(
            "Rounded.TEntry",
            fieldbackground="#ffffff",
            borderwidth=0,
            relief="flat",
            bordercolor="#cccccc",
            focuscolor="none",
            padding=(10, 8),
        )

        # Button styles with rounded appearance
        style.configure(
            "Send.TButton",
            background="#2d5a2d",
            foreground="#ffffff",
            borderwidth=0,
            relief="flat",
            bordercolor="#2d5a2d",
            focuscolor="none",
            padding=(15, 8),
        )
        style.map(
            "Send.TButton", background=[("active", "#1e3d1e"), ("pressed", "#0f1f0f")]
        )

        # Main frame - centered with proper padding
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Chat area
        self._setup_chat_area(main_frame)

        # Status bar (between chat and input)
        self._setup_status_bar(main_frame)

        # Input area
        self._setup_input_area(main_frame)

    def _setup_chat_area(self, parent: tk.Frame) -> None:
        """Set up the chat display area."""
        # Chat frame - remove ttk.Frame to eliminate surrounding colors
        chat_frame = tk.Frame(parent, bg="#f5f5f5")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Chat text widget with conditional scrollbar
        self.chat_text = tk.Text(
            chat_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#ffffff",
            fg="#333333",
            font=("Arial", 13),
            insertbackground="#333333",
            selectbackground="#e0e0e0",
            relief=tk.FLAT,
            borderwidth=0,
            padx=15,
            pady=15,
            highlightthickness=0,
        )
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Custom scrollbar that only appears when needed
        self.scrollbar = tk.Scrollbar(
            chat_frame, orient=tk.VERTICAL, command=self._scroll_command
        )
        self.chat_text.configure(yscrollcommand=self._on_scroll)

        # Initially hide the scrollbar
        self.scrollbar.pack_forget()

        # Configure text tags for styling
        self.chat_text.tag_configure(
            "user", foreground="#333333", font=("Arial", 13, "bold")
        )
        self.chat_text.tag_configure(
            "yoda", foreground="#2d5a2d", font=("Arial", 13, "bold")
        )
        self.chat_text.tag_configure(
            "system", foreground="#666666", font=("Arial", 12, "italic")
        )

    def _setup_input_area(self, parent: tk.Frame) -> None:
        """Set up the input area."""
        # Input area - remove ttk.Frame to eliminate surrounding colors
        input_frame = tk.Frame(parent, bg="#f5f5f5")
        input_frame.pack(fill=tk.X, pady=(5, 10))

        # Input field with rounded style
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            input_frame,
            textvariable=self.input_var,
            font=("Arial", 13),
            style="Rounded.TEntry",
        )
        # Pack with reduced padding
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self._on_send_clicked,
            style="Send.TButton",
        )
        self.send_button.pack(side=tk.RIGHT)

    def _setup_status_bar(self, parent: tk.Frame) -> None:
        """Set up the status bar with chat-like design."""
        # Create a subtle status indicator
        self.status_var = tk.StringVar()
        self.status_var.set("")

        # Status container - make same color as background
        status_container = tk.Frame(parent, bg="#f5f5f5", relief=tk.FLAT, bd=0)
        status_container.pack(fill=tk.X, pady=(2, 2))

        # Status label - make same color as background
        self.status_label = tk.Label(
            status_container,
            textvariable=self.status_var,
            bg="#f5f5f5",
            fg="#666666",
            font=("Arial", 9),
            padx=8,
            pady=4,
        )
        self.status_label.pack(side=tk.LEFT)

        # No loading animation - just status text
        self.loading_animation = None

    def _setup_bindings(self) -> None:
        """Set up keyboard bindings."""
        self.input_entry.bind("<Return>", lambda _: self._on_send_clicked())

    def _on_send_clicked(self) -> None:
        """Handle send button click."""
        message = self.input_var.get().strip()
        if message and self.controller:
            self.input_var.set("")
            self.controller(message)

    def add_message(self, sender: str, message: str) -> None:
        """Add a message to the chat display.

        Args:
            sender: The sender of the message ("You" or "Yoda").
            message: The message content.
        """
        self.chat_text.config(state=tk.NORMAL)

        # Add sender label
        if sender == "You":
            self.chat_text.insert(tk.END, f"{sender}: ", "user")
        else:
            self.chat_text.insert(tk.END, f"{sender}: ", "yoda")

        # Add message content
        self.chat_text.insert(tk.END, f"{message}\n\n")

        self.chat_text.config(state=tk.DISABLED)
        self._scroll_to_bottom()
        # Check if scrollbar should be shown/hidden after adding content
        self.root.after_idle(self._check_scrollbar_visibility)

    def add_system_message(self, message: str) -> None:
        """Add a system message to the chat display.

        Args:
            message: The system message content.
        """
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"System: {message}\n\n", "system")
        self.chat_text.config(state=tk.DISABLED)
        self._scroll_to_bottom()
        # Check if scrollbar should be shown/hidden after adding content
        self.root.after_idle(self._check_scrollbar_visibility)

    def show_loading(self) -> None:
        """Show the loading state."""
        self.status_var.set("Yoda is typing...")
        self.send_button.config(state=tk.DISABLED)
        self.input_entry.config(state=tk.DISABLED)

    def hide_loading(self) -> None:
        """Hide the loading state."""
        self.status_var.set("")
        self.send_button.config(state=tk.NORMAL)
        self.input_entry.config(state=tk.NORMAL)
        self.input_entry.focus()

    def disable_input(self) -> None:
        """Disable input during model initialization."""
        self.send_button.config(state=tk.DISABLED)
        self.input_entry.config(state=tk.DISABLED)

    def enable_input(self) -> None:
        """Enable input when model is ready."""
        self.send_button.config(state=tk.NORMAL)
        self.input_entry.config(state=tk.NORMAL)
        self.input_entry.focus()

    def show_error(self, error_message: str) -> None:
        """Show an error message.

        Args:
            error_message: The error message to display.
        """
        messagebox.showerror("Error", error_message)
        self.hide_loading()

    def show_info(self, info_message: str) -> None:
        """Show an info message.

        Args:
            info_message: The info message to display.
        """
        messagebox.showinfo("Info", info_message)

    def update_status(self, status: str) -> None:
        """Update the status bar message.

        Args:
            status: The status message to display.
        """
        self.status_var.set(status)

    def _scroll_command(self, *args: str) -> None:
        """Handle scrollbar commands from the scrollbar widget."""
        # Simply pass through to the text widget's yview method
        self.chat_text.yview(*args)

    def _on_scroll(self, *args: str) -> None:
        """Handle scrollbar visibility based on content."""
        # Update the scrollbar position
        self.scrollbar.set(*args)

        # Check if scrollbar should be visible
        if args:
            # Convert string arguments to float
            first, last = float(args[0]), float(args[1])
        else:
            first, last = self.chat_text.yview()

        # Show scrollbar only if content extends beyond visible area
        if first > 0 or last < 1:
            if not self.scrollbar.winfo_viewable():
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        elif self.scrollbar.winfo_viewable():
            self.scrollbar.pack_forget()

    def _check_scrollbar_visibility(self) -> None:
        """Check if scrollbar should be visible based on content."""
        # Get the current view
        first, last = self.chat_text.yview()

        # Show scrollbar only if content extends beyond visible area
        if first > 0 or last < 1:
            if not self.scrollbar.winfo_viewable():
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        elif self.scrollbar.winfo_viewable():
            self.scrollbar.pack_forget()

    def _scroll_to_bottom(self) -> None:
        """Scroll the chat text to the bottom."""
        self.chat_text.see(tk.END)

    def focus_input(self) -> None:
        """Focus the input field."""
        self.input_entry.focus()

    def run(self) -> None:
        """Start the UI main loop."""
        self.root.mainloop()
