from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
import rlc

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("RLC Circuit Simulator")
        self.setGeometry(200, 100, 600, 400)

        # Create a layout
        layout = QVBoxLayout()

        # Input fields
        self.resistance_input = QLineEdit(self)
        self.resistance_input.setPlaceholderText("Enter resistance (Ω)")
        layout.addWidget(self.resistance_input)

        self.inductance_input = QLineEdit(self)
        self.inductance_input.setPlaceholderText("Enter inductance (H)")
        layout.addWidget(self.inductance_input)

        self.capacitance_input = QLineEdit(self)
        self.capacitance_input.setPlaceholderText("Enter capacitance (F)")
        layout.addWidget(self.capacitance_input)

        self.initial_capacitor_voltage_input = QLineEdit(self)
        self.initial_capacitor_voltage_input.setPlaceholderText("Initial capacitor voltage (V)")
        layout.addWidget(self.initial_capacitor_voltage_input)

        self.initial_current_input = QLineEdit(self)
        self.initial_current_input.setPlaceholderText("Initial inductor current (A)")
        layout.addWidget(self.initial_current_input)

        self.choice_input = QLineEdit(self)
        self.choice_input.setPlaceholderText("Type 1 for parallel, 2 for series")
        layout.addWidget(self.choice_input)

        self.graphic_choice = QLineEdit(self)
        self.graphic_choice.setPlaceholderText("Would you like to see the graph of the function? Write 1 for yes, 0 for no: ")
        layout.addWidget(self.graphic_choice)

       
        self.button = QPushButton("Simulate RLC Circuit", self)
        self.button.clicked.connect(self.on_submit_button_click)
        layout.addWidget(self.button)

        # Label to display results
        self.label = QLabel("", self)
        layout.addWidget(self.label)

        # Set the layout
        self.setLayout(layout)

    def on_submit_button_click(self):
       
        try:
            resistance = float(self.resistance_input.text())
            inductance = float(self.inductance_input.text())
            capacitance = float(self.capacitance_input.text())
            initial_capacitor_voltage = float(self.initial_capacitor_voltage_input.text())
            initial_inductor_current = float(self.initial_current_input.text())
            choice = int(self.choice_input.text())
            graphic_choice = int(self.graphic_choice.text())

           
            result_text = rlc.rlc(resistance, inductance, capacitance, initial_capacitor_voltage, initial_inductor_current, choice, graphic_choice)

            self.label.setText(result_text)
        except ValueError:
            self.label.setText("Invalid input! Please enter numerical values.")

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
