from pico2d import get_canvas_width, load_image

import game_framework


PIXEL_PER_METER = 10.0 / 0.3
BIRD_SPEED_KMPH = 20
BIRD_SPEED_MPS = BIRD_SPEED_KMPH * 1000.0 / 60.0 / 60.0
BIRD_SPEED_PPS = BIRD_SPEED_MPS * PIXEL_PER_METER

DISTANCE_PER_WINGBEAT_M = 2.0
FRAMES_PER_WINGBEAT = 14
FRAME_COUNT = FRAMES_PER_WINGBEAT
FRAMES_PER_SECOND = (
    BIRD_SPEED_MPS / DISTANCE_PER_WINGBEAT_M * FRAMES_PER_WINGBEAT
)

FRAME_WIDTH = 183
FRAME_HEIGHT = 168
DRAW_WIDTH = 110
DRAW_HEIGHT = 100


class Bird:
    image = None

    def __init__(self, x, y, frame=0):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = frame % FRAME_COUNT
        self.direction = 1

    def update(self):
        frame_time = game_framework.frame_time
        self.frame = (
            self.frame + FRAMES_PER_SECOND * frame_time
        ) % FRAME_COUNT
        self.x += self.direction * BIRD_SPEED_PPS * frame_time

        half_width = DRAW_WIDTH / 2
        min_x = half_width
        max_x = get_canvas_width() - half_width
        if self.x <= min_x:
            self.x = min_x
            self.direction = 1
        elif self.x >= max_x:
            self.x = max_x
            self.direction = -1

    def draw(self):
        frame_index = int(self.frame)
        row, column = divmod(frame_index, 5)
        source_y = 506 - (row + 1) * FRAME_HEIGHT
        flip = '' if self.direction == 1 else 'h'
        Bird.image.clip_composite_draw(
            column * FRAME_WIDTH, source_y,
            FRAME_WIDTH, FRAME_HEIGHT,
            0, flip, self.x, self.y, DRAW_WIDTH, DRAW_HEIGHT
        )