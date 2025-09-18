guests = ["Kendall", "nick", "Cam", "Fiona", "Angel", "manman"] 

print("Unfortunately, the new dinner table won’t arrive in time for the dinner, so I can only invite two people.\n")

while len(guests) > 2:
    removed_guest = guests.pop()
    print(f"Sorry, {removed_guest}, I can’t invite you to dinner.") 

for guest in guests:
    print(f"Hi {guest}, you are still invited to dinner at my place!")

del guests[0]
del guests[0]

print("Final guest list:", guests)