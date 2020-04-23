def flagger(data):
    for i in data['Country']:
        count = data['Country'].count(i)
        if count/len(data['Country']) < .10:
            data['Flagged'].append("0000")

    for i in data['Location']:
        count = data['Location'].count(i)
        if count/len(data['Location']) < .10:
            data['Flagged'].append("0000")

    for i in data['Number of Strikes']:
        count = data['Number of Strikes'].count(i)
        if count/len(data['Number of Strikes']) < .10:
            data['Flagged'].append("0000")

    for i in data['Number of Units']:
        count = data['Number of Units'].count(i),
        if count/len(data['Number of Units']) < .10:
            data['Flagged'].append("0000")

    for i in data['Unit']:
        count = data['Unit'].count(i)
        if count/len(data['Unit']) < .10:
            data['Flagged'].append("0000")

            

#    if count/len(data['Number of Units']) < .10:
# TypeError: unsupported operand type(s) for /: 'tuple' and 'int'