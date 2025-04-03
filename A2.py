import streamlit as st
import numpy as np
import scipy.linalg


def generate_transition_matrix(n, k, mu, gamma, warm_standby, repairmen):
    """
    Generates the transition rate matrix for the k-out-of-n system.
    """
    size = n + 1  #State space: 0 (all failed) to n (all working)
    Q = np.zeros((size, size))

    for i in range(size):
        #Failure transitions (downward)
        if i > 0:
            failure_rate = i * mu  # Only working components fail
            Q[i, i - 1] = failure_rate

        #Repair transitions (upward)
        if i < n:
            num_repairs = min(i, repairmen)  # Repairmen limit
            repair_rate = num_repairs * gamma
            Q[i, i + 1] = repair_rate

        #Set diagonal elements
        Q[i, i] = -np.sum(Q[i, :])
    return Q


def compute_stationary_distribution(Q):
    """
    Computes the stationary distribution by solving Q * pi = 0.
    """
    Q[-1, :] = 1  # Replace last row for normalization constraint
    b = np.zeros(Q.shape[0])
    b[-1] = 1
    pi = np.linalg.lstsq(Q.T, b, rcond=None)[0]
    return pi


def main():
    st.title("k-out-of-n System Availability Calculator")

    #Inputs
    mu = st.number_input("Failure Rate (per component)", min_value=0.0001, value=0.1)
    gamma = st.number_input("Repair Rate (per component)", min_value=0.0001, value=0.5)
    warm_standby = st.radio("Are unused components in warm standby?", ("Yes", "No"))
    warm_standby = warm_standby == "Yes"
    n = st.number_input("Total Number of Components (n)", min_value=1, value=5, step=1)
    k = st.number_input("Minimum Components for Functionality (k)", min_value=1, value=3, step=1)
    repairmen = st.number_input("Number of Repairmen", min_value=1, value=2, step=1)

    if st.button("Calculate Availability"):
        Q = generate_transition_matrix(n, k, mu, gamma, warm_standby, repairmen)
        pi = compute_stationary_distribution(Q)

        #Compute system availability
        availability = sum(pi[k:])  #Sum probabilities where system is operational

        st.write(f"### Fraction of Time System is Up: {availability:.4f}")
        # st.bar_chart(pi)  #Show probability distribution


if __name__ == "__main__":
    main()


#streamlit run /Users/davita/PycharmProjects/OBP2/A2.py [ARGUMENTS]