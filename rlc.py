import cmath
import math
import numpy as np
import matplotlib.pyplot as plt


def rlc(resistance, inductance, capacitance):
    print("Type 1 if parallel, 2 if serially connected")
    choice = int(input("Enter an integer: "))

    damped = 0
    res_freq_squared = 1 / (inductance * capacitance)
    res_freq = math.sqrt(res_freq_squared)

    if choice == 1:
        neper_freq = 1 / (2 * resistance * capacitance)
    elif choice == 2:
        neper_freq = resistance / (2 * inductance)
    else:
        print("Invalid choice")
        return

    neper_freq_square = pow(neper_freq, 2)

    s_1 = -neper_freq + cmath.sqrt((pow(neper_freq, 2) - res_freq_squared))
    s_2 = -neper_freq - cmath.sqrt((pow(neper_freq, 2) - res_freq_squared))

    if res_freq_squared < neper_freq_square:
        damped = 1
    elif neper_freq_square < res_freq_squared:
        damped = 2
    else:
        damped = 3

    damped_conditions = {
        1: "over-damped",
        2: "under-damped",
        3: "critically damped"
    }

    print(f"neper frequency (alpha): {neper_freq:.2f}")
    print(f"resonant frequency (w): {res_freq:.2f}")
    print(f"s1: {s_1:.2f}")
    print(f"s2: {s_2:.2f}")
    print("damped condition:", damped_conditions.get(damped, "Unknown condition"))

    derivative_of_vc = 0
    initial_capacitor_voltage = 0
    initial_inductor_current = 0

    if choice == 1:

        initial_capacitor_voltage = int(input("Initial capacitor voltage (V): "))
        initial_inductor_current = float(input("Initial inductor current (A): "))

        derivative_of_vc = -(initial_inductor_current + (initial_capacitor_voltage / resistance)) / capacitance

        if damped == 1:
            # Coefficients matrix
            A = np.array([[1, 1],
                          [s_1.real, s_2.real]])  # Use real parts

            # Constants matrix
            B = np.array([initial_capacitor_voltage, derivative_of_vc])

            # Solving for [x, y]
            solution = np.linalg.solve(A, B)

            A1, A2 = solution

            print(f"x = {A1}, y = {A2}")

            print(f"x(t) = {A1:.2f}e^{s_1.real:.2f}t)) + {A2:.2f}e^{s_2.real:.2f}t))")

        if damped == 2:
            B1 = initial_capacitor_voltage
            w_d = math.sqrt(res_freq_squared - neper_freq_square)
            B2 = (derivative_of_vc + (neper_freq * B1)) / w_d

            print(f"x(t) = {B1:.2f}cos({w_d}*t) + {B2:.2f}sin({w_d}*t) ) e^-{neper_freq}t")

        if damped == 3:
            D2 = initial_capacitor_voltage
            D1 = derivative_of_vc + (neper_freq * D2)

            print(f"x(t) = ({D1:.2f}t + {D2})e^-{neper_freq}t)")

    elif choice == 2:

        # Serial RLC circuit

        initial_capacitor_voltage = int(input("Initial capacitor voltage (V): "))
        initial_inductor_current = float(input("Initial inductor current (A): "))
        derivative_of_il = -(initial_capacitor_voltage / inductance) - (
                    resistance * initial_inductor_current / inductance)

        if damped == 1:

            A = np.array([[1, 1], [s_1.real, s_2.real]])
            B = np.array([initial_inductor_current, derivative_of_il])
            solution = np.linalg.solve(A, B)

            A1, A2 = solution

            print(f"i_L(t) = {A1:.2f}e^{s_1.real:.2f}t + {A2:.2f}e^{s_2.real:.2f}t")

        elif damped == 2:

            w_d = math.sqrt(res_freq_squared - neper_freq_square)
            B1 = initial_inductor_current
            B2 = (derivative_of_il + (neper_freq * B1)) / w_d

            print(f"i_L(t) = ({B1:.2f}cos({w_d:.2f}t) + {B2:.2f}sin({w_d:.2f}t)) * e^(-{neper_freq:.2f}t)")

        elif damped == 3:

            D2 = initial_inductor_current
            D1 = derivative_of_il + (neper_freq * D2)

            print(f"i_L(t) = ({D1:.2f}t + {D2:.2f}) * e^(-{neper_freq:.2f}t)")

    graphic_choice = bool(input("Would you like to see the graph of the function? Write 1 for yes, 0 for no: "))

    if graphic_choice == 1:

        if damped == 1:  # Over-damped
            end_time = 5 * (1 / neper_freq)  # Allow for settling time
        elif damped == 2:  # Under-damped
            end_time = 3 * (2 * np.pi / res_freq)  # Few cycles of oscillation
        else:  # Critically damped
            end_time = 5 * (1 / neper_freq)  # Similar to over-damped

        t = np.linspace(0, end_time, 1000)  # time from 0 to 10 ms
        response = np.zeros_like(t)

        if choice == 1:  # Parallel circuit
            if damped == 1:
                # Over-damped response
                response = A1 * np.exp(s_1.real * t) + A2 * np.exp(s_2.real * t)
            elif damped == 2:
                # Under-damped response
                response = B1 * np.cos(w_d * t) * np.exp(-neper_freq * t) + B2 * np.sin(w_d * t) * np.exp(
                    -neper_freq * t)
            elif damped == 3:
                # Critically damped response
                response = (D1 * t + D2) * np.exp(-neper_freq * t)

        elif choice == 2:  # Serial circuit
            if damped == 1:
                response = A1 * np.exp(s_1.real * t) + A2 * np.exp(s_2.real * t)
            elif damped == 2:
                response = (B1 * np.cos(w_d * t) + B2 * np.sin(w_d * t)) * np.exp(-neper_freq * t)
            elif damped == 3:
                response = (D1 * t + D2) * np.exp(-neper_freq * t)

        # Plot the response
        plt.figure(figsize=(10, 5))
        plt.plot(t, response)
        plt.title('RLC Circuit Response')
        plt.xlabel('Time (s)')
        plt.ylabel('Response')
        plt.grid()
        plt.show()


rlc(200, 50e-3, 0.2e-6)

# serial rlc(560, 0.1, 0.1e-6)
# rlc(200, 50e-3, 0.2e-6)
