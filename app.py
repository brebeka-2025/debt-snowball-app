# First pass: calculate minimums for all unpaid debts
min_payments = []
for i in active_debts.index:
    if active_debts.at[i, "Balance"] > 0:
        min_payments.append(min(active_debts.at[i, "Minimum Payment"], active_debts.at[i, "Balance"]))
    else:
        min_payments.append(0)

remaining_budget = total_budget - sum(min_payments)

# Apply payments
for i in active_debts.index:
    if active_debts.at[i, "Balance"] <= 0:
        continue

    rate = active_debts.at[i, "Interest Rate (%)"] / 100 / 12
    interest = active_debts.at[i, "Balance"] * rate
    min_payment = min_payments[i]

    # Add snowball only to first unpaid
    if i == active_debts[active_debts["Balance"] > 0].index[0]:
        payment = min(min_payment + remaining_budget, active_debts.at[i, "Balance"] + interest)
    else:
        payment = min_payment

    principal = max(payment - interest, 0)
    new_balance = max(active_debts.at[i, "Balance"] - principal, 0)

    # Save row
    snowball_rows.append({
        "Month": month_name,
        "Debt Name": active_debts.at[i, "Debt Name"],
        "Starting Balance": active_debts.at[i, "Balance"],
        "Interest": round(interest, 2),
        "Principal": round(principal, 2),
        "Payment": round(payment, 2),
        "Ending Balance": round(new_balance, 2)
    })

    active_debts.at[i, "Balance"] = new_balance
