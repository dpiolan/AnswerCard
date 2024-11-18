
Debug = True
UseJSONTemplate = True

JSONPath = "test.json"

BaseSize = [1680,2376]

StudentNumberParseMode = "pyzbar"

StudentNumberNum = 10

PreSupposePos = [[250,550],[600,900],[950,1250],[1300,1600]]

Template = [
    {
        "Name" : "BarCode",
        "count" : 1
    },
    {
        "Name" : "Question_1",
        "count" : 4
    },
    {
        "Name": "Question_2",
        "count": 2
    }
]