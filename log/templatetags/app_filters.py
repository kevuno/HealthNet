from django import template

register = template.Library()


@register.filter(name='index')
def index(sequence, position):
    """
    Tag for statistics.html because you can't use 'advanced' logic in templates
    :param sequence: num_patients_in_each_hospital
    :param position: forloop.counter0
    :return:
    """
    return sequence[position]

@register.filter(name='checkNext')
def check_next(sequence, position):
    """
    Tag that checks if the next element in an array is equal to the current one
    :param sequence: list_of_days
    :param position: forloop.counter0
    :return:
    """
    try:
        if sequence[position] == sequence[position+1]:
            return True
        else:
            return False
    except IndexError:
        return False

@register.filter(name='getCount')
def get_count(sequence, position):
    """
    Tag that counts the number of times a day is repeated in the log
    :param sequence: list_of_days
    :param position: forloop.counter0
    :return:
    """
    count = 1
    #print(len(sequence))
    #print(position)
    startingIndex = 0

    # find starting index where the current position technically starts
    for i in range(0, len(sequence)):
        if sequence[i] == sequence[position]:
            startingIndex = i
            break

    # iterate up until the current position and increment the occurrences
    for j in range(startingIndex, position):
        count += 1

    return count
