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

        # indxes = [trans_json["pieceId"] for trans_json in self.response_15DBPAST1staged["piecesFinalTransformation"]]

        # sorted_transformations 

        img,positions = restore_assembly_img.restore_final_assembly_image(self.response_15DBPAST1staged,bag_of_pieces,
                                                                          background_size=(8000,8000))
        ax.imshow(img)

        xs = [pos[0] for pos in positions]
        ys = [pos[1] for pos in positions]
        ax.scatter(xs,ys,marker="x",color="red")

        # polygons = [Polygon(piece_json["coordinates"]) for piece in bag_of_pieces for piece_json in self.response_15DBPAST1staged["piecesFinalCoords"] if piece.id == piece_json["pieceId"]]
        # polygons = [affinity.translate(poly,) for piece in zipbag_of_pieces for piece_json in self.response_15DBPAST1staged["piecesFinalTransformation"] if piece.id == piece_json["pieceId"]]
        # plot_polygons(polygons,ax=ax)

        
        # for piece,pos in zip(bag_of_pieces,positions):
        #     xs,ys = affinity.rotate(piece.polygon.exterior
        #     ax.plot(xs,ys)

        plt.show()


if __name__ == "__main__":
    unittest.main()