def main():
    dict1 = {"first":1,"second":2,"third":3,"fourth":4,"fifth":5}
    string = "sixth"
    if string not in dict1:
        dict1[string] = 6
    print(dict1)
main()
