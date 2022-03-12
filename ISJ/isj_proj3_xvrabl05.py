#!/usr/bin/env python3

# ukol za 2 body
def first_odd_or_even(numbers):
    """Returns 0 if there is the same number of even numbers and odd numbers
       in the input list of ints, or there are only odd or only even numbers.
       Returns the first odd number in the input list if the list has more even
       numbers.
       Returns the first even number in the input list if the list has more odd 
       numbers.

    >>> first_odd_or_even([2,4,2,3,6])
    3
    >>> first_odd_or_even([3,5,4])
    4
    >>> first_odd_or_even([2,4,3,5])
    0
    >>> first_odd_or_even([2,4])
    0
    >>> first_odd_or_even([3])
    0
    """
    counter = 0
    fodd = -1
    feven = -1
    for i in numbers:
        if(i % 2 == 1):
            if fodd == -1:
                fodd = i
            counter = counter + 1
        else:
            if feven == -1:
                feven = i
            counter = counter - 1
    if fodd == -1:
        return 0
    if feven == -1:
        return 0

    if counter < 0:
        return fodd
    elif counter > 0:
        return feven
    else:
        return 0

# ukol za 3 body
def to_pilot_alpha(word):
    """Returns a list of pilot alpha codes corresponding to the input word

    >>> to_pilot_alpha('Smrz')
    ['Sierra', 'Mike', 'Romeo', 'Zulu']
    """

    pilot_alpha = ['Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot',
        'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'Lima', 'Mike',
        'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango',
        'Uniform', 'Victor', 'Whiskey', 'Xray', 'Yankee', 'Zulu']

    pilot_alpha_list = []
    for j in word:
        for i in pilot_alpha:
            if i[0] == j.upper():
                pilot_alpha_list.append(i);
    
    return pilot_alpha_list


if __name__ == "__main__":
    import doctest
    doctest.testmod()
