grocery_list = ["apples", "bread", "milk", "eggs", "bannas"]

grocery_list.append("beans")
grocery_list.remove("bread")
grocery_list.sort()

print("Updated Grocery List:")
for item in grocery_list:
    print(item)