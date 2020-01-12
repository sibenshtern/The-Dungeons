class Camera:

    def __init__(self, screen_width, screen_height):
        self.x = 0
        self.y = 0

        self.width = screen_width
        self.height = screen_height

    def apply(self, obj):
        obj.rect.x += self.x
        obj.rect.y += self.y

    def update(self, target):
        self.x = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.y = -(target.rect.y + target.rect.h // 2 - self.height // 2)
