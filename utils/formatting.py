
def freq_dict_to_percent_dict(d):
    for key in d.keys():
        value = d[key]
        d[key] = "{0:.2f}%".format(value * 100)
    return d
