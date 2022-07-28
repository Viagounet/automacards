from math import log


def parse(ctx):
    string = ctx.triggered[0]["prop_id"].split(".")[0]
    index = string.split("{\"index\":\"")[1].split("\",")[0]
    type = string.split("type\":\"")[1].replace("\"}", "")
    return type, index


def level_mapping(score):
    if score < 0:
        return 0
    return int(log(score + 1, 3))
