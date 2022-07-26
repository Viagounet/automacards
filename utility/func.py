def parse(ctx):
    string = ctx.triggered[0]["prop_id"].split(".")[0]
    index = string.split("{\"index\":\"")[1].split("\",")[0]
    type = string.split("type\":\"")[1].replace("\"}", "")
    return type, index
