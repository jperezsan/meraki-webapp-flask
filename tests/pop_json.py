my_list = ["pedro", "maria", "juan"]
print(len(my_list))
if len(my_list) >= 3:
    removed = my_list.pop(0)
    print(removed)
    print(my_list)
    print(len(my_list))
my_list.append("Gabo")
print(len(my_list))
print(my_list)

