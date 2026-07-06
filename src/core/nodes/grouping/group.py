def group(state: dict):
    dictionary = {}
    tempscript = []
    tempgrouped = []

    script = state['script']

    for words in script:
        tempscript.append(words)

    for elements in state['grouped']:
        tempgrouped.append(elements['text'])

    for w in tempgrouped:
        for word in w.split():
            for ts in tempgrouped:
                if word in ts.split():
                        dictionary[word] = word
                else:
                    print('Provided grouped script does not match with Script')
                                    
    return dictionary


state = {'script':['Not a Misunderstanding'],
         'grouped':[{'id':1,'text':'This is'},{'id':2,'text':'nothing but a'},{'id':3,'text':'misunderstanding'}]}

d = group(state)
print(d)