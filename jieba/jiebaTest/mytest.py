fi = open('gram7-past-tense.txt', 'r')
fi2 = open('gram7-past-tense2.txt', 'w')
i = 1
for line in fi:
    li = line.split(' ')
    if len(li) != 4:
        print len(li), '//////////////////////', i
        print li
        continue
    i += 1
    fi2.write(' '.join(li))

fi.close()
fi2.close()
