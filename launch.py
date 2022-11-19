from flight import Plain, pif, crashReport

if __name__ == "__main__":
    pln = Plain(name='Самолет')
    print(pln.name)
    crashReport()
    pif(0, 0, 0)
    pass