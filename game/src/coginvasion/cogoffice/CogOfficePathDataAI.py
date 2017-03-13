# Filename: CogOfficePathDataAI.py
# Created by:  blach (15Feb16)

from CogOfficeConstants import *

from ccoginvasion import SuitPathFinderAI

PathPolygons = {
    EXECUTIVE_FLOOR: [
        # Outermost loop, in CCW order
        [
            (-23.6198, 105.99),
            (-23, -4),
            (-25, -4),
            (-24.8597, 19.7615),
            (-73.2874, 19.6853),
            (-73.181, -18.9053),
            (23.9987, -19.1026),
            (24.3914, 105.982)
        ],
        # Large room middle desk
        [
            (14.0779, 34.2745),
            (-13.0885, 34.3094),
            (-13.0021, 65.2247),
            (14.2347, 65.2362)
        ],
        # Small room desk
        [
            (-56.6534, -8.13378),
            (-56.3471, -19.3702),
            (-73.9767, -19.6004),
            (-74.2037, -7.84778)
        ],
        # Large room right plant
        [
            (17.7337, 98.6777),
            (17.487, 105.123),
            (23.6936, 105.668),
            (23.9333, 98.9018)
        ],
        # Large room left plant
        [
            (-22.7783, 99.0361),
            (-23.0657, 105.05),
            (-16.5746, 105.644),
            (-16.5335, 99.3192)
        ],
        # Meeting table
        [
            (12.4674, 11.4722),
            (23.1376, 11.2703),
            (23.1953, -8.33822),
            (12.4227, -8.25342)
        ],

        # Meeting table chairs
        [ # 1
            (10.7629, -5.20445),
            (7.14602, -5.3047),
            (7.36057, -0.144386),
            (11.0009, -0.506205)
        ],
        [ # 2
            (10.7584, 3.34137),
            (7.30297, 3.02385),
            (7.3772, 7.88281),
            (10.6883, 8.04887)
        ],
        [ # 3
            (15.4582, -10.2653),
            (20.1923, -10.0593),
            (20.2982, -13.6088),
            (15.3869, -13.7005)
        ],
        [ # 4
            (15.3884, 13.1823),
            (15.4897, 16.443),
            (20.4219, 16.4386),
            (20.2548, 13.0272)
        ],

        # Small room desk chair
        [
            (-43.8819, -1.69798),
            (-47.2743, -2.8323),
            (-49.0769, 1.67703),
            (-45.7351, 2.75913)
        ],
    ],

    RECEPTION_FLOOR: [
        # Outermost loop, in CCW order
        [
            (9.84398, -9.77427),
            (9.66335, 29.4538),
            (-39.0881, 29.368),
            (-39.5746, -9.7075)
        ],
        # the 2 brown chairs
        [
            (-26.8556, -4.18886),
            (-17.1781, -4.01255),
            (-17.0241, -8.52118),
            (-26.8681, -8.43272)
        ],
        # The blue and white couch
        [
            (-27.6587, 25.7791),
            (-27.3032, 29.7652),
            (-19.5471, 29.478),
            (-19.6179, 26.3872)
        ],
        # Reception desk
        [
            (9.53479, 11.4891),
            (2.77426, 11.5997),
            (-2.79629, 14.6561),
            (-8.19409, 21.3034),
            (-8.503, 29.5709),
            (9.41554, 29.3894)
        ]
    ],

    CONFERENCE_FLOOR: [
        # Outermost loop, in CCW order
        [
            (-23.2364, -9.51548),
            (24.5698, -9.2548),
            (24.2484, 60.2761),
            (-23.4691, 60.5339)
        ],
        # the bookshelves
        [
            (-20.2676, 56.9492),
            (-20.6383, 27.9099),
            (-23.5174, 27.9565),
            (-23.3698, 57.1333)
        ],
        # the potted plant
        [
            (18.5513, -1.58998),
            (24.2785, -1.44093),
            (23.5045, -8.02527),
            (17.4315, -7.85613)
        ],
        # The reception desk
        [
            (24.1397, -0.69419),
            (13.0028, -0.570719),
            (12.9355, 17.2904),
            (24.7485, 17.6188)
        ],
        # The meeting table
        [
            (-6.53951, -4.81745),
            (-18.5539, -4.7359),
            (-18.5116, 16.295),
            (-6.79715, 16.2899)
        ],
        #-------Meeting table chairs-------#
        # 1
        [
            (-10.6989, 21.5713),
            (-10.5862, 17.5027),
            (-15.743, 17.7034),
            (-15.5578, 21.8772)
        ],
        # 2
        [
            (-19.8605, 13.2362),
            (-19.835, 7.52097),
            (-24.1598, 7.58476),
            (-23.8032, 13.0269)
        ],
        # 3
        [
            (-19.8374, 4.07941),
            (-19.8902, -0.98915),
            (-23.717, -1.2653),
            (-23.9181, 4.18953)
        ]
    ],

    LOUNGE_FLOOR: [
        # Outermost loop, in counter-clockwise order.
        [
            (-34.2147, 0.0498759),
            (36.3672, 0.19353),
            (36.0996, 81.7578),
            (-34.1152, 81.8778),
        ],

        # ----------computer desk chairs---------- #
        [ # 1
            (-21.8052, 36.5294),
            (-21.9194, 31.1991),
            (-26.2335, 31.3998),
            (-26.2467, 36.5092)
        ],
        [ # 2
            (-22.0058, 28.6912),
            (-22.2885, 23.4955),
            (-26.2374, 23.5246),
            (-26.314, 28.7862)
        ],
        [ # 3
            (-21.6038, 21.1434),
            (-21.9487, 15.5454),
            (-26.3404, 15.4474),
            (-26.5729, 21.0419)
        ],

        # ----------tv area chairs---------- #
        # It's one big polygon because their basically all connected to each other.
        [
            (15.7413, 77.4139),
            (19.8426, 78.0954),
            (23.816, 68.134),
            (33.6325, 64.2728),
            (33.0908, 60.3853),
            (20.3968, 64.8375),
        ]
    ]
}

floor2pathFinder = {}

def getPathFinder(floor):
    if not floor2pathFinder.get(floor):
        floor2pathFinder[floor] = SuitPathFinderAI(PathPolygons[floor])

    return floor2pathFinder[floor]
