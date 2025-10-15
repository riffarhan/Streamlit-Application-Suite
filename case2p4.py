import streamlit as st
import os  # using this just to check if the log file exists (simple + clear)

st.title("🧾 Singapore Cash Receipting App")

# --- Session state ---
# keep this so the app doesn't crash the first time we reference receiptNo
if "receiptNo" not in st.session_state:
    st.session_state.receiptNo = 10000

# --- Inputs ---
amount_payable = st.number_input("Enter Amount Payable (SGD)", min_value=0.00, format="%.2f")
amount_tendered = st.number_input("Enter Amount Tendered (SGD)", min_value=0.00, format="%.2f")

# NOTE: adding a single action button so we log exactly once per transaction.
# in P2 it would "auto" run and could write multiple times when someone nudges inputs.
if st.button("Calculate & Record"):
    # --- basic guardrail ---
    if amount_tendered < amount_payable:
        st.error("Amount tendered is less than amount payable. Please enter a valid amount.")
        st.stop()

  # Convert dollars to integer cents to avoid floating-point precision issues
    def to_cents(x: float) -> int:
        return int(round(x * 100))

    payable_cents = to_cents(amount_payable)
    tendered_cents = to_cents(amount_tendered)
    change_cents = tendered_cents - payable_cents

    # Round change down to the nearest 5 cents (smallest legal denomination in SGD)
    remainder = change_cents % 5
    if remainder != 0:
        # be conservative: floor down to nearest 5c we can actually dispense
        change_cents -= remainder

    change = change_cents / 100.0
    st.success(f"Change to be returned: ${change:.2f}")

    # if exact amount, no need to spam the breakdown sections
    if change_cents == 0:
        st.info("Exact amount received. No change to dispense.")
    else:
        # --- Notes (keep the P2 look) ---
        st.subheader("💵 Notes Dispensed")

        remaining = change_cents 

        note_50 = remaining // 5000
        remaining -= note_50 * 5000
        if note_50 > 0:
            st.write(f"{note_50} × $50 note")

        note_10 = remaining // 1000
        remaining -= note_10 * 1000
        if note_10 > 0:
            st.write(f"{note_10} × $10 note")

        note_5 = remaining // 500
        remaining -= note_5 * 500
        if note_5 > 0:
            st.write(f"{note_5} × $5 note")

        note_2 = remaining // 200
        remaining -= note_2 * 200
        if note_2 > 0:
            st.write(f"{note_2} × $2 note")

        # --- Coins (keep the P2 look) ---
        st.subheader("🪙 Coins Dispensed")

        coin_1 = remaining // 100
        remaining -= coin_1 * 100
        if coin_1 > 0:
            st.write(f"{coin_1} × $1 coin")

        coin_050 = remaining // 50
        remaining -= coin_050 * 50
        if coin_050 > 0:
            st.write(f"{coin_050} × $0.50 coin")

        coin_020 = remaining // 20
        remaining -= coin_020 * 20
        if coin_020 > 0:
            st.write(f"{coin_020} × $0.20 coin")

        coin_010 = remaining // 10
        remaining -= coin_010 * 10
        if coin_010 > 0:
            st.write(f"{coin_010} × $0.10 coin")

        coin_005 = remaining // 5
        remaining -= coin_005 * 5
        if coin_005 > 0:
            st.write(f"{coin_005} × $0.05 coin")

        # Any leftover at this point indicates a logic error
        if remaining != 0:
            st.warning("Tiny rounding remainder couldn’t be dispensed (should be 0).")

    # --- Logging (collections.txt) ---
    filename = "collections.txt"
    # log line uses current receiptNo; we will bump the number only after a successful write
    line = f"{st.session_state.receiptNo},{amount_payable:.2f},{amount_tendered:.2f},{change:.2f}\n"

    try:
        # Create file and header if it does not already exist    
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("Receipt No, Amount Payable, Amount Tendered, Change\n")

        # append the record
        with open(filename, "a") as f:
            f.write(line)

        # Increment receipt number only after successful write
        st.session_state.receiptNo += 1
        st.success("Transaction recorded to collections.txt ✅")

    except Exception as e:
        st.error(f"Failed to record transaction: {e}")
