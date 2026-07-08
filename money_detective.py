import pandas as pd

# ---------------------------------------
# Money Detective
# Lecture 7 Assignment
# ---------------------------------------

df = pd.read_csv("transactions.csv")

expenses = df[df["Amount"] < 0].copy()

expenses["Category"] = "Other"

keywords = {
    "Subscription": [
        "Netflix",
        "Spotify",
        "Adobe",
        "Google One"
    ],
    "Food": [
        "McDonalds",
        "KFC",
        "Foodpanda"
    ],
    "Transport": [
        "Uber"
    ],
    "Bills": [
        "Electricity"
    ],
    "Shopping": [
        "Amazon",
        "Steam"
    ]
}

for category, words in keywords.items():
    for word in words:
        expenses.loc[
            expenses["Description"].str.contains(word, case=False),
            "Category"
        ] = category

print("=" * 60)
print("              MONEY DETECTIVE REPORT")
print("=" * 60)

print("\nTOTAL SPENDING")

total_spent = abs(expenses["Amount"].sum())
print(f"${total_spent:.2f}")

print("\n")

print("=" * 60)
print("SPENDING BY CATEGORY")
print("=" * 60)

category_totals = (
    expenses.groupby("Category")["Amount"]
    .sum()
    .abs()
    .sort_values(ascending=False)
)

for category, amount in category_totals.items():
    print(f"{category:<20} ${amount:.2f}")

print("\n")

print("=" * 60)
print("RECURRING CHARGES")
print("=" * 60)

recurring = (
    expenses.groupby("Description")
    .size()
    .sort_values(ascending=False)
)

for desc, count in recurring.items():
    if count > 1:
        print(f"{desc:<25} {count} payments")

print("\n")

print("=" * 60)
print("POSSIBLE DUPLICATE PAYMENTS")
print("=" * 60)

duplicates = expenses[
    expenses.duplicated(
        subset=["Description", "Amount"],
        keep=False
    )
]

if duplicates.empty:
    print("No duplicate payments found.")
else:
    print(
        duplicates[
            ["Date", "Description", "Amount"]
        ].to_string(index=False)
    )

print("\n")

print("=" * 60)
print("TOP 5 LARGEST EXPENSES")
print("=" * 60)

largest = (
    expenses.sort_values("Amount")
    .head(5)
)

print(
    largest[
        ["Date", "Description", "Amount"]
    ].to_string(index=False)
)

print("\n")

print("=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"Transactions Analysed : {len(df)}")
print(f"Expense Transactions  : {len(expenses)}")
print(f"Income Transactions   : {len(df[df['Amount'] > 0])}")
print(f"Recurring Charges     : {(recurring > 1).sum()}")
print(f"Duplicate Entries     : {len(duplicates)}")
print(f"Total Spending        : ${total_spent:.2f}")

print("=" * 60)
