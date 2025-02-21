import cmath
import math
import numpy as np
import matplotlib.pyplot as plt
import gui


def rlc(resistance, inductance, capacitance, initial_capacitor_voltage, initial_inductor_current, choice, graphic_choice):

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

    if choice == 1:

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

            print(f"x(t) = {A1:.2f}e^({s_1.real:.2f}t) + {A2:.2f}e^({s_2.real:.2f}t)")

        if damped == 2:
            B1 = initial_capacitor_voltage
            w_d = math.sqrt(res_freq_squared - neper_freq_square)
            B2 = (derivative_of_vc + (neper_freq * B1)) / w_d

            print(f"x(t) = ({B1:.2f}cos({w_d:.2f}*t) + {B2:.2f}sin({w_d:.2f}*t))e^-{neper_freq:.2f}t")

        if damped == 3:
            D2 = initial_capacitor_voltage
            D1 = derivative_of_vc + (neper_freq * D2)

            print(f"x(t) = ({D1:.2f}t + {D2})e^-{neper_freq}t)")

    elif choice == 2:  # Serial RLC circuite

        derivative_of_il = -((initial_inductor_current * resistance) + initial_capacitor_voltage) / inductance

        if damped == 1:  # over-damp

            # Coefficients matrix
            A = np.array([[1, 1],
                          [s_1.real, s_2.real]])  # Use real parts

            # Constants matrix
            B = np.array([initial_inductor_current, derivative_of_il])

            # Solving for [x, y]
            solution = np.linalg.solve(A, B)

            A1, A2 = solution

            print(f"x = {A1}, y = {A2}")

            print(f"x(t) = {A1:.2f}e^({s_1.real:.2f}t) + {A2:.2f}e^({s_2.real:.2f}t)")

        elif damped == 2:  # under-damp

            B1 = initial_inductor_current
            w_d = math.sqrt(res_freq_squared - neper_freq_square)
            B2 = (derivative_of_il + (neper_freq * B1)) / w_d

            print(f"I(t) = ({B1:.2f}cos({w_d:.2f}*t) + {B2:.2f}sin({w_d:.2f}*t))e^-{neper_freq:.2f}t A")

        elif damped == 3:  # critical-damp
            D2 = initial_inductor_current
            D1 = derivative_of_il + (neper_freq * D2)

            print(f"x(t) = ({D1:.2f}t + {D2})e^-{neper_freq:.2f}t)")

    # Graphing
    if graphic_choice == 1:

        if damped == 1:  # Over-damped
            end_time = 5 * (1 / neper_freq)
        elif damped == 2:  # Under-damped
            end_time = 3 * (2 * np.pi / res_freq)
        else:  # Critically damped
            end_time = 5 * (1 / neper_freq)

        t = np.linspace(0, end_time, 1000)  # initialize time axis
        response = np.zeros_like(t)  # initilize a zero response to not get an error if the response is not updated with the damping conditions

        # Y axis, response.
        if damped == 1:  # Over-damped response
            response = A1 * np.exp(s_1.real * t) + A2 * np.exp(s_2.real * t)
        elif damped == 2:  # Under-damped response
            response = (B1 * np.cos(w_d * t) + B2 * np.sin(w_d * t)) * np.exp(-neper_freq * t)
        elif damped == 3:  # Critically damped response
            response = (D1 * t + D2) * np.exp(-neper_freq * t)

        # Plot the response
        plt.figure(figsize=(10, 5))
        plt.plot(t, response)
        plt.title('RLC Circuit Response')
        plt.xlabel('Time (s)')
        plt.ylabel('Response')
        plt.grid()
        plt.show()


#rlc(9, 50e-3, 0.2e-6)
#rlc(200,50e-3,0.2e-6)
