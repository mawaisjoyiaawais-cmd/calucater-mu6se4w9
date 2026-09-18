import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

# A safer way to evaluate mathematical expressions than raw eval()
def safe_eval(expression):
    try:
        # A simple check to avoid obvious non-mathematical inputs
        if any(c.isalpha() for c in expression):
            return "Error"
        # The eval function can still be a security risk if not used carefully,
        # but in this controlled calculator environment, it is acceptable.
        return str(eval(expression))
    except (SyntaxError, ZeroDivisionError, TypeError):
        return "Error"
    except Exception:
        # Catch any other unexpected errors during evaluation
        return "Error"

class CalucaterApp(App):
    def build(self):
        self.title = "Calucater"
        self.operators = ['/', '*', '-', '+']
        
        # Main layout container
        root_widget = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Display screen for numbers and results
        self.display = TextInput(
            text='', 
            font_size=60, 
            readonly=True, 
            halign='right', 
            multiline=False,
            size_hint_y=None,
            height=150
        )
        root_widget.add_widget(self.display)

        # Layout for the grid of buttons
        button_layout = GridLayout(cols=4, spacing=10)
        
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '.', '+'
        ]

        for label in buttons:
            button = Button(text=label, font_size=40, on_press=self.on_button_press)
            button_layout.add_widget(button)
        
        root_widget.add_widget(button_layout)
        
        # Dedicated equals button at the bottom
        equals_button = Button(
            text='=', 
            font_size=40, 
            size_hint_y=None, 
            height=100,
            on_press=self.on_solution,
            background_color=(0.2, 0.6, 0.8, 1) # Make it stand out
        )
        root_widget.add_widget(equals_button)

        return root_widget

    def on_button_press(self, instance):
        button_text = instance.text
        current_text = self.display.text

        if button_text == 'C':
            self.display.text = ''
            return
            
        if current_text == "Error":
             self.display.text = ''
             current_text = ''

        # Prevent adding multiple operators consecutively
        if button_text in self.operators:
            if not current_text:
                # Do not start an expression with an operator
                return
            if current_text[-1] in self.operators:
                # If the last character is an operator, replace it
                self.display.text = current_text[:-1] + button_text
                return

        # Prevent multiple decimal points in a single number segment
        if button_text == '.':
            # A simple way to check the current number segment for a decimal
            temp_text = current_text.replace('/', ' ').replace('*', ' ').replace('-', ' ').replace('+', ' ')
            numbers = temp_text.split()
            if numbers and '.' in numbers[-1]:
                # If the last number segment already has a decimal, do nothing
                return

        self.display.text += button_text

    def on_solution(self, instance):
        expression = self.display.text
        if not expression:
            return

        # Do not try to evaluate if the expression ends with an operator
        if expression[-1] in self.operators:
            return
            
        result = safe_eval(expression)
        self.display.text = result


if __name__ == '__main__':
    CalucaterApp().run()
