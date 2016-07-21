from pygame.rect import Rect


class Camera(object):
    def __init__(self, size, window_size):
        self.window_size = window_size
        self.state = Rect(0, 0, size[0], size[1])

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def reverse(self, pos):
        return pos[0] - self.state.left, pos[1] - self.state.top

    def camera_func(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l + self.window_size[0] / 2, -t + self.window_size[1] / 2, w, h

        l = min(0, l)
        l = max(-(camera.width - self.window_size[0]), l)
        t = max(-(camera.height - self.window_size[1]), t)
        t = min(0, t)
        return Rect(l, t, w, h)
