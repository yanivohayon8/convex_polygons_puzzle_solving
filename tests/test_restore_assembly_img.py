import unittest
from src.physics import restore_assembly_img
from src.recipes.puzzle import loadRegularPuzzle
import matplotlib.pyplot as plt
import random
from shapely.geometry import Polygon
from shapely import affinity

def plot_polygons(polygons, ax = None,seed = 10):
    if ax is None:
        _,ax = plt.subplots()
    
    random.seed(seed)

    for poly in polygons:
        xs,ys = poly.exterior.xy
        ax.fill(xs,ys, alpha=0.5,fc=(random.random(),random.random(),random.random()),ec="black")

    ax.set_aspect("equal")

class Test19_DB1(unittest.TestCase):

    assembly_json_19_DB1 = {
            "AfterEnableCollision": {
                "springs": [
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 1,
                        "secondPieceId": "9",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 10.142101287841797
                    },
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 2,
                        "secondPieceId": "9",
                        "secondPieceVertex": 3,
                        "snapshotedLength": 11.260101318359375
                    },
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 0,
                        "secondPieceId": "8",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 20.635299682617188
                    },
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 1,
                        "secondPieceId": "8",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 20.327173233032227
                    },
                    {
                        "firstPieceId": "8",
                        "firstPieceVertex": 1,
                        "secondPieceId": "9",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 15.948013305664063
                    },
                    {
                        "firstPieceId": "8",
                        "firstPieceVertex": 2,
                        "secondPieceId": "9",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 14.22866153717041
                    },
                    {
                        "firstPieceId": "6",
                        "firstPieceVertex": 1,
                        "secondPieceId": "9",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 13.986743927001953
                    },
                    {
                        "firstPieceId": "6",
                        "firstPieceVertex": 2,
                        "secondPieceId": "9",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 15.092012405395508
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 2,
                        "secondPieceId": "8",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 7.531733989715576
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 3,
                        "secondPieceId": "8",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 12.917973518371582
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 2,
                        "secondPieceId": "6",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 15.013673782348633
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 3,
                        "secondPieceId": "6",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 14.896913528442383
                    },
                    {
                        "firstPieceId": "4",
                        "firstPieceVertex": 1,
                        "secondPieceId": "6",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 9.381514549255371
                    },
                    {
                        "firstPieceId": "4",
                        "firstPieceVertex": 2,
                        "secondPieceId": "6",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 11.278538703918457
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 3,
                        "secondPieceId": "0",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 17.220252990722656
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 0,
                        "secondPieceId": "0",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 17.102039337158203
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 0,
                        "secondPieceId": "1",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 11.324124336242676
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 1,
                        "secondPieceId": "1",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 11.957756996154785
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 1,
                        "secondPieceId": "5",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 11.744946479797363
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 2,
                        "secondPieceId": "5",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 10.237936973571777
                    },
                    {
                        "firstPieceId": "2",
                        "firstPieceVertex": 1,
                        "secondPieceId": "5",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 21.767284393310547
                    },
                    {
                        "firstPieceId": "2",
                        "firstPieceVertex": 2,
                        "secondPieceId": "5",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 21.589750289916992
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 0,
                        "secondPieceId": "4",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 10.96021556854248
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 1,
                        "secondPieceId": "4",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 8.148117065429688
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 2,
                        "secondPieceId": "2",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 19.059406280517578
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 0,
                        "secondPieceId": "2",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 14.149581909179688
                    },
                    {
                        "firstPieceId": "1",
                        "firstPieceVertex": 1,
                        "secondPieceId": "2",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 12.62522029876709
                    },
                    {
                        "firstPieceId": "1",
                        "firstPieceVertex": 2,
                        "secondPieceId": "2",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 18.883333206176758
                    }
                ],
                "sumSpringsLength": 386.0
            },
            "piecesBeforeEnableCollision": [
                {
                    "coordinates": [
                        [
                            1930.1241455078125,
                            478.7597351074219
                        ],
                        [
                            1529.546630859375,
                            245.06185913085938
                        ],
                        [
                            -16.576766967773438,
                            682.7735595703125
                        ],
                        [
                            678.8386840820313,
                            1548.4256591796875
                        ]
                    ],
                    "pieceId": "0"
                },
                {
                    "coordinates": [
                        [
                            1936.2601318359375,
                            488.2793273925781
                        ],
                        [
                            1865.0911865234375,
                            -451.6658630371094
                        ],
                        [
                            1521.1409912109375,
                            236.55889892578125
                        ]
                    ],
                    "pieceId": "1"
                },
                {
                    "coordinates": [
                        [
                            1872.827392578125,
                            -441.6885070800781
                        ],
                        [
                            1479.560791015625,
                            126.71660614013672
                        ],
                        [
                            1503.2862548828125,
                            230.41151428222656
                        ]
                    ],
                    "pieceId": "2"
                },
                {
                    "coordinates": [
                        [
                            1885.993896484375,
                            -436.5062561035156
                        ],
                        [
                            739.084228515625,
                            11.081694602966309
                        ],
                        [
                            1469.1905517578125,
                            110.7234878540039
                        ]
                    ],
                    "pieceId": "3"
                },
                {
                    "coordinates": [
                        [
                            1875.2860107421875,
                            -438.84466552734375
                        ],
                        [
                            -260.4713439941406,
                            -4.7607421875
                        ],
                        [
                            740.8103637695313,
                            3.1185147762298584
                        ]
                    ],
                    "pieceId": "4"
                },
                {
                    "coordinates": [
                        [
                            1513.0748291015625,
                            249.65475463867188
                        ],
                        [
                            1460.519775390625,
                            116.1689682006836
                        ],
                        [
                            742.9752197265625,
                            0.0
                        ],
                        [
                            0.0,
                            678.110107421875
                        ]
                    ],
                    "pieceId": "5"
                },
                {
                    "coordinates": [
                        [
                            732.6068725585938,
                            10.858534812927246
                        ],
                        [
                            -264.0743103027344,
                            -13.422011375427246
                        ],
                        [
                            5.653380870819092,
                            664.3275756835938
                        ]
                    ],
                    "pieceId": "6"
                },
                {
                    "coordinates": [
                        [
                            670.642822265625,
                            1545.0858154296875
                        ],
                        [
                            7.158278942108154,
                            936.2391967773438
                        ],
                        [
                            -379.63482666015625,
                            1472.7401123046875
                        ]
                    ],
                    "pieceId": "7"
                },
                {
                    "coordinates": [
                        [
                            685.2988891601563,
                            1559.6121826171875
                        ],
                        [
                            -12.493132591247559,
                            689.1021118164063
                        ],
                        [
                            -4.0378570556640625,
                            919.2733154296875
                        ]
                    ],
                    "pieceId": "8"
                },
                {
                    "coordinates": [
                        [
                            -2.586364507675171,
                            933.4277954101563
                        ],
                        [
                            -4.985809326171875,
                            675.0316162109375
                        ],
                        [
                            -262.9203796386719,
                            -27.36091423034668
                        ],
                        [
                            -370.9144287109375,
                            1479.865966796875
                        ]
                    ],
                    "pieceId": "9"
                }
            ],
            "piecesFinalCoords": [
                {
                    "coordinates": [
                        [
                            1930.1241455078125,
                            478.7597351074219
                        ],
                        [
                            1529.546630859375,
                            245.06185913085938
                        ],
                        [
                            -16.576766967773438,
                            682.7735595703125
                        ],
                        [
                            678.8386840820313,
                            1548.4256591796875
                        ]
                    ],
                    "pieceId": "0"
                },
                {
                    "coordinates": [
                        [
                            1936.2601318359375,
                            488.2793273925781
                        ],
                        [
                            1865.0911865234375,
                            -451.6658630371094
                        ],
                        [
                            1521.1409912109375,
                            236.55889892578125
                        ]
                    ],
                    "pieceId": "1"
                },
                {
                    "coordinates": [
                        [
                            1872.827392578125,
                            -441.6885070800781
                        ],
                        [
                            1479.560791015625,
                            126.71660614013672
                        ],
                        [
                            1503.2862548828125,
                            230.41151428222656
                        ]
                    ],
                    "pieceId": "2"
                },
                {
                    "coordinates": [
                        [
                            1885.993896484375,
                            -436.5062561035156
                        ],
                        [
                            739.084228515625,
                            11.081694602966309
                        ],
                        [
                            1469.1905517578125,
                            110.7234878540039
                        ]
                    ],
                    "pieceId": "3"
                },
                {
                    "coordinates": [
                        [
                            1875.2860107421875,
                            -438.84466552734375
                        ],
                        [
                            -260.4713439941406,
                            -4.7607421875
                        ],
                        [
                            740.8103637695313,
                            3.1185147762298584
                        ]
                    ],
                    "pieceId": "4"
                },
                {
                    "coordinates": [
                        [
                            1513.0748291015625,
                            249.65475463867188
                        ],
                        [
                            1460.519775390625,
                            116.1689682006836
                        ],
                        [
                            742.9752197265625,
                            0.0
                        ],
                        [
                            0.0,
                            678.110107421875
                        ]
                    ],
                    "pieceId": "5"
                },
                {
                    "coordinates": [
                        [
                            732.6068725585938,
                            10.858534812927246
                        ],
                        [
                            -264.0743103027344,
                            -13.422011375427246
                        ],
                        [
                            5.653380870819092,
                            664.3275756835938
                        ]
                    ],
                    "pieceId": "6"
                },
                {
                    "coordinates": [
                        [
                            670.642822265625,
                            1545.0858154296875
                        ],
                        [
                            7.158278942108154,
                            936.2391967773438
                        ],
                        [
                            -379.63482666015625,
                            1472.7401123046875
                        ]
                    ],
                    "pieceId": "7"
                },
                {
                    "coordinates": [
                        [
                            685.2988891601563,
                            1559.6121826171875
                        ],
                        [
                            -12.493132591247559,
                            689.1021118164063
                        ],
                        [
                            -4.0378570556640625,
                            919.2733154296875
                        ]
                    ],
                    "pieceId": "8"
                },
                {
                    "coordinates": [
                        [
                            -2.586364507675171,
                            933.4277954101563
                        ],
                        [
                            -4.985809326171875,
                            675.0316162109375
                        ],
                        [
                            -262.9203796386719,
                            -27.36091423034668
                        ],
                        [
                            -370.9144287109375,
                            1479.865966796875
                        ]
                    ],
                    "pieceId": "9"
                }
            ],
            "piecesFinalTransformation": [
                {
                    "pieceId": "0",
                    "rotationRadians": -2.657514810562134,
                    "translateVectorX": 928.5106201171875,
                    "translateVectorY": 804.6798095703125
                },
                {
                    "pieceId": "1",
                    "rotationRadians": -18.95050621032715,
                    "translateVectorX": 1774.1640625,
                    "translateVectorY": 91.05681610107422
                },
                {
                    "pieceId": "2",
                    "rotationRadians": -0.8310062289237976,
                    "translateVectorX": 1618.556884765625,
                    "translateVectorY": -28.186796188354492
                },
                {
                    "pieceId": "3",
                    "rotationRadians": 3.585374593734741,
                    "translateVectorX": 1364.755615234375,
                    "translateVectorY": -104.90035247802734
                },
                {
                    "pieceId": "4",
                    "rotationRadians": -9.907032012939453,
                    "translateVectorX": 785.2077026367188,
                    "translateVectorY": -146.82960510253906
                },
                {
                    "pieceId": "5",
                    "rotationRadians": 0.0,
                    "translateVectorX": 0.0,
                    "translateVectorY": 0.0
                },
                {
                    "pieceId": "6",
                    "rotationRadians": -2.453127861022949,
                    "translateVectorX": 158.06198120117188,
                    "translateVectorY": 220.5886688232422
                },
                {
                    "pieceId": "7",
                    "rotationRadians": 1.8316062688827515,
                    "translateVectorX": 99.38811492919922,
                    "translateVectorY": 1318.021728515625
                },
                {
                    "pieceId": "8",
                    "rotationRadians": 6.320694923400879,
                    "translateVectorX": 222.9232635498047,
                    "translateVectorY": 1055.995849609375
                },
                {
                    "pieceId": "9",
                    "rotationRadians": -43.570457458496094,
                    "translateVectorX": -198.01901245117188,
                    "translateVectorY": 764.249755859375
                }
            ]
        }

    assembly_json_wrong_loop_19_DB1 = {
    "AfterEnableCollision": {
        "springs": [
            {
                "firstPieceId": "1",
                "firstPieceVertex": 0,
                "secondPieceId": "7",
                "secondPieceVertex": 0,
                "snapshotedLength": 45.22626495361328
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 1,
                "secondPieceId": "7",
                "secondPieceVertex": 2,
                "snapshotedLength": 44.08641052246094
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "2",
                "secondPieceVertex": 1,
                "snapshotedLength": 13.66238784790039
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 2,
                "secondPieceId": "2",
                "secondPieceVertex": 0,
                "snapshotedLength": 23.023393630981445
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 2,
                "secondPieceId": "3",
                "secondPieceVertex": 2,
                "snapshotedLength": 27.258745193481445
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 0,
                "secondPieceId": "3",
                "secondPieceVertex": 1,
                "snapshotedLength": 29.713163375854492
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 0,
                "secondPieceId": "4",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.962418556213379
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 1,
                "secondPieceId": "4",
                "secondPieceVertex": 2,
                "snapshotedLength": 14.248226165771484
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 1,
                "secondPieceId": "6",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.103209495544434
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 2,
                "secondPieceId": "6",
                "secondPieceVertex": 2,
                "snapshotedLength": 15.100750923156738
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 1,
                "secondPieceId": "1",
                "secondPieceVertex": 2,
                "snapshotedLength": 30.014440536499023
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 2,
                "secondPieceId": "1",
                "secondPieceVertex": 1,
                "snapshotedLength": 27.741790771484375
            }
        ],
        "sumSpringsLength": 286.0
    },
    "piecesBeforeEnableCollision": [
        {
            "coordinates": [
                [
                    813.8789672851563,
                    0.0
                ],
                [
                    0.0,
                    534.4486083984375
                ],
                [
                    805.0174560546875,
                    488.1019287109375
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    -14.177321434020996,
                    564.3272094726563
                ],
                [
                    -85.78681182861328,
                    -124.26375579833984
                ],
                [
                    -217.39385986328125,
                    -215.9957733154297
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    -891.7255249023438,
                    -318.8686218261719
                ],
                [
                    -1.094818115234375,
                    537.6510620117188
                ],
                [
                    -211.64511108398438,
                    -189.35202026367188
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -881.7653198242188,
                    -318.78851318359375
                ],
                [
                    443.28497314453125,
                    1463.4627685546875
                ],
                [
                    12.624739646911621,
                    533.8058471679688
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    453.3824768066406,
                    1463.123291015625
                ],
                [
                    775.0892333984375,
                    490.37548828125
                ],
                [
                    27.700422286987305,
                    532.9341430664063
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    851.285888671875,
                    -25.419233322143555
                ],
                [
                    -76.84135437011719,
                    -113.93355560302734
                ],
                [
                    -36.586761474609375,
                    559.0438842773438
                ]
            ],
            "pieceId": "7"
        }
    ],
    "piecesFinalCoords": [
        {
            "coordinates": [
                [
                    813.8789672851563,
                    0.0
                ],
                [
                    0.0,
                    534.4486083984375
                ],
                [
                    805.0174560546875,
                    488.1019287109375
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    -14.177321434020996,
                    564.3272094726563
                ],
                [
                    -85.78681182861328,
                    -124.26375579833984
                ],
                [
                    -217.39385986328125,
                    -215.9957733154297
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    -891.7255249023438,
                    -318.8686218261719
                ],
                [
                    -1.094818115234375,
                    537.6510620117188
                ],
                [
                    -211.64511108398438,
                    -189.35202026367188
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -881.7653198242188,
                    -318.78851318359375
                ],
                [
                    443.28497314453125,
                    1463.4627685546875
                ],
                [
                    12.624739646911621,
                    533.8058471679688
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    453.3824768066406,
                    1463.123291015625
                ],
                [
                    775.0892333984375,
                    490.37548828125
                ],
                [
                    27.700422286987305,
                    532.9341430664063
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    851.285888671875,
                    -25.419233322143555
                ],
                [
                    -76.84135437011719,
                    -113.93355560302734
                ],
                [
                    -36.586761474609375,
                    559.0438842773438
                ]
            ],
            "pieceId": "7"
        }
    ],
    "piecesFinalTransformation": [
        {
            "pieceId": "1",
            "rotationRadians": 0.0,
            "translateVectorX": 0.0,
            "translateVectorY": 0.0
        },
        {
            "pieceId": "2",
            "rotationRadians": 35.4358024597168,
            "translateVectorX": -105.78536224365234,
            "translateVectorY": 74.68986511230469
        },
        {
            "pieceId": "3",
            "rotationRadians": 68.0147476196289,
            "translateVectorX": -368.1564025878906,
            "translateVectorY": 9.809494018554688
        },
        {
            "pieceId": "4",
            "rotationRadians": 72.03107452392578,
            "translateVectorX": -141.9525146484375,
            "translateVectorY": 559.4940185546875
        },
        {
            "pieceId": "6",
            "rotationRadians": 20.80687141418457,
            "translateVectorX": 418.7240295410156,
            "translateVectorY": 828.8115844726563
        },
        {
            "pieceId": "7",
            "rotationRadians": -47.86832809448242,
            "translateVectorX": 245.9525909423828,
            "translateVectorY": 139.89639282226563
        }
    ]
}

    def test_position_final_assembly_image(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 1
        recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level,is_load_extrapolation_data=False)
        bag_of_pieces = recipe.cook()

        [piece.load_image() for piece in bag_of_pieces]

        positions = restore_assembly_img.position_final_assembly_image(self.assembly_json_19_DB1,bag_of_pieces)

        print(positions)
    
    def test_mask_final_assembly_image(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 1
        recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level,is_load_extrapolation_data=False)
        bag_of_pieces = recipe.cook()

        [piece.load_image() for piece in bag_of_pieces]
        masks = restore_assembly_img.mask_final_assembly_image(self.assembly_json_19_DB1,bag_of_pieces)

        print("finished")

    def test_restore_final_assembly_image(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 1
        recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level,is_load_extrapolation_data=False)
        bag_of_pieces = recipe.cook()
        # bag_of_pieces = bag_of_pieces[]

        [piece.load_image() for piece in bag_of_pieces]

        img = restore_assembly_img.restore_final_assembly_image(self.assembly_json_wrong_loop_19_DB1,bag_of_pieces)

        plt.imshow(img)
        plt.show()
    
    

    def test_draw_polygons(self):
        polygons = [Polygon(piece_json["coordinates"]) for piece_json in self.assembly_json_wrong_loop_19_DB1["piecesFinalCoords"]]
        plot_polygons(polygons)

        plt.show()

class TestToy(unittest.TestCase):

    response_15DBPAST1staged = {
    "AfterEnableCollision": {
        "springs": [
            {
                "firstPieceId": "0",
                "firstPieceVertex": 1,
                "secondPieceId": "4",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.900880813598633
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 2,
                "secondPieceId": "4",
                "secondPieceVertex": 0,
                "snapshotedLength": 12.717195510864258
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 0,
                "secondPieceId": "1",
                "secondPieceVertex": 0,
                "snapshotedLength": 16.989652633666992
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 1,
                "secondPieceId": "1",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.834179878234863
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 0,
                "secondPieceId": "2",
                "secondPieceVertex": 0,
                "snapshotedLength": 13.177959442138672
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 1,
                "secondPieceId": "2",
                "secondPieceVertex": 3,
                "snapshotedLength": 17.292564392089844
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 2,
                "secondPieceId": "8",
                "secondPieceVertex": 1,
                "snapshotedLength": 15.081279754638672
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 3,
                "secondPieceId": "8",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.501011848449707
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 1,
                "secondPieceId": "5",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.954963684082031
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 2,
                "secondPieceId": "5",
                "secondPieceVertex": 2,
                "snapshotedLength": 12.009024620056152
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 0,
                "secondPieceId": "4",
                "secondPieceVertex": 0,
                "snapshotedLength": 12.797148704528809
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 1,
                "secondPieceId": "4",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.883907318115234
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 1,
                "secondPieceId": "9",
                "secondPieceVertex": 0,
                "snapshotedLength": 15.914145469665527
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 2,
                "secondPieceId": "9",
                "secondPieceVertex": 2,
                "snapshotedLength": 13.12105941772461
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 1,
                "secondPieceId": "12",
                "secondPieceVertex": 1,
                "snapshotedLength": 17.76831817626953
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 2,
                "secondPieceId": "12",
                "secondPieceVertex": 0,
                "snapshotedLength": 16.726045608520508
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 0,
                "secondPieceId": "6",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.523397445678711
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 1,
                "secondPieceId": "6",
                "secondPieceVertex": 2,
                "snapshotedLength": 13.743523597717285
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 1,
                "secondPieceId": "13",
                "secondPieceVertex": 2,
                "snapshotedLength": 8.057954788208008
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 2,
                "secondPieceId": "13",
                "secondPieceVertex": 1,
                "snapshotedLength": 24.0550537109375
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "11",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.506077766418457
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 2,
                "secondPieceId": "11",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.5421781539917
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 0,
                "secondPieceId": "8",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.89278793334961
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "8",
                "secondPieceVertex": 2,
                "snapshotedLength": 13.552861213684082
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 1,
                "secondPieceId": "12",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.873885154724121
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 2,
                "secondPieceId": "12",
                "secondPieceVertex": 2,
                "snapshotedLength": 18.87995719909668
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 0,
                "secondPieceId": "10",
                "secondPieceVertex": 0,
                "snapshotedLength": 16.90696907043457
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 1,
                "secondPieceId": "10",
                "secondPieceVertex": 3,
                "snapshotedLength": 19.233386993408203
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 2,
                "secondPieceId": "16",
                "secondPieceVertex": 1,
                "snapshotedLength": 15.58446216583252
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 3,
                "secondPieceId": "16",
                "secondPieceVertex": 0,
                "snapshotedLength": 15.624086380004883
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 1,
                "secondPieceId": "14",
                "secondPieceVertex": 0,
                "snapshotedLength": 13.634718894958496
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 2,
                "secondPieceId": "14",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.55380630493164
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 0,
                "secondPieceId": "11",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.27896499633789
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 1,
                "secondPieceId": "11",
                "secondPieceVertex": 3,
                "snapshotedLength": 15.906221389770508
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 2,
                "secondPieceId": "14",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.034432411193848
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 3,
                "secondPieceId": "14",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.532358169555664
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 1,
                "secondPieceId": "13",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.889525413513184
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 2,
                "secondPieceId": "13",
                "secondPieceVertex": 2,
                "snapshotedLength": 15.000899314880371
            },
            {
                "firstPieceId": "15",
                "firstPieceVertex": 1,
                "secondPieceId": "17",
                "secondPieceVertex": 0,
                "snapshotedLength": 15.734725952148438
            },
            {
                "firstPieceId": "15",
                "firstPieceVertex": 2,
                "secondPieceId": "17",
                "secondPieceVertex": 2,
                "snapshotedLength": 6.6857099533081055
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 1,
                "secondPieceId": "17",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.957154273986816
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 2,
                "secondPieceId": "17",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.163063049316406
            }
        ],
        "sumSpringsLength": 530.0
    },
    "piecesBeforeEnableCollision": [
        {
            "coordinates": [
                [
                    -5699.58447265625,
                    5686.90478515625
                ],
                [
                    19.311904907226563,
                    -77.08930969238281
                ],
                [
                    -5108.20849609375,
                    -1364.488525390625
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    -5632.6767578125,
                    5737.80615234375
                ],
                [
                    -748.7659301757813,
                    841.9055786132813
                ],
                [
                    48.94637680053711,
                    -67.69752502441406
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    8.321762084960938,
                    -10.168074607849121
                ],
                [
                    1243.2764892578125,
                    2881.231201171875
                ],
                [
                    3123.452880859375,
                    4143.1904296875
                ],
                [
                    1542.7359619140625,
                    680.88720703125
                ]
            ],
            "pieceId": "10"
        },
        {
            "coordinates": [
                [
                    0.0,
                    0.0
                ],
                [
                    1266.082763671875,
                    4952.16357421875
                ],
                [
                    2198.0361328125,
                    8389.861328125
                ],
                [
                    1251.8043212890625,
                    2894.763916015625
                ]
            ],
            "pieceId": "11"
        },
        {
            "coordinates": [
                [
                    617.1092529296875,
                    5830.23046875
                ],
                [
                    1512.0582275390625,
                    6820.76025390625
                ],
                [
                    1217.3975830078125,
                    4920.2705078125
                ]
            ],
            "pieceId": "12"
        },
        {
            "coordinates": [
                [
                    1245.6912841796875,
                    4931.05859375
                ],
                [
                    1573.3660888671875,
                    6847.78759765625
                ],
                [
                    2135.791748046875,
                    8375.2822265625
                ]
            ],
            "pieceId": "13"
        },
        {
            "coordinates": [
                [
                    1241.6839599609375,
                    2892.30322265625
                ],
                [
                    2187.84130859375,
                    8395.6748046875
                ],
                [
                    3132.42138671875,
                    4134.2216796875
                ]
            ],
            "pieceId": "14"
        },
        {
            "coordinates": [
                [
                    1586.1719970703125,
                    703.4091796875
                ],
                [
                    2631.9541015625,
                    -1454.32275390625
                ],
                [
                    2960.901123046875,
                    -2173.810791015625
                ]
            ],
            "pieceId": "15"
        },
        {
            "coordinates": [
                [
                    1529.428466796875,
                    687.7860717773438
                ],
                [
                    3131.254150390625,
                    4135.99755859375
                ],
                [
                    2629.516357421875,
                    -1447.7232666015625
                ]
            ],
            "pieceId": "16"
        },
        {
            "coordinates": [
                [
                    2629.543212890625,
                    -1459.060546875
                ],
                [
                    3121.812744140625,
                    4135.0859375
                ],
                [
                    2966.712890625,
                    -2183.923583984375
                ]
            ],
            "pieceId": "17"
        },
        {
            "coordinates": [
                [
                    -5564.8388671875,
                    5781.09326171875
                ],
                [
                    -1400.012939453125,
                    7943.1357421875
                ],
                [
                    593.0328369140625,
                    5830.33544921875
                ],
                [
                    -727.6839599609375,
                    860.0578002929688
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    -5113.76171875,
                    -1376.6707763671875
                ],
                [
                    3079.013671875,
                    -2119.304443359375
                ],
                [
                    86.98653411865234,
                    -2455.243896484375
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -5103.1474609375,
                    -1372.871337890625
                ],
                [
                    12.060164451599121,
                    -65.16647338867188
                ],
                [
                    3088.584716796875,
                    -2114.27294921875
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    -1382.026611328125,
                    7939.05615234375
                ],
                [
                    1509.2181396484375,
                    6830.04736328125
                ],
                [
                    605.7071533203125,
                    5832.07080078125
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    -1364.3912353515625,
                    7938.5751953125
                ],
                [
                    2084.516357421875,
                    8363.759765625
                ],
                [
                    1528.6502685546875,
                    6827.35009765625
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    -750.617919921875,
                    922.7809448242188
                ],
                [
                    1246.4637451171875,
                    4939.9814453125
                ],
                [
                    19.521713256835938,
                    -14.804839134216309
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    -734.0946044921875,
                    885.8508911132813
                ],
                [
                    613.6474609375,
                    5843.58740234375
                ],
                [
                    1209.16552734375,
                    4920.89453125
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    18.899917602539063,
                    -42.694087982177734
                ],
                [
                    1532.255126953125,
                    690.2617797851563
                ],
                [
                    3072.662109375,
                    -2109.22802734375
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalCoords": [
        {
            "coordinates": [
                [
                    -5516.5048828125,
                    5967.2314453125
                ],
                [
                    -19.27947998046875,
                    -8.544921875
                ],
                [
                    -5191.74560546875,
                    -1101.45751953125
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    -5519.2783203125,
                    5983.9931640625
                ],
                [
                    -794.3134155273438,
                    934.5225830078125
                ],
                [
                    -26.075361251831055,
                    -0.1068115159869194
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    8.710861206054688,
                    -5.456923961639404
                ],
                [
                    1257.6007080078125,
                    2879.951416015625
                ],
                [
                    3143.844482421875,
                    4132.82373046875
                ],
                [
                    1546.4400634765625,
                    678.1882934570313
                ]
            ],
            "pieceId": "10"
        },
        {
            "coordinates": [
                [
                    0.0,
                    0.0
                ],
                [
                    1266.082763671875,
                    4952.16357421875
                ],
                [
                    2198.0361328125,
                    8389.861328125
                ],
                [
                    1251.8043212890625,
                    2894.763916015625
                ]
            ],
            "pieceId": "11"
        },
        {
            "coordinates": [
                [
                    668.06982421875,
                    5897.19189453125
                ],
                [
                    1591.2303466796875,
                    6861.482421875
                ],
                [
                    1241.849853515625,
                    4970.287109375
                ]
            ],
            "pieceId": "12"
        },
        {
            "coordinates": [
                [
                    1273.6549072265625,
                    4959.9892578125
                ],
                [
                    1613.5692138671875,
                    6874.583984375
                ],
                [
                    2185.7412109375,
                    8398.4560546875
                ]
            ],
            "pieceId": "13"
        },
        {
            "coordinates": [
                [
                    1246.0364990234375,
                    2887.174560546875
                ],
                [
                    2206.878662109375,
                    8388.0
                ],
                [
                    3140.081298828125,
                    4124.04248046875
                ]
            ],
            "pieceId": "14"
        },
        {
            "coordinates": [
                [
                    1556.86181640625,
                    656.8641357421875
                ],
                [
                    2656.67529296875,
                    -1473.8367919921875
                ],
                [
                    3003.642822265625,
                    -2184.80859375
                ]
            ],
            "pieceId": "15"
        },
        {
            "coordinates": [
                [
                    1562.0325927734375,
                    677.1964721679688
                ],
                [
                    3158.611083984375,
                    4127.841796875
                ],
                [
                    2665.364990234375,
                    -1456.6383056640625
                ]
            ],
            "pieceId": "16"
        },
        {
            "coordinates": [
                [
                    2670.10107421875,
                    -1465.6314697265625
                ],
                [
                    3168.5693359375,
                    4127.9677734375
                ],
                [
                    3006.4677734375,
                    -2190.8681640625
                ]
            ],
            "pieceId": "17"
        },
        {
            "coordinates": [
                [
                    -5507.021484375,
                    5988.833984375
                ],
                [
                    -1290.8018798828125,
                    8048.8544921875
                ],
                [
                    650.2246704101563,
                    5888.166015625
                ],
                [
                    -791.0880737304688,
                    951.5113525390625
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    -5180.11083984375,
                    -1119.0623779296875
                ],
                [
                    2973.979736328125,
                    -2207.120849609375
                ],
                [
                    -29.56580924987793,
                    -2416.368408203125
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -5179.97216796875,
                    -1106.2659912109375
                ],
                [
                    -13.652800559997559,
                    -17.877578735351563
                ],
                [
                    2972.6923828125,
                    -2196.313720703125
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    -1282.7071533203125,
                    8056.23583984375
                ],
                [
                    1579.8358154296875,
                    6875.1181640625
                ],
                [
                    651.5979614257813,
                    5900.0966796875
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    -1275.08154296875,
                    8061.94287109375
                ],
                [
                    2182.863037109375,
                    8405.982421875
                ],
                [
                    1591.0548095703125,
                    6883.05615234375
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    -770.4696044921875,
                    950.8933715820313
                ],
                [
                    1255.662841796875,
                    4953.51953125
                ],
                [
                    -7.143020153045654,
                    7.753371715545654
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    -780.3172607421875,
                    955.5491943359375
                ],
                [
                    665.1057739257813,
                    5885.6923828125
                ],
                [
                    1242.279052734375,
                    4951.4140625
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    1.9607542753219604,
                    -20.957944869995117
                ],
                [
                    1539.2607421875,
                    660.3450317382813
                ],
                [
                    2984.012451171875,
                    -2189.685791015625
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalTransformation": [
        {
            "pieceId": "0",
            "rotationRadians": -12.564847946166992,
            "translateVectorX": -3575.84375,
            "translateVectorY": 1619.07568359375
        },
        {
            "pieceId": "1",
            "rotationRadians": 0.0006398410187102854,
            "translateVectorX": -2113.221923828125,
            "translateVectorY": 2306.136962890625
        },
        {
            "pieceId": "10",
            "rotationRadians": -6.279477119445801,
            "translateVectorX": 1520.2274169921875,
            "translateVectorY": 1953.2984619140625
        },
        {
            "pieceId": "11",
            "rotationRadians": 0.0,
            "translateVectorX": 0.0,
            "translateVectorY": 0.0
        },
        {
            "pieceId": "12",
            "rotationRadians": 6.280244827270508,
            "translateVectorX": 1167.05126953125,
            "translateVectorY": 5909.654296875
        },
        {
            "pieceId": "13",
            "rotationRadians": 12.57500171661377,
            "translateVectorX": 1690.9884033203125,
            "translateVectorY": 6744.34423828125
        },
        {
            "pieceId": "14",
            "rotationRadians": -0.003736441023647785,
            "translateVectorX": 2197.666015625,
            "translateVectorY": 5133.07177734375
        },
        {
            "pieceId": "15",
            "rotationRadians": 62.83720397949219,
            "translateVectorX": 2405.727294921875,
            "translateVectorY": -1000.5931396484375
        },
        {
            "pieceId": "16",
            "rotationRadians": -12.563152313232422,
            "translateVectorX": 2462.003662109375,
            "translateVectorY": 1116.1326904296875
        },
        {
            "pieceId": "17",
            "rotationRadians": -6.281647205352783,
            "translateVectorX": 2948.37939453125,
            "translateVectorY": 157.15599060058594
        },
        {
            "pieceId": "2",
            "rotationRadians": 6.283578395843506,
            "translateVectorX": -1932.6513671875,
            "translateVectorY": 4986.640625
        },
        {
            "pieceId": "3",
            "rotationRadians": -12.564457893371582,
            "translateVectorX": -745.2315673828125,
            "translateVectorY": -1914.1844482421875
        },
        {
            "pieceId": "4",
            "rotationRadians": -12.564960479736328,
            "translateVectorX": -740.3106079101563,
            "translateVectorY": -1106.819091796875
        },
        {
            "pieceId": "5",
            "rotationRadians": 0.0007610126049257815,
            "translateVectorX": 316.2422180175781,
            "translateVectorY": 6943.81689453125
        },
        {
            "pieceId": "6",
            "rotationRadians": -6.283064842224121,
            "translateVectorX": 832.94482421875,
            "translateVectorY": 7783.66064453125
        },
        {
            "pieceId": "7",
            "rotationRadians": -0.0018555914284661412,
            "translateVectorX": 159.35134887695313,
            "translateVectorY": 1970.7220458984375
        },
        {
            "pieceId": "8",
            "rotationRadians": 6.283085823059082,
            "translateVectorX": 375.68853759765625,
            "translateVectorY": 3930.885009765625
        },
        {
            "pieceId": "9",
            "rotationRadians": -6.278622150421143,
            "translateVectorX": 1508.411376953125,
            "translateVectorY": -516.7674560546875
        }
    ]
}   
    
    def test_draw_polygons(self):
        polygons = [Polygon(piece_json["coordinates"]) for piece_json in self.response_15DBPAST1staged["piecesFinalCoords"]]

        ax = plt.subplot()
        seed = 10
        plot_polygons(polygons,ax=ax,seed=seed)
        ax.invert_yaxis()

        plt.show()

    def test_masks(self):
        db = "0-30"
        puzzle_num = "15DBPAST1staged"
        puzzle_noise_level = 1
        recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level,is_load_extrapolation_data=False)
        bag_of_pieces = recipe.cook()
        bag_of_pieces = bag_of_pieces[:3]

        [piece.load_image() for piece in bag_of_pieces]
        masks = restore_assembly_img.mask_final_assembly_image(self.response_15DBPAST1staged,bag_of_pieces)

        _, axs = plt.subplots(1,3)
        axs[0].imshow(masks[0])
        axs[1].imshow(masks[1])
        axs[2].imshow(masks[2])

        plt.show()


    def test_center_mask(self):
        piece_i =11
        coords = self.response_15DBPAST1staged["piecesFinalCoords"][piece_i]["coordinates"]
        poly = Polygon(coords)
        mass_x, mass_y = restore_assembly_img.center_of_mass(poly)

        print(f"Center of mass {(mass_x,mass_y)}")
        print(f"Centroid {poly.centroid}")
        print(self.response_15DBPAST1staged["piecesFinalTransformation"][piece_i])

        db = "0-30"
        puzzle_num = "15DBPAST1staged"
        puzzle_noise_level = 1
        recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level,is_load_extrapolation_data=False)
        bag_of_pieces = recipe.cook()
        bag_of_pieces[piece_i].load_image()

        img_mass_x,img_mass_y = restore_assembly_img.center_of_mass(bag_of_pieces[piece_i].polygon)
        img_mass_x*=1/3
        img_mass_y*=1/3

        ax = plt.subplot()
        ax.imshow(bag_of_pieces[piece_i].img)
        ax.scatter([img_mass_x],[img_mass_y],color="red",marker="X")
        ax.scatter([bag_of_pieces[piece_i].img.shape[1]//2],[bag_of_pieces[piece_i].img.shape[0]//2],color="yellow",marker="X")

        centroid_x = bag_of_pieces[piece_i].polygon.centroid.x*1/3
        centroid_y = bag_of_pieces[piece_i].polygon.centroid.y*1/3
        ax.scatter([centroid_x],[centroid_y],color="purple",marker="o")

        plt.show()

        # print


    def test_draw_solution(self):
        db = "0-30"
        puzzle_num = "15DBPAST1staged"
        puzzle_noise_level = 1
        recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level,is_load_extrapolation_data=False)
        bag_of_pieces = recipe.cook()
        # bag_of_pieces = bag_of_pieces[3:5]
        # bag_of_pieces = bag_of_pieces[0:3]
        # bag_of_pieces = bag_of_pieces[10:]
        # bag_of_pieces = bag_of_pieces[11:]

        [piece.load_image() for piece in bag_of_pieces]

        ax = plt.subplot()

        img,positions = restore_assembly_img.restore_final_assembly_image(self.response_15DBPAST1staged,bag_of_pieces,
                                                                                  background_size=(4800,4800))
        ax.imshow(img)

        # xs = [pos[0] for pos in positions]
        # ys = [pos[1] for pos in positions]
        # ax.scatter(xs,ys,marker="x",color="red")

        plt.show()



    def test_draw_solution_gloria(self):
        response = {
    "AfterEnableCollision": {
        "springs": [
            {
                "firstPieceId": "0",
                "firstPieceVertex": 2,
                "secondPieceId": "33",
                "secondPieceVertex": 4,
                "snapshotedLength": 392.3402099609375
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 3,
                "secondPieceId": "33",
                "secondPieceVertex": 3,
                "snapshotedLength": 323.60736083984375
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 1,
                "secondPieceId": "15",
                "secondPieceVertex": 1,
                "snapshotedLength": 1248.386474609375
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 2,
                "secondPieceId": "15",
                "secondPieceVertex": 0,
                "snapshotedLength": 1546.234130859375
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 0,
                "secondPieceId": "1",
                "secondPieceVertex": 0,
                "snapshotedLength": 933.78955078125
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 1,
                "secondPieceId": "1",
                "secondPieceVertex": 3,
                "snapshotedLength": 971.8310546875
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 2,
                "secondPieceId": "14",
                "secondPieceVertex": 1,
                "snapshotedLength": 2543.594482421875
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 3,
                "secondPieceId": "14",
                "secondPieceVertex": 0,
                "snapshotedLength": 3311.35693359375
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 2,
                "secondPieceId": "15",
                "secondPieceVertex": 0,
                "snapshotedLength": 1506.6644287109375
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 3,
                "secondPieceId": "15",
                "secondPieceVertex": 2,
                "snapshotedLength": 1315.379150390625
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 1,
                "secondPieceId": "16",
                "secondPieceVertex": 0,
                "snapshotedLength": 908.4593505859375
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 2,
                "secondPieceId": "16",
                "secondPieceVertex": 2,
                "snapshotedLength": 861.9580688476563
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 0,
                "secondPieceId": "2",
                "secondPieceVertex": 0,
                "snapshotedLength": 1099.86572265625
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 1,
                "secondPieceId": "2",
                "secondPieceVertex": 3,
                "snapshotedLength": 1085.8349609375
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 2,
                "secondPieceId": "16",
                "secondPieceVertex": 1,
                "snapshotedLength": 184.96351623535156
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 3,
                "secondPieceId": "16",
                "secondPieceVertex": 0,
                "snapshotedLength": 182.4475555419922
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 1,
                "secondPieceId": "27",
                "secondPieceVertex": 0,
                "snapshotedLength": 227.07749938964844
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 2,
                "secondPieceId": "27",
                "secondPieceVertex": 2,
                "snapshotedLength": 227.19073486328125
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 0,
                "secondPieceId": "3",
                "secondPieceVertex": 0,
                "snapshotedLength": 317.1300048828125
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 1,
                "secondPieceId": "3",
                "secondPieceVertex": 3,
                "snapshotedLength": 275.63751220703125
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 2,
                "secondPieceId": "29",
                "secondPieceVertex": 1,
                "snapshotedLength": 768.3653564453125
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 3,
                "secondPieceId": "29",
                "secondPieceVertex": 0,
                "snapshotedLength": 757.9497680664063
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 0,
                "secondPieceId": "4",
                "secondPieceVertex": 0,
                "snapshotedLength": 154.20864868164063
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 1,
                "secondPieceId": "4",
                "secondPieceVertex": 2,
                "snapshotedLength": 131.81056213378906
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 1,
                "secondPieceId": "26",
                "secondPieceVertex": 0,
                "snapshotedLength": 119.38037872314453
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 2,
                "secondPieceId": "26",
                "secondPieceVertex": 2,
                "snapshotedLength": 118.30621337890625
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 0,
                "secondPieceId": "5",
                "secondPieceVertex": 0,
                "snapshotedLength": 99.68753814697266
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 1,
                "secondPieceId": "5",
                "secondPieceVertex": 3,
                "snapshotedLength": 39.31767654418945
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 2,
                "secondPieceId": "26",
                "secondPieceVertex": 1,
                "snapshotedLength": 134.7532501220703
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 3,
                "secondPieceId": "26",
                "secondPieceVertex": 0,
                "snapshotedLength": 98.06596374511719
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 1,
                "secondPieceId": "34",
                "secondPieceVertex": 1,
                "snapshotedLength": 285.5046081542969
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 2,
                "secondPieceId": "34",
                "secondPieceVertex": 0,
                "snapshotedLength": 164.37582397460938
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 0,
                "secondPieceId": "6",
                "secondPieceVertex": 0,
                "snapshotedLength": 24.760805130004883
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 1,
                "secondPieceId": "6",
                "secondPieceVertex": 2,
                "snapshotedLength": 47.66613006591797
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 1,
                "secondPieceId": "24",
                "secondPieceVertex": 0,
                "snapshotedLength": 36.608070373535156
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 2,
                "secondPieceId": "24",
                "secondPieceVertex": 2,
                "snapshotedLength": 56.408355712890625
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 0,
                "secondPieceId": "7",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.832366943359375
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 1,
                "secondPieceId": "7",
                "secondPieceVertex": 3,
                "snapshotedLength": 9.983080863952637
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 2,
                "secondPieceId": "25",
                "secondPieceVertex": 1,
                "snapshotedLength": 11.84190559387207
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 3,
                "secondPieceId": "25",
                "secondPieceVertex": 0,
                "snapshotedLength": 19.154605865478516
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "22",
                "secondPieceVertex": 0,
                "snapshotedLength": 8.828548431396484
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 2,
                "secondPieceId": "22",
                "secondPieceVertex": 2,
                "snapshotedLength": 11.465388298034668
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 0,
                "secondPieceId": "8",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.139047622680664
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "8",
                "secondPieceVertex": 2,
                "snapshotedLength": 8.939743995666504
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 1,
                "secondPieceId": "22",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.85622787475586
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 2,
                "secondPieceId": "22",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.035956382751465
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 1,
                "secondPieceId": "19",
                "secondPieceVertex": 0,
                "snapshotedLength": 8.813992500305176
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 2,
                "secondPieceId": "19",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.959501266479492
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 0,
                "secondPieceId": "10",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.881643295288086
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 1,
                "secondPieceId": "10",
                "secondPieceVertex": 4,
                "snapshotedLength": 11.091161727905273
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 3,
                "secondPieceId": "20",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.8673734664917
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 4,
                "secondPieceId": "20",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.671050071716309
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 2,
                "secondPieceId": "32",
                "secondPieceVertex": 0,
                "snapshotedLength": 54.583099365234375
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 3,
                "secondPieceId": "32",
                "secondPieceVertex": 2,
                "snapshotedLength": 60.32255554199219
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 1,
                "secondPieceId": "11",
                "secondPieceVertex": 0,
                "snapshotedLength": 24.479970932006836
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 2,
                "secondPieceId": "11",
                "secondPieceVertex": 3,
                "snapshotedLength": 28.392162322998047
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 2,
                "secondPieceId": "32",
                "secondPieceVertex": 1,
                "snapshotedLength": 90.11803436279297
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 3,
                "secondPieceId": "32",
                "secondPieceVertex": 0,
                "snapshotedLength": 82.95804595947266
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 1,
                "secondPieceId": "30",
                "secondPieceVertex": 2,
                "snapshotedLength": 168.96817016601563
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 2,
                "secondPieceId": "30",
                "secondPieceVertex": 1,
                "snapshotedLength": 189.1004638671875
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 0,
                "secondPieceId": "12",
                "secondPieceVertex": 0,
                "snapshotedLength": 308.4625244140625
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 1,
                "secondPieceId": "12",
                "secondPieceVertex": 2,
                "snapshotedLength": 283.11712646484375
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 1,
                "secondPieceId": "23",
                "secondPieceVertex": 2,
                "snapshotedLength": 130.84381103515625
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 2,
                "secondPieceId": "23",
                "secondPieceVertex": 1,
                "snapshotedLength": 160.8664093017578
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 0,
                "secondPieceId": "13",
                "secondPieceVertex": 0,
                "snapshotedLength": 323.81072998046875
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 1,
                "secondPieceId": "13",
                "secondPieceVertex": 2,
                "snapshotedLength": 356.6547546386719
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 1,
                "secondPieceId": "18",
                "secondPieceVertex": 2,
                "snapshotedLength": 242.33689880371094
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 2,
                "secondPieceId": "18",
                "secondPieceVertex": 1,
                "snapshotedLength": 111.89544677734375
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 0,
                "secondPieceId": "14",
                "secondPieceVertex": 0,
                "snapshotedLength": 185.11233520507813
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 1,
                "secondPieceId": "14",
                "secondPieceVertex": 2,
                "snapshotedLength": 264.6000061035156
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 0,
                "secondPieceId": "15",
                "secondPieceVertex": 0,
                "snapshotedLength": 1607.66015625
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 1,
                "secondPieceId": "15",
                "secondPieceVertex": 2,
                "snapshotedLength": 639.116455078125
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 1,
                "secondPieceId": "23",
                "secondPieceVertex": 1,
                "snapshotedLength": 90.8294906616211
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 2,
                "secondPieceId": "23",
                "secondPieceVertex": 0,
                "snapshotedLength": 178.6611785888672
            },
            {
                "firstPieceId": "17",
                "firstPieceVertex": 2,
                "secondPieceId": "18",
                "secondPieceVertex": 1,
                "snapshotedLength": 126.14356994628906
            },
            {
                "firstPieceId": "17",
                "firstPieceVertex": 3,
                "secondPieceId": "18",
                "secondPieceVertex": 0,
                "snapshotedLength": 103.7656478881836
            },
            {
                "firstPieceId": "17",
                "firstPieceVertex": 1,
                "secondPieceId": "23",
                "secondPieceVertex": 0,
                "snapshotedLength": 152.05963134765625
            },
            {
                "firstPieceId": "17",
                "firstPieceVertex": 2,
                "secondPieceId": "23",
                "secondPieceVertex": 2,
                "snapshotedLength": 74.15473175048828
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 0,
                "secondPieceId": "20",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.746318817138672
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 1,
                "secondPieceId": "20",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.002448081970215
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 1,
                "secondPieceId": "21",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.753242492675781
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 2,
                "secondPieceId": "21",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.547063827514648
            },
            {
                "firstPieceId": "22",
                "firstPieceVertex": 1,
                "secondPieceId": "31",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.360956192016602
            },
            {
                "firstPieceId": "22",
                "firstPieceVertex": 2,
                "secondPieceId": "31",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.101561546325684
            },
            {
                "firstPieceId": "24",
                "firstPieceVertex": 1,
                "secondPieceId": "36",
                "secondPieceVertex": 0,
                "snapshotedLength": 315.1536560058594
            },
            {
                "firstPieceId": "24",
                "firstPieceVertex": 2,
                "secondPieceId": "36",
                "secondPieceVertex": 2,
                "snapshotedLength": 294.9503173828125
            },
            {
                "firstPieceId": "24",
                "firstPieceVertex": 0,
                "secondPieceId": "25",
                "secondPieceVertex": 0,
                "snapshotedLength": 15.242585182189941
            },
            {
                "firstPieceId": "24",
                "firstPieceVertex": 1,
                "secondPieceId": "25",
                "secondPieceVertex": 2,
                "snapshotedLength": 14.348396301269531
            },
            {
                "firstPieceId": "25",
                "firstPieceVertex": 1,
                "secondPieceId": "31",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.813782691955566
            },
            {
                "firstPieceId": "25",
                "firstPieceVertex": 2,
                "secondPieceId": "31",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.62606430053711
            },
            {
                "firstPieceId": "26",
                "firstPieceVertex": 1,
                "secondPieceId": "33",
                "secondPieceVertex": 2,
                "snapshotedLength": 200.987060546875
            },
            {
                "firstPieceId": "26",
                "firstPieceVertex": 2,
                "secondPieceId": "33",
                "secondPieceVertex": 1,
                "snapshotedLength": 380.0284423828125
            },
            {
                "firstPieceId": "27",
                "firstPieceVertex": 1,
                "secondPieceId": "30",
                "secondPieceVertex": 0,
                "snapshotedLength": 66.20027160644531
            },
            {
                "firstPieceId": "27",
                "firstPieceVertex": 2,
                "secondPieceId": "30",
                "secondPieceVertex": 2,
                "snapshotedLength": 149.26513671875
            },
            {
                "firstPieceId": "27",
                "firstPieceVertex": 0,
                "secondPieceId": "28",
                "secondPieceVertex": 0,
                "snapshotedLength": 284.280029296875
            },
            {
                "firstPieceId": "27",
                "firstPieceVertex": 1,
                "secondPieceId": "28",
                "secondPieceVertex": 2,
                "snapshotedLength": 248.8850860595703
            },
            {
                "firstPieceId": "28",
                "firstPieceVertex": 1,
                "secondPieceId": "30",
                "secondPieceVertex": 1,
                "snapshotedLength": 368.23431396484375
            },
            {
                "firstPieceId": "28",
                "firstPieceVertex": 2,
                "secondPieceId": "30",
                "secondPieceVertex": 0,
                "snapshotedLength": 313.7090759277344
            },
            {
                "firstPieceId": "28",
                "firstPieceVertex": 0,
                "secondPieceId": "29",
                "secondPieceVertex": 0,
                "snapshotedLength": 438.757080078125
            },
            {
                "firstPieceId": "28",
                "firstPieceVertex": 1,
                "secondPieceId": "29",
                "secondPieceVertex": 2,
                "snapshotedLength": 552.695556640625
            },
            {
                "firstPieceId": "29",
                "firstPieceVertex": 1,
                "secondPieceId": "33",
                "secondPieceVertex": 0,
                "snapshotedLength": 575.6041259765625
            },
            {
                "firstPieceId": "29",
                "firstPieceVertex": 2,
                "secondPieceId": "33",
                "secondPieceVertex": 4,
                "snapshotedLength": 1022.815185546875
            },
            {
                "firstPieceId": "32",
                "firstPieceVertex": 1,
                "secondPieceId": "35",
                "secondPieceVertex": 1,
                "snapshotedLength": 1394.390625
            },
            {
                "firstPieceId": "32",
                "firstPieceVertex": 2,
                "secondPieceId": "35",
                "secondPieceVertex": 0,
                "snapshotedLength": 356.57965087890625
            },
            {
                "firstPieceId": "33",
                "firstPieceVertex": 3,
                "secondPieceId": "35",
                "secondPieceVertex": 2,
                "snapshotedLength": 770.7720336914063
            },
            {
                "firstPieceId": "33",
                "firstPieceVertex": 4,
                "secondPieceId": "35",
                "secondPieceVertex": 1,
                "snapshotedLength": 716.6930541992188
            },
            {
                "firstPieceId": "33",
                "firstPieceVertex": 2,
                "secondPieceId": "34",
                "secondPieceVertex": 0,
                "snapshotedLength": 140.74545288085938
            },
            {
                "firstPieceId": "33",
                "firstPieceVertex": 3,
                "secondPieceId": "34",
                "secondPieceVertex": 2,
                "snapshotedLength": 84.19673156738281
            },
            {
                "firstPieceId": "34",
                "firstPieceVertex": 1,
                "secondPieceId": "37",
                "secondPieceVertex": 0,
                "snapshotedLength": 115.81373596191406
            },
            {
                "firstPieceId": "34",
                "firstPieceVertex": 2,
                "secondPieceId": "37",
                "secondPieceVertex": 2,
                "snapshotedLength": 84.71394348144531
            },
            {
                "firstPieceId": "36",
                "firstPieceVertex": 1,
                "secondPieceId": "37",
                "secondPieceVertex": 1,
                "snapshotedLength": 177.84051513671875
            },
            {
                "firstPieceId": "36",
                "firstPieceVertex": 2,
                "secondPieceId": "37",
                "secondPieceVertex": 0,
                "snapshotedLength": 217.3974151611328
            }
        ],
        "sumSpringsLength": 38033.0
    },
    "piecesBeforeEnableCollision": [
        {
            "coordinates": [
                [
                    -4633.18603515625,
                    1605.697509765625
                ],
                [
                    -3875.245849609375,
                    1758.2606201171875
                ],
                [
                    779.3178100585938,
                    201.1527862548828
                ],
                [
                    1024.8603515625,
                    86.16255950927734
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    -5564.46044921875,
                    1537.20654296875
                ],
                [
                    -5104.09912109375,
                    1522.5943603515625
                ],
                [
                    -1383.3350830078125,
                    1231.6092529296875
                ],
                [
                    -4795.978515625,
                    1447.2769775390625
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    -2978.89697265625,
                    -1001.2835693359375
                ],
                [
                    -3076.8125,
                    -765.369384765625
                ],
                [
                    1212.6292724609375,
                    7.734298229217529
                ],
                [
                    3130.168701171875,
                    -237.23410034179688
                ],
                [
                    -2139.392822265625,
                    -1376.3541259765625
                ]
            ],
            "pieceId": "10"
        },
        {
            "coordinates": [
                [
                    -3052.40234375,
                    -763.5230712890625
                ],
                [
                    159.24453735351563,
                    1255.397705078125
                ],
                [
                    3257.270751953125,
                    668.1995239257813
                ],
                [
                    1239.19287109375,
                    17.75360107421875
                ]
            ],
            "pieceId": "11"
        },
        {
            "coordinates": [
                [
                    -2744.21484375,
                    -750.4996948242188
                ],
                [
                    -619.8863525390625,
                    1037.77685546875
                ],
                [
                    439.889892578125,
                    1292.74365234375
                ]
            ],
            "pieceId": "12"
        },
        {
            "coordinates": [
                [
                    -2421.310302734375,
                    -726.2916259765625
                ],
                [
                    -1632.919189453125,
                    1153.9287109375
                ],
                [
                    -263.8130187988281,
                    1017.3854370117188
                ]
            ],
            "pieceId": "13"
        },
        {
            "coordinates": [
                [
                    -2246.39306640625,
                    -665.7066040039063
                ],
                [
                    -3612.005126953125,
                    2457.53857421875
                ],
                [
                    -1369.216796875,
                    1175.6820068359375
                ]
            ],
            "pieceId": "14"
        },
        {
            "coordinates": [
                [
                    -731.7256469726563,
                    -126.86156463623047
                ],
                [
                    -4852.15185546875,
                    2535.510986328125
                ],
                [
                    -3535.407958984375,
                    1823.0284423828125
                ]
            ],
            "pieceId": "15"
        },
        {
            "coordinates": [
                [
                    -5927.62939453125,
                    1906.1259765625
                ],
                [
                    415.8840026855469,
                    1531.623779296875
                ],
                [
                    -2239.953857421875,
                    1327.3829345703125
                ]
            ],
            "pieceId": "16"
        },
        {
            "coordinates": [
                [
                    -5383.19580078125,
                    2592.17431640625
                ],
                [
                    -2095.5810546875,
                    1616.9241943359375
                ],
                [
                    -442.53155517578125,
                    989.4160766601563
                ],
                [
                    -4327.2568359375,
                    1525.81591796875
                ]
            ],
            "pieceId": "17"
        },
        {
            "coordinates": [
                [
                    -4242.40869140625,
                    1585.54638671875
                ],
                [
                    -355.8349304199219,
                    1081.0469970703125
                ],
                [
                    -1728.4354248046875,
                    931.2095336914063
                ]
            ],
            "pieceId": "18"
        },
        {
            "coordinates": [
                [
                    -2137.18408203125,
                    -1384.7559814453125
                ],
                [
                    -97.4464340209961,
                    -1913.7496337890625
                ],
                [
                    -895.6450805664063,
                    -2482.9462890625
                ]
            ],
            "pieceId": "19"
        },
        {
            "coordinates": [
                [
                    -6570.6748046875,
                    1981.3193359375
                ],
                [
                    -1335.353759765625,
                    1969.1046142578125
                ],
                [
                    231.607421875,
                    1515.6973876953125
                ],
                [
                    -6107.22509765625,
                    1938.257080078125
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    -2129.12939453125,
                    -1379.2667236328125
                ],
                [
                    3130.5732421875,
                    -227.37501525878906
                ],
                [
                    -87.98407745361328,
                    -1910.5128173828125
                ]
            ],
            "pieceId": "20"
        },
        {
            "coordinates": [
                [
                    -882.0704956054688,
                    -2464.1435546875
                ],
                [
                    -87.50342559814453,
                    -1899.9747314453125
                ],
                [
                    3138.98828125,
                    -222.44451904296875
                ]
            ],
            "pieceId": "21"
        },
        {
            "coordinates": [
                [
                    -4889.99365234375,
                    2947.944580078125
                ],
                [
                    -2011.3505859375,
                    4335.54443359375
                ],
                [
                    -2494.4248046875,
                    3477.84033203125
                ]
            ],
            "pieceId": "22"
        },
        {
            "coordinates": [
                [
                    -2192.264404296875,
                    1499.561279296875
                ],
                [
                    460.1745300292969,
                    1452.3238525390625
                ],
                [
                    -512.06396484375,
                    963.6497192382813
                ]
            ],
            "pieceId": "23"
        },
        {
            "coordinates": [
                [
                    -3760.173583984375,
                    3008.701171875
                ],
                [
                    -118.0610580444336,
                    3946.536865234375
                ],
                [
                    770.6260375976563,
                    3202.903564453125
                ]
            ],
            "pieceId": "24"
        },
        {
            "coordinates": [
                [
                    -3759.107421875,
                    2993.491943359375
                ],
                [
                    -2486.3662109375,
                    3483.112060546875
                ],
                [
                    -132.33566284179688,
                    3945.08349609375
                ]
            ],
            "pieceId": "25"
        },
        {
            "coordinates": [
                [
                    -3111.755126953125,
                    2534.042236328125
                ],
                [
                    226.81234741210938,
                    2981.040771484375
                ],
                [
                    512.4568481445313,
                    2337.21533203125
                ]
            ],
            "pieceId": "26"
        },
        {
            "coordinates": [
                [
                    -1448.106689453125,
                    2166.2099609375
                ],
                [
                    -641.8113403320313,
                    1823.076171875
                ],
                [
                    13.359068870544434,
                    1452.5755615234375
                ]
            ],
            "pieceId": "27"
        },
        {
            "coordinates": [
                [
                    -1589.118896484375,
                    2413.051513671875
                ],
                [
                    2711.959716796875,
                    554.7752075195313
                ],
                [
                    -881.8473510742188,
                    1888.8453369140625
                ]
            ],
            "pieceId": "28"
        },
        {
            "coordinates": [
                [
                    -1986.4425048828125,
                    2599.17431640625
                ],
                [
                    394.1192321777344,
                    1517.6695556640625
                ],
                [
                    2170.982177734375,
                    441.5321044921875
                ]
            ],
            "pieceId": "29"
        },
        {
            "coordinates": [
                [
                    -6847.50927734375,
                    2136.0244140625
                ],
                [
                    759.0369873046875,
                    2375.266845703125
                ],
                [
                    1002.2086791992188,
                    1987.3656005859375
                ],
                [
                    -1609.607666015625,
                    1941.5396728515625
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -583.6219482421875,
                    1791.5037841796875
                ],
                [
                    3070.457275390625,
                    638.8778686523438
                ],
                [
                    -2.5348660945892334,
                    1304.1590576171875
                ]
            ],
            "pieceId": "30"
        },
        {
            "coordinates": [
                [
                    -2496.10888671875,
                    3487.80419921875
                ],
                [
                    -2009.7769775390625,
                    4344.77197265625
                ],
                [
                    -139.27078247070313,
                    3938.40771484375
                ]
            ],
            "pieceId": "31"
        },
        {
            "coordinates": [
                [
                    1160.7779541015625,
                    -9.317398071289063
                ],
                [
                    3167.4306640625,
                    661.1251220703125
                ],
                [
                    3070.3046875,
                    -244.65940856933594
                ]
            ],
            "pieceId": "32"
        },
        {
            "coordinates": [
                [
                    0.0,
                    1937.181396484375
                ],
                [
                    136.11221313476563,
                    2390.0107421875
                ],
                [
                    422.3270263671875,
                    3027.6220703125
                ],
                [
                    1336.7862548828125,
                    0.0
                ],
                [
                    1170.7496337890625,
                    227.8079833984375
                ]
            ],
            "pieceId": "33"
        },
        {
            "coordinates": [
                [
                    282.1597900390625,
                    3040.366943359375
                ],
                [
                    881.6318359375,
                    3053.951171875
                ],
                [
                    1384.2333984375,
                    69.55337524414063
                ]
            ],
            "pieceId": "34"
        },
        {
            "coordinates": [
                [
                    2784.92333984375,
                    -30.866621017456055
                ],
                [
                    1880.0810546875,
                    125.34903717041016
                ],
                [
                    2002.3306884765625,
                    388.7672119140625
                ]
            ],
            "pieceId": "35"
        },
        {
            "coordinates": [
                [
                    160.63497924804688,
                    4093.67724609375
                ],
                [
                    1886.53369140625,
                    644.38818359375
                ],
                [
                    554.229736328125,
                    3002.487060546875
                ]
            ],
            "pieceId": "36"
        },
        {
            "coordinates": [
                [
                    765.8290405273438,
                    3052.352783203125
                ],
                [
                    1754.2838134765625,
                    525.4859619140625
                ],
                [
                    1459.339111328125,
                    108.74365997314453
                ]
            ],
            "pieceId": "37"
        },
        {
            "coordinates": [
                [
                    -6970.697265625,
                    2228.790283203125
                ],
                [
                    -2998.126953125,
                    2497.4365234375
                ],
                [
                    627.7179565429688,
                    2363.872314453125
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    -7008.30029296875,
                    2321.113525390625
                ],
                [
                    739.509521484375,
                    3301.56689453125
                ],
                [
                    315.2313232421875,
                    2879.3525390625
                ],
                [
                    -3031.841064453125,
                    2477.203369140625
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    -6999.83935546875,
                    2344.383056640625
                ],
                [
                    -3775.220703125,
                    2975.326416015625
                ],
                [
                    759.13232421875,
                    3258.125244140625
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    -6988.44482421875,
                    2347.575927734375
                ],
                [
                    -4890.46826171875,
                    2939.128662109375
                ],
                [
                    -2496.580078125,
                    3489.101318359375
                ],
                [
                    -3765.239501953125,
                    2975.341552734375
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    -6982.86767578125,
                    2339.103515625
                ],
                [
                    -2007.348876953125,
                    4344.546875
                ],
                [
                    -4881.66796875,
                    2940.700439453125
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    -2971.807373046875,
                    -1008.1691284179688
                ],
                [
                    -2145.982666015625,
                    -1385.2786865234375
                ],
                [
                    -900.3295288085938,
                    -2491.7353515625
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalCoords": [
        {
            "coordinates": [
                [
                    -4633.18603515625,
                    1605.697509765625
                ],
                [
                    -3875.245849609375,
                    1758.2606201171875
                ],
                [
                    779.3178100585938,
                    201.1527862548828
                ],
                [
                    1024.8603515625,
                    86.16255950927734
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    -5564.46044921875,
                    1537.20654296875
                ],
                [
                    -5104.09912109375,
                    1522.5943603515625
                ],
                [
                    -1383.3350830078125,
                    1231.6092529296875
                ],
                [
                    -4795.978515625,
                    1447.2769775390625
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    -2978.89697265625,
                    -1001.2835693359375
                ],
                [
                    -3076.8125,
                    -765.369384765625
                ],
                [
                    1212.6292724609375,
                    7.734298229217529
                ],
                [
                    3130.168701171875,
                    -237.23410034179688
                ],
                [
                    -2139.392822265625,
                    -1376.3541259765625
                ]
            ],
            "pieceId": "10"
        },
        {
            "coordinates": [
                [
                    -3052.40234375,
                    -763.5230712890625
                ],
                [
                    159.24453735351563,
                    1255.397705078125
                ],
                [
                    3257.270751953125,
                    668.1995239257813
                ],
                [
                    1239.19287109375,
                    17.75360107421875
                ]
            ],
            "pieceId": "11"
        },
        {
            "coordinates": [
                [
                    -2744.21484375,
                    -750.4996948242188
                ],
                [
                    -619.8863525390625,
                    1037.77685546875
                ],
                [
                    439.889892578125,
                    1292.74365234375
                ]
            ],
            "pieceId": "12"
        },
        {
            "coordinates": [
                [
                    -2421.310302734375,
                    -726.2916259765625
                ],
                [
                    -1632.919189453125,
                    1153.9287109375
                ],
                [
                    -263.8130187988281,
                    1017.3854370117188
                ]
            ],
            "pieceId": "13"
        },
        {
            "coordinates": [
                [
                    -2246.39306640625,
                    -665.7066040039063
                ],
                [
                    -3612.005126953125,
                    2457.53857421875
                ],
                [
                    -1369.216796875,
                    1175.6820068359375
                ]
            ],
            "pieceId": "14"
        },
        {
            "coordinates": [
                [
                    -731.7256469726563,
                    -126.86156463623047
                ],
                [
                    -4852.15185546875,
                    2535.510986328125
                ],
                [
                    -3535.407958984375,
                    1823.0284423828125
                ]
            ],
            "pieceId": "15"
        },
        {
            "coordinates": [
                [
                    -5927.62939453125,
                    1906.1259765625
                ],
                [
                    415.8840026855469,
                    1531.623779296875
                ],
                [
                    -2239.953857421875,
                    1327.3829345703125
                ]
            ],
            "pieceId": "16"
        },
        {
            "coordinates": [
                [
                    -5383.19580078125,
                    2592.17431640625
                ],
                [
                    -2095.5810546875,
                    1616.9241943359375
                ],
                [
                    -442.53155517578125,
                    989.4160766601563
                ],
                [
                    -4327.2568359375,
                    1525.81591796875
                ]
            ],
            "pieceId": "17"
        },
        {
            "coordinates": [
                [
                    -4242.40869140625,
                    1585.54638671875
                ],
                [
                    -355.8349304199219,
                    1081.0469970703125
                ],
                [
                    -1728.4354248046875,
                    931.2095336914063
                ]
            ],
            "pieceId": "18"
        },
        {
            "coordinates": [
                [
                    -2137.18408203125,
                    -1384.7559814453125
                ],
                [
                    -97.4464340209961,
                    -1913.7496337890625
                ],
                [
                    -895.6450805664063,
                    -2482.9462890625
                ]
            ],
            "pieceId": "19"
        },
        {
            "coordinates": [
                [
                    -6570.6748046875,
                    1981.3193359375
                ],
                [
                    -1335.353759765625,
                    1969.1046142578125
                ],
                [
                    231.607421875,
                    1515.6973876953125
                ],
                [
                    -6107.22509765625,
                    1938.257080078125
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    -2129.12939453125,
                    -1379.2667236328125
                ],
                [
                    3130.5732421875,
                    -227.37501525878906
                ],
                [
                    -87.98407745361328,
                    -1910.5128173828125
                ]
            ],
            "pieceId": "20"
        },
        {
            "coordinates": [
                [
                    -882.0704956054688,
                    -2464.1435546875
                ],
                [
                    -87.50342559814453,
                    -1899.9747314453125
                ],
                [
                    3138.98828125,
                    -222.44451904296875
                ]
            ],
            "pieceId": "21"
        },
        {
            "coordinates": [
                [
                    -4889.99365234375,
                    2947.944580078125
                ],
                [
                    -2011.3505859375,
                    4335.54443359375
                ],
                [
                    -2494.4248046875,
                    3477.84033203125
                ]
            ],
            "pieceId": "22"
        },
        {
            "coordinates": [
                [
                    -2192.264404296875,
                    1499.561279296875
                ],
                [
                    460.1745300292969,
                    1452.3238525390625
                ],
                [
                    -512.06396484375,
                    963.6497192382813
                ]
            ],
            "pieceId": "23"
        },
        {
            "coordinates": [
                [
                    -3760.173583984375,
                    3008.701171875
                ],
                [
                    -118.0610580444336,
                    3946.536865234375
                ],
                [
                    770.6260375976563,
                    3202.903564453125
                ]
            ],
            "pieceId": "24"
        },
        {
            "coordinates": [
                [
                    -3759.107421875,
                    2993.491943359375
                ],
                [
                    -2486.3662109375,
                    3483.112060546875
                ],
                [
                    -132.33566284179688,
                    3945.08349609375
                ]
            ],
            "pieceId": "25"
        },
        {
            "coordinates": [
                [
                    -3111.755126953125,
                    2534.042236328125
                ],
                [
                    226.81234741210938,
                    2981.040771484375
                ],
                [
                    512.4568481445313,
                    2337.21533203125
                ]
            ],
            "pieceId": "26"
        },
        {
            "coordinates": [
                [
                    -1448.106689453125,
                    2166.2099609375
                ],
                [
                    -641.8113403320313,
                    1823.076171875
                ],
                [
                    13.359068870544434,
                    1452.5755615234375
                ]
            ],
            "pieceId": "27"
        },
        {
            "coordinates": [
                [
                    -1589.118896484375,
                    2413.051513671875
                ],
                [
                    2711.959716796875,
                    554.7752075195313
                ],
                [
                    -881.8473510742188,
                    1888.8453369140625
                ]
            ],
            "pieceId": "28"
        },
        {
            "coordinates": [
                [
                    -1986.4425048828125,
                    2599.17431640625
                ],
                [
                    394.1192321777344,
                    1517.6695556640625
                ],
                [
                    2170.982177734375,
                    441.5321044921875
                ]
            ],
            "pieceId": "29"
        },
        {
            "coordinates": [
                [
                    -6847.50927734375,
                    2136.0244140625
                ],
                [
                    759.0369873046875,
                    2375.266845703125
                ],
                [
                    1002.2086791992188,
                    1987.3656005859375
                ],
                [
                    -1609.607666015625,
                    1941.5396728515625
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -583.6219482421875,
                    1791.5037841796875
                ],
                [
                    3070.457275390625,
                    638.8778686523438
                ],
                [
                    -2.5348660945892334,
                    1304.1590576171875
                ]
            ],
            "pieceId": "30"
        },
        {
            "coordinates": [
                [
                    -2496.10888671875,
                    3487.80419921875
                ],
                [
                    -2009.7769775390625,
                    4344.77197265625
                ],
                [
                    -139.27078247070313,
                    3938.40771484375
                ]
            ],
            "pieceId": "31"
        },
        {
            "coordinates": [
                [
                    1160.7779541015625,
                    -9.317398071289063
                ],
                [
                    3167.4306640625,
                    661.1251220703125
                ],
                [
                    3070.3046875,
                    -244.65940856933594
                ]
            ],
            "pieceId": "32"
        },
        {
            "coordinates": [
                [
                    0.0,
                    1937.181396484375
                ],
                [
                    136.11221313476563,
                    2390.0107421875
                ],
                [
                    422.3270263671875,
                    3027.6220703125
                ],
                [
                    1336.7862548828125,
                    0.0
                ],
                [
                    1170.7496337890625,
                    227.8079833984375
                ]
            ],
            "pieceId": "33"
        },
        {
            "coordinates": [
                [
                    282.1597900390625,
                    3040.366943359375
                ],
                [
                    881.6318359375,
                    3053.951171875
                ],
                [
                    1384.2333984375,
                    69.55337524414063
                ]
            ],
            "pieceId": "34"
        },
        {
            "coordinates": [
                [
                    2784.92333984375,
                    -30.866621017456055
                ],
                [
                    1880.0810546875,
                    125.34903717041016
                ],
                [
                    2002.3306884765625,
                    388.7672119140625
                ]
            ],
            "pieceId": "35"
        },
        {
            "coordinates": [
                [
                    160.63497924804688,
                    4093.67724609375
                ],
                [
                    1886.53369140625,
                    644.38818359375
                ],
                [
                    554.229736328125,
                    3002.487060546875
                ]
            ],
            "pieceId": "36"
        },
        {
            "coordinates": [
                [
                    765.8290405273438,
                    3052.352783203125
                ],
                [
                    1754.2838134765625,
                    525.4859619140625
                ],
                [
                    1459.339111328125,
                    108.74365997314453
                ]
            ],
            "pieceId": "37"
        },
        {
            "coordinates": [
                [
                    -6970.697265625,
                    2228.790283203125
                ],
                [
                    -2998.126953125,
                    2497.4365234375
                ],
                [
                    627.7179565429688,
                    2363.872314453125
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    -7008.30029296875,
                    2321.113525390625
                ],
                [
                    739.509521484375,
                    3301.56689453125
                ],
                [
                    315.2313232421875,
                    2879.3525390625
                ],
                [
                    -3031.841064453125,
                    2477.203369140625
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    -6999.83935546875,
                    2344.383056640625
                ],
                [
                    -3775.220703125,
                    2975.326416015625
                ],
                [
                    759.13232421875,
                    3258.125244140625
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    -6988.44482421875,
                    2347.575927734375
                ],
                [
                    -4890.46826171875,
                    2939.128662109375
                ],
                [
                    -2496.580078125,
                    3489.101318359375
                ],
                [
                    -3765.239501953125,
                    2975.341552734375
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    -6982.86767578125,
                    2339.103515625
                ],
                [
                    -2007.348876953125,
                    4344.546875
                ],
                [
                    -4881.66796875,
                    2940.700439453125
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    -2971.807373046875,
                    -1008.1691284179688
                ],
                [
                    -2145.982666015625,
                    -1385.2786865234375
                ],
                [
                    -900.3295288085938,
                    -2491.7353515625
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalTransformation": [
        {
            "pieceId": "0",
            "rotationRadians": 1.3085418939590454,
            "translateVectorX": -2367.279052734375,
            "translateVectorY": 1117.0196533203125
        },
        {
            "pieceId": "1",
            "rotationRadians": 0.9867603182792664,
            "translateVectorX": -3951.621826171875,
            "translateVectorY": 1414.417236328125
        },
        {
            "pieceId": "10",
            "rotationRadians": 0.5715035796165466,
            "translateVectorX": -336.9998779296875,
            "translateVectorY": -631.4773559570313
        },
        {
            "pieceId": "11",
            "rotationRadians": 0.569705069065094,
            "translateVectorX": 168.1136932373047,
            "translateVectorY": 333.1222229003906
        },
        {
            "pieceId": "12",
            "rotationRadians": 0.579066276550293,
            "translateVectorX": -974.7371215820313,
            "translateVectorY": 526.6742553710938
        },
        {
            "pieceId": "13",
            "rotationRadians": 0.5585509538650513,
            "translateVectorX": -1439.34814453125,
            "translateVectorY": 481.6741638183594
        },
        {
            "pieceId": "14",
            "rotationRadians": 0.5072117447853088,
            "translateVectorX": -2409.204345703125,
            "translateVectorY": 989.1700439453125
        },
        {
            "pieceId": "15",
            "rotationRadians": 1.0569162368774414,
            "translateVectorX": -3039.762451171875,
            "translateVectorY": 1410.55859375
        },
        {
            "pieceId": "16",
            "rotationRadians": 0.9094825387001038,
            "translateVectorX": -2583.900390625,
            "translateVectorY": 1588.376953125
        },
        {
            "pieceId": "17",
            "rotationRadians": 0.7607741951942444,
            "translateVectorX": -3301.04052734375,
            "translateVectorY": 1705.86962890625
        },
        {
            "pieceId": "18",
            "rotationRadians": 0.7687143683433533,
            "translateVectorX": -2108.892333984375,
            "translateVectorY": 1199.268310546875
        },
        {
            "pieceId": "19",
            "rotationRadians": 0.5734511017799377,
            "translateVectorX": -1043.424560546875,
            "translateVectorY": -1927.150634765625
        },
        {
            "pieceId": "2",
            "rotationRadians": 0.9029754400253296,
            "translateVectorX": -2608.5947265625,
            "translateVectorY": 1821.71435546875
        },
        {
            "pieceId": "20",
            "rotationRadians": 0.5731024146080017,
            "translateVectorX": 304.4872131347656,
            "translateVectorY": -1172.3841552734375
        },
        {
            "pieceId": "21",
            "rotationRadians": 0.569817066192627,
            "translateVectorX": 723.1368408203125,
            "translateVectorY": -1528.854248046875
        },
        {
            "pieceId": "22",
            "rotationRadians": 0.8036117553710938,
            "translateVectorX": -3131.923583984375,
            "translateVectorY": 3587.1083984375
        },
        {
            "pieceId": "23",
            "rotationRadians": 0.8148803114891052,
            "translateVectorX": -748.0506591796875,
            "translateVectorY": 1305.1776123046875
        },
        {
            "pieceId": "24",
            "rotationRadians": 0.7959323525428772,
            "translateVectorX": -1035.8695068359375,
            "translateVectorY": 3386.047119140625
        },
        {
            "pieceId": "25",
            "rotationRadians": 0.8004035353660583,
            "translateVectorX": -2125.9365234375,
            "translateVectorY": 3473.895751953125
        },
        {
            "pieceId": "26",
            "rotationRadians": 0.8359315395355225,
            "translateVectorX": -790.8286743164063,
            "translateVectorY": 2617.431396484375
        },
        {
            "pieceId": "27",
            "rotationRadians": 0.7306472659111023,
            "translateVectorX": -692.1863403320313,
            "translateVectorY": 1813.9552001953125
        },
        {
            "pieceId": "28",
            "rotationRadians": 0.49463656544685364,
            "translateVectorX": 80.33179473876953,
            "translateVectorY": 1618.890625
        },
        {
            "pieceId": "29",
            "rotationRadians": 0.4238070845603943,
            "translateVectorX": 192.88633728027344,
            "translateVectorY": 1519.458740234375
        },
        {
            "pieceId": "3",
            "rotationRadians": 0.8671045899391174,
            "translateVectorX": -1852.626708984375,
            "translateVectorY": 2137.431884765625
        },
        {
            "pieceId": "30",
            "rotationRadians": 0.5443376302719116,
            "translateVectorX": 828.1001586914063,
            "translateVectorY": 1244.8463134765625
        },
        {
            "pieceId": "31",
            "rotationRadians": 0.7993705868721008,
            "translateVectorX": -1548.385498046875,
            "translateVectorY": 3923.66015625
        },
        {
            "pieceId": "32",
            "rotationRadians": 0.579119086265564,
            "translateVectorX": 2466.171142578125,
            "translateVectorY": 135.71548461914063
        },
        {
            "pieceId": "33",
            "rotationRadians": 0.0,
            "translateVectorX": 0.0,
            "translateVectorY": 0.0
        },
        {
            "pieceId": "34",
            "rotationRadians": 0.06202017515897751,
            "translateVectorX": 849.34228515625,
            "translateVectorY": 2054.62255859375
        },
        {
            "pieceId": "35",
            "rotationRadians": -4.1995110511779785,
            "translateVectorX": 2222.4462890625,
            "translateVectorY": 161.0832061767578
        },
        {
            "pieceId": "36",
            "rotationRadians": 0.2677340805530548,
            "translateVectorX": 867.1321411132813,
            "translateVectorY": 2580.184814453125
        },
        {
            "pieceId": "37",
            "rotationRadians": 0.12591201066970825,
            "translateVectorX": 1326.484619140625,
            "translateVectorY": 1228.86083984375
        },
        {
            "pieceId": "4",
            "rotationRadians": 0.8526905179023743,
            "translateVectorX": -3113.70263671875,
            "translateVectorY": 2363.364990234375
        },
        {
            "pieceId": "5",
            "rotationRadians": 0.8227529525756836,
            "translateVectorX": -2328.756103515625,
            "translateVectorY": 2758.76611328125
        },
        {
            "pieceId": "6",
            "rotationRadians": 0.8141472339630127,
            "translateVectorX": -3338.641845703125,
            "translateVectorY": 2859.279541015625
        },
        {
            "pieceId": "7",
            "rotationRadians": 0.8118889331817627,
            "translateVectorX": -4504.44970703125,
            "translateVectorY": 2934.516845703125
        },
        {
            "pieceId": "8",
            "rotationRadians": 0.8100077509880066,
            "translateVectorX": -4623.96044921875,
            "translateVectorY": 3208.118408203125
        },
        {
            "pieceId": "9",
            "rotationRadians": 0.5670587420463562,
            "translateVectorX": -2006.04052734375,
            "translateVectorY": -1628.39501953125
        }
    ]
        }

        db = "30-50"
        puzzle_num = "numPieces_38_rand_56665269_gloria"
        puzzle_noise_level = 1
        recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level,is_load_extrapolation_data=False)
        bag_of_pieces = recipe.cook()

        [piece.load_image() for piece in bag_of_pieces]

        ax = plt.subplot()

        img,positions = restore_assembly_img.restore_final_assembly_image(response,bag_of_pieces,
                                                                                  background_size=(4800,4800))
        ax.imshow(img)

        # xs = [pos[0] for pos in positions]
        # ys = [pos[1] for pos in positions]
        # ax.scatter(xs,ys,marker="x",color="red")

        plt.show()

if __name__ == "__main__":
    unittest.main()