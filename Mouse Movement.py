
import pygame, math

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((800, 800))
   # set the title of the display window
   pygame.display.set_caption('A template for graphical games with two moving dots')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.default_color = 'red'
      self.small_dot = Dot(self.default_color, 10, [400, 400], [1, 2], self.surface)

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            #self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
         if event.type == pygame.KEYUP:
            self.handle_keyup(event)
            
         if event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouseup(event)
            
         if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mousedown(event)
            
         if event.type == pygame.MOUSEMOTION:  # allows us to move the dot
            self.handle_mouse_motion(event)
   
   def handle_mouse_motion(self, event):
      print(event)
      if event.buttons == (1, 0, 0):  # checks if only the left mouse button is clicked
         self.small_dot.set_center(event.pos)  # event.pos = position of the event
            
   def handle_mousedown(self, event):
      print(event)
      # collidepoint checks if click is inside the dot
      # stops the dot only when inside of the dot is clicked
      if event.button == 1 and self.small_dot.collidepoint(event.pos):  # checks if position of click is inside the dot
         self.small_dot.stop()
         print("press")
         self.small_dot.shape(self)
                  

   def handle_mouseup(self, event):
      # Dot stops moving when the mouse is clicked and moves again when cloced again
      print(event)
      if event.button == 3:
         if self.small_dot.collidepoint(event.pos):
            self.small_dot.stop()
         else:
            self.small_dot.restart()
      if event.button == 1:
         self.small_dot.restart()

   def handle_keyup(self, event):
      if event.key == pygame.K_r or event.key == pygame.K_g or event.key == pygame.K_b:
         self.small_dot.set_color(self.default_color)
            
   def handle_keydown(self, event):
      if event.key == pygame.mouse.get_pressed(1):
         print("press")
         self.small_dot.shape(self)
         
         
      #if event.key == pygame.K_r:
         #self.small_dot.set_color('red')
      #if event.key == pygame.K_g:
         #self.small_dot.set_color('green')
      #if event.key == pygame.K_b:
         #self.small_dot.set_color('blue')
      #if event.key == pygame.K_SPACE:
         #self.small_dot.set_color(self.default_color)

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.small_dot.draw()
      pygame.display.update() # make the updated surface appear on the display

   #def update(self):
      ## Update the game objects for the next frame.
      ## - self is the Game to update
      
      #self.small_dot.move()

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      pass
      


class Dot:
   # An object in this class represents a Dot that moves 
   
   def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):
      # Initialize a Dot.
      # - self is the Dot to initialize
      # - color is the pygame.Color of the dot
      # - center is a list containing the x and y int
      #   coords of the center of the dot
      # - radius is the int pixel radius of the dot
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object

      self.color = pygame.Color(dot_color)
      self.radius = dot_radius
      self.center = dot_center
      self.velocity = dot_velocity
      self.velocity_backup = dot_velocity
      self.surface = surface
      
   
   def stop(self):
      # stops the movement of the dot by setting its velocity to zero
      # self is the dot
      self.velocity = [0, 0]
      
   def restart(self):
      # restarts the movement of the dot by setting the velocity back to its original value
      # - self is the dot
      self.velocity = self.velocity_backup
   
   def collidepoint(self, point):
      # return True if the point is inside the dot; False otherwise
      # - self is the dot
      # - point is a tuple or list representing a point
      
      distance = math.sqrt((self.center[0] - point[0])**2   # math computation tells us the distance to the center
                           + (self.center[1] - point[1])**2)
      return distance <= self.radius  # return statment only returns the distance variable if statement is True (boolean)
     
   def set_center(self, point):
      # sets the center coordinates of the dot to a new point
      # - self is the dot
      # - point is a tuple or a list representing the new point
      self.center[0] = point[0]
      self.center[1] = point[1]  # center list is same as point tuple
      
   def set_color(self, color):
      # Changes the color of the dot
      # - self is the dot
      # - color is a string object representing a color name
      self.color = pygame.Color(color)
   
   def draw(self):
      # Draw the dot on the surface
      # - self is the Dot
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
      
   def shape(self):
      rect_right = False
      rect_left = False
      print("work")
      if self.velocity[0] > 0 and self.velocity[1] > 0:
         rect_right == True
      
      if rect_right == True:
         pass
         
      
         

main()