import custom_trig as trig

x = 0
print(f"sin(0) = {trig.sin(x)}")
print(f"cos(0) = {trig.cos(x)}")
print(f"tan(0) = {trig.tan(x)}")

#assert trig.sin(x) == 0.5, "sin(x) doesn't work"
x = trig.pi/2
print(f"sin(0) = {trig.sin(x)}")
print(f"cos(0) = {trig.cos(x)}")
print(f"tan(0) = {trig.tan(x)}")

# this should print 0, 1, 0
#print(trig.sin(0), trig.cos(0), trig.tan(0))
# this should print 1, 0, inf (or something close to it)
#print(trig.sin(trig.pi/2), trig.cos(trig.pi/2), trig.tan(trig.pi/2))