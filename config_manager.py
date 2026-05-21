class ConfigManager:
    """Клас для збереження та управління станом застосунку."""

    def __init__(self):
        self.input_mode = "Text"  
        self.output_mode = "Text"  
        self.volume = 1.0  
        self.rate = 150  
        self.voice_id = None  

    def set_input_mode(self, mode: str):
        if mode.upper() in ["TEXT", "VOICE"]:
            self.input_mode = mode.capitalize()

    def set_output_mode(self, mode: str):
        if mode.upper() in ["TEXT", "VOICE"]:
            self.output_mode = mode.capitalize()


config = ConfigManager()  
