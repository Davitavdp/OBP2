#Assignment 2A

import streamlit as st
import numpy as np

st.title("Calculate fraction of time that the system is up")

#Input
failure_rate = st.number_input("Failure rate:", value=0.5)
repair_rate = st.number_input("Repair rate:", value=0.8)
No_components = st.number_input("Number of Components:", value=3)
No_components_to_func = st.number_input("Number of Components for system to function:", value=2)
No_repairman = st.number_input("Number of Repairman:", value=1)
Warm_or_Cold = st.selectbox('Select the Stand-by:', ('Warm', 'Cold'))


def power_method(P, max_iter=1000):
    n = len(P)
    pi = [1.0 / n] * n

    for _ in range(max_iter):
        new_pi = [sum(P[j][i] * pi[j] for j in range(n)) for i in range(n)]
        pi = new_pi
    return pi

def create_stationary(No_components, No_components_to_func,No_repairman, failure_rate, repair_rate, Warm_or_Cold ):
    states = range(No_components+1)
    Q = np.zeros((No_components+1, No_components+1))

    if No_components_to_func > No_components:
        st.error("ERROR: k should not be bigger than n")

    for i in states:
        if Warm_or_Cold == 'Warm':
            failure = failure_rate * (i)
        elif i < No_components_to_func:
            failure = 0
        else:
            failure = failure_rate * No_components_to_func
        repair = min(No_repairman, No_components-i) * repair_rate

        if i < No_components and i != 0:
            Q[i][i - 1] = failure
            Q[i][i + 1] = repair
        elif i == 0:
            Q[i][i + 1] = repair
        elif i == No_components:
            Q[i][i - 1] = failure

        Q[i][i] = -sum(Q[i])
    lambda_max = max(-Q[i][i] for i in range(No_components+1))
    P = []

    for i in range(No_components + 1):
        row = []
        for j in range(No_components + 1):
            #On the diagonals we add 1 to make the sum of the row 0.
            if i == j:
                row.append(1 + Q[i][i] / lambda_max)
            else:
                #Transition/Total sum competing exponentials
                row.append(Q[i][j] / lambda_max)
        P.append(row)

    stationary_dist = power_method(P)
    return stationary_dist

stationary_dist = create_stationary(No_components, No_components_to_func, No_repairman, failure_rate, repair_rate, Warm_or_Cold)
y = sum(stationary_dist[No_components_to_func:No_components+1])

st.write("### The fraction of the time the system is up:", y)