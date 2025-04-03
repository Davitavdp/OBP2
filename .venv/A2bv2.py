import streamlit as st
import numpy as np

st.title("Optimal number of components and repairmen")

#Input fields
failure_rate = st.number_input("Failure rate:", value=0.5, step=0.1)
repair_rate = st.number_input("Repair rate:", value=0.8, step=0.1)
No_components_to_func = st.number_input("Number of Components for system to function:", value=2)
Warm_or_Cold = st.selectbox('Select the Stand-by:', ('Warm', 'Cold'))
cost_per_component = st.number_input("Cost per Component:", value=3.0, step=1.0)
cost_per_repairman = st.number_input("Cost per Repairman:", value=10.0, step=5.0)
downtime_cost = st.number_input("Downtime Cost:", value=100.0, step=10.0)


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
        repair = min(No_repairman, No_components - i) * repair_rate

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


max_components = No_components_to_func+15
current_y = 0
optimal_y = 0
optimal_nr_components = No_components_to_func
optimal_nr_repairmen = 1
optimal_cost = float("inf")

for n in range(No_components_to_func,max_components+1):
    max_repairmen = n
    for m in range(1,max_repairmen+1):
        stationary_dist = create_stationary(n, No_components_to_func, m, failure_rate,
                                            repair_rate, Warm_or_Cold)
        current_y = sum(stationary_dist[No_components_to_func:n+1])
        current_cost = cost_per_component*n + cost_per_repairman*m + downtime_cost*(1-current_y)

        if current_cost <= optimal_cost:
            optimal_cost = current_cost
            optimal_y = current_y
            optimal_nr_components = n
            optimal_nr_repairmen = m


st.write(f"### The minimum cost is: {optimal_cost}")
st.write(f"Optimal number of components: {optimal_nr_components}")
st.write(f"Optimal number of repairmen: {optimal_nr_repairmen}")
st.write(f"### The fraction of time the system is up: {optimal_y:.4f}")

#streamlit run /Users/davita/PycharmProjects/OBP2/.venv/A2bv2.py [ARGUMENTS]