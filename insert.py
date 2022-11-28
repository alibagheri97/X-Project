from sup import sup
import os
    
file = open("test.service", "r")
val = file.read()
file.close()
lst = sup(val, "$")
cwd = os.getcwd() + "/"
final = lst[0] + cwd + lst[1] + cwd + lst[-1]
file = open("test.service", "w")
file.write(final)
file.close()
