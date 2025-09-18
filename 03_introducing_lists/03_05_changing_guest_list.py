guests = ["Kendall", "Nick", "Cam"]

for guest in guests:
    print(f"Hi {guest}, you are invited to the dorm!")

    cantmakeit = "Kendall"
    print(f"\nunfortuantely, {cantmakeit} can't make it to the dinner.\n")

    index_to_replace = guests.index(cantmakeit)
    guests[index_to_replace] = 'Kareem'

for guest in guests:
    print(f"Hi {guest}, you are invited to the dorm!")
