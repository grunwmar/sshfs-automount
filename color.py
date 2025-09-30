class Color:
    
    def __init__(self, fg:int=None, bg:int=None, st:int=None):
        self.fg = None if fg is None else (fg % 8 + 30 if fg < 10 else (fg-10) % 8 + 90)
        self.bg = None if bg is None else (bg % 8 + 40 if bg < 10 else (bg-10) % 8 + 70)
        self.st = st % 8 if st is not None else None
        
    def __ror__(self, string):
        color_codes = [] 
        
        if self.bg is not None:
            color_codes += [str(self.bg)]
            
        if self.fg is not None:
            color_codes += [str(self.fg)]
            
        if self.st is not None:
            color_codes += [str(self.st)] 
            
        prefix = "\033[" + ";".join(color_codes) + "m"
        return f"{prefix}{string}\033[0m"
