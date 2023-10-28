from tkinter import *
from random import randint,choices,choice,random
import numpy as np

size = (600, 400)

root = Tk()
root.title('Fireworks Animation')
canvas = Canvas(root, background='black', width=size[0], height=size[1])
canvas.pack()

center = (size[0]/2, size[1]/2)

def get_random_color(mode=0):
    match mode:
        case 0:
            return f"#{''.join(choices('0123456789ABCDEF', k=6))}"
        case 1:
            return choice(('red', 'white', 'blue'))

class Particle():
    def __init__(self, x, y, firework_size, size, color):
        self.x = x
        self.y = y
        
        self.color = color
        self.size = size
        
        self.offset = (firework_size - size) / 2

class Trail(Particle):
    def __init__(self, x, y, firework_size, size, color):
        super().__init__(x, y, firework_size, size, color)
        
        self.trail = canvas.create_rectangle(
            self.x + self.offset,
            self.y + self.offset,
            self.x + self.offset + self.size,
            self.y - self.offset - self.size,
            outline = self.color,
            fill = self.color
        )
    
    def erase(self):
        canvas.delete(self.trail)

class Spark(Particle):
    firework_trails_limit = 6
    firework_explode_force_steps_limit = 10
    
    trail_size = 2
    
    def __init__(self, x, y, firework_size, size, color, radians):
        super().__init__(x, y, firework_size, size, color)
        
        self.radians = radians
        self.random_force_score = random()
        
        self.step = 0
        
        self.trails = []
        
        self.spark = canvas.create_rectangle(
            self.x + self.offset,
            self.y + self.offset,
            self.x + self.offset + self.size,
            self.y + self.offset - self.size,
            outline = self.color,
            fill = self.color
        )
    
    def update_coords(self):
        canvas.coords(
            self.spark,
            self.x + self.offset,
            self.y + self.offset,
            self.x + self.offset + self.size,
            self.y + self.offset - self.size
        )
    
    def destroy(self):
        for obj in self.trails:
            obj.erase()
        self.trails.clear()
        
        self.erase()
    
    def move(self):
        if self.y > size[1] * 1.5:
            self.destroy()
            return False
        
        self.trails.append(Trail(self.x + self.offset, self.y + self.offset, self.size, self.trail_size, self.color))
        
        if len(self.trails) >= self.firework_trails_limit:
            self.trails[0].erase()
            self.trails.pop(0)
        
        x_speed = max((0.2, (self.firework_explode_force_steps_limit - self.step) * self.random_force_score))
        y_speed = max((1, (self.firework_explode_force_steps_limit - self.step) * self.random_force_score))
        
        if self.step > self.firework_explode_force_steps_limit * 3:
            x_speed /= 4
        
        self.x += np.cos(self.radians) * 2 * x_speed
        self.y -= np.sin(self.radians) * 2 * y_speed
        
        if self.step > self.firework_explode_force_steps_limit:
            self.y += self.step / self.firework_explode_force_steps_limit
        
        self.update_coords()
        
        self.step += 1
        
        return True
    
    def erase(self):
        canvas.delete(self.spark)


class Firework():
    firework_size = 8
    firework_speed = 2
    firework_duration_expire = 2
    firework_trails_limit = 6
    
    trail_size = 4
    
    spark_size = 4
    sparks_number = 120
    
    def __init__(self, x, duration, steps_delay, color):
        self.x = x
        self.y = size[1] + self.firework_size*2

        self.color = color
        self.steps_delay = steps_delay
        self.duration = duration + self.firework_duration_expire
        
        self.trails = []
        self.sparks = []
        
        self.firework = canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.firework_size,
            self.y - self.firework_size,
            outline = self.color,
            fill = self.color
        )
    
    def update_coords(self):
        canvas.coords(
            self.firework,
            self.x,
            self.y,
            self.x + self.firework_size,
            self.y - self.firework_size
        )
        
    def move(self):
        if not self.steps_delay > 0:
            if self.duration - self.firework_duration_expire > 0:
                self.trails.append(Trail(self.x, self.y, self.firework_size, self.trail_size, self.color))
                
                if len(self.trails) >= self.firework_trails_limit:
                    self.trails[0].erase()
                    self.trails.pop(0)
                
                self.y -= np.log2(self.duration) * self.firework_speed
                self.duration -= 1 * self.firework_speed
                
                self.update_coords()
            else:
                if self.trails:
                    for obj in self.trails:
                        obj.erase()
                    self.trails.clear()
                    
                    self.erase()
                
                    self.sparks = list(
                        map(
                            lambda radians: 
                                Spark(self.x, self.y, self.firework_size, self.spark_size, self.color, radians),
                            np.arange(0, np.pi*2, np.pi*2/self.sparks_number)
                        )
                    )
                
                move_result = [spark.move() for spark in self.sparks]
                
                if not any(move_result):
                    return False
        else:
            self.steps_delay -= 1
            
        return True
            
    
    def erase(self):
        canvas.delete(self.firework)
        
fireworks = [Firework(randint(0+10, size[0]-10), randint(50, 78), randint(0, 200), get_random_color()) for _ in range(7)]

def move():
    for firework_id in range(len(fireworks)):
        move_result = fireworks[firework_id].move()
        
        if not move_result:
            fireworks[firework_id].__init__(randint(0+10, size[0]-10), randint(50, 78), randint(0, 100), get_random_color())
            
    root.after(16, move)

move()
 
root.mainloop()