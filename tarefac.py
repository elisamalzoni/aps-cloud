class Tarefa():
    
    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done

    def set_title(self, title):
        self.title = title
    
    def set_description(self, description):
        self.description = description
    
    def set_done(self, done):
        self.done = done

    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_done(self):
        return self.done
