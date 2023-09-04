# Generate 3 random integers between 100 and 999 which is divisible by 5
from random import randrange

random_integers = set()
for num in range(3):
    random_integers.add(randrange(100,999,5))

print(random_integers)

# Lottery tickets
import random

lottery_ticket_list = set()

for i in range(100):
    lottery_ticket_list.add(randrange(1000000000,9999999999))

winners = random.sample(lottery_ticket_list,2)
print(winners)
print(lottery_ticket_list)