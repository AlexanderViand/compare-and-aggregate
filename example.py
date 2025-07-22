

def swap(condition, target, truevalue, falsevalue):
    if condition:
        target = truevalue
    else:
        target = falsevalue

def foo(a,b, l):

    if a < b:
        z = a
        l[i] = l[i+1]
        # this would be bad:
        if l[i] < l[i-1]:
            l[i] = l[i-1]
    else:
        z = b
        l[i] = l[i-1]

    # swap(a<b, l[i], l[i+1],l[i-1])