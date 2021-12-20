try:
    name, surname = input().split()
except ValueError:
    print("You need to enter exactly 2 words. Try again!")
except Exception as e:
    print(e,str(e), e.__class__)
else:
    print("Welcome to our party,",name,surname)