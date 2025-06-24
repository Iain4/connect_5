import pygame as pg

# TODO: make not fugly
class Button:
    def __init__(
            self,
            pose,
            dim,
            b_color="orange",
            text=None,
            text_color="black",
            font=pg.font.get_default_font(),
            font_size=24,
            alpha = 200,
            **kwargs
        ):
        pg.font.init()
        # self.pose = pose
        self.dim = dim
        self.b_color = b_color
        self.text_color = text_color
        
        self.text = pg.font.SysFont(font, font_size).render(
            text,
            True,
            self.text_color, 
            self.b_color
        )
        
        self.b_rect = pg.Rect(
            pose,
            dim,
            color=b_color,
            **kwargs
        )
        self.b_rect.center = pose

        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.b_rect.center

        # self.b_surf = pg.Surface(self.b_rect.size)
        # self.b_surf.set_alpha(alpha) 


    def draw(self, surface):
        # self.b_surf.fill(self.b_color, self.b_rect)
        pg.draw.rect(surface, self.b_color, self.b_rect)
        surface.blit(self.text, self.text_rect)

    
    def pressed(self)->bool:
        for event in pg.event.get():
            if (
                    event.type == pg.MOUSEBUTTONDOWN 
                    and event.button == 1
                    and self.rect.collidepoint(pg.mouse.get_pos()) == True
                ):
                return True
        return False