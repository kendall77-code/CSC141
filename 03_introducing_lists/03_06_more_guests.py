guests = ["Kendall", "Dominick", "Maine"]

for guest in guests:
    print(f"Hi {guest}, you are invited to dinner at my place!")

cantmakeit = "Dominick"
print(f"\nUnfortunately, {cantmakeit} can’t make it to the dinner.\n")

guests[guests.index(cantmakeit)] = "Kareem"

for guest in guests:
    print(f"Hi {guest}, you are still invited to dinner at my place!")

print("\nGood news! I found a bigger dinner table, so more guests are invited!\n")
insertbeginning = "Fiona"
insertmiddle = "Angel"
appendend = "Fatman"
guests.insert(0, insertbeginning)
guests.insert(2, insertmiddle)
guests.append(appendend)
for guest in guests:
    print(f"Hi {guest}, you are invited to dinner at my place!")