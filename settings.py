# Settings for the Tetris game

# Tetris block shapes with all rotation states
SHAPES = [
    [  # I shape
        [[1, 1, 1, 1]],  # Horizontal
        [[1], [1], [1], [1]]  # Vertical
    ],
    [  # O shape (same in all rotations)
        [[1, 1],
         [1, 1]]
    ],
    [  # S shape
        [[0, 1, 1],
         [1, 1, 0]],  # Horizontal
        [[1, 0],
         [1, 1],
         [0, 1]]  # Vertical
    ],
    [  # Z shape
        [[1, 1, 0],
         [0, 1, 1]],  # Horizontal
        [[0, 1],
         [1, 1],
         [1, 0]]  # Vertical
    ],
    [  # T shape
        [[1, 1, 1],
         [0, 1, 0]],  # Horizontal
        [[0, 1],
         [1, 1],
         [0, 1]],  # Vertical
        [[0, 1, 0],
         [1, 1, 1]],  # 180-degree rotation
        [[1, 0],
         [1, 1],
         [1, 0]]  # 270-degree rotation
    ],
    [  # L shape
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]],  # Horizontal
        [[0, 0, 1],
         [1, 1, 1]],  # Vertical
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],  # 180-degree rotation
        [[1, 1, 1],
         [1, 0, 0]]  # 270-degree rotation
    ],
    [  # J shape
        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],  # Horizontal
        [[1, 0, 0],
         [1, 1, 1]],  # Vertical
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]],  # 180-degree rotation
        [[1, 1, 1],
         [0, 0, 1]]  # 270-degree rotation
    ]
]

# Colors corresponding to each shape
COLORS = [
    (0, 255, 255),  # Cyan for I
    (255, 255, 0),  # Yellow for O
    (0, 255, 0),    # Green for S
    (255, 0, 0),    # Red for Z
    (255, 0, 255),  # Magenta for T
    (255, 165, 0),  # Orange for L
    (0, 0, 255),    # Blue for J
]

# Dimensions of the game grid (standard Tetris size)
COLS = 10  # 12 columns
ROWS = 24  # 24 rows

# Block size (each Tetris block will be BLOCK_SIZE pixels wide and tall)
BLOCK_SIZE = 30  # Standard block size (feel free to adjust this)
