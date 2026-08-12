# Version 0.1

print("AI IT Support Assistant")
print("-----------------------")

problem = input("Describe your IT problem: ")

print("\nYou reported:")
print(problem)

print("\nInitial analysis:")

if "wifi" in problem.lower() or "wi-fi" in problem.lower() or "internet" in problem.lower():
    print("Category: Network")
    print("Suggested first step: Check network connectivity and DNS.")
    print("Category: Network")
   
elif "password" in problem.lower() or "login" in problem.lower():
    print("Category: Authentication")
    print("Suggested first step: Verify credentials and account status.")
else:
    print("Category: General IT Support")
    print("Suggested first step: Gather additional information about the problem.")