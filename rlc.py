import cmath
import math
import numpy as np


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

        derivative_of_vc = -(initial_inductor_current + (initial_capacitor_voltage/resistance)) / capacitance

    elif choice == 2:
        print("choice 2")

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

        print(f"x(t) = {A1:.2f}exp(pow(e,{s_1.real:.2f}*t)) + {A2:.2f}.exp(pow(e,{s_2.real:.2f}t))")

    if damped == 2:
        B1 = initial_capacitor_voltage
        w_d = math.sqrt(res_freq_squared - neper_freq_square)
        B2 = (derivative_of_vc + (neper_freq * B1)) / w_d

        print(B2)

        print(f"{B1:.2f}cos({w_d}*t) + {B2:.2f}sin({w_d}*t) ) e^-{neper_freq}t")





rlc(20e3, 8, 0.125e-6)
