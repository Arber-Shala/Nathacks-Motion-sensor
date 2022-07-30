import pygame, math

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((800, 800))
   # set the title of the display window
   pygame.display.set_caption('A template for graphical games with two moving Points')   
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
      self.button_press = False
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.default_color = 'red'
      self.small_Point = Point(self.default_color, 10, [400, 400], [1, 2], self.surface)

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
            self.button_press = False 
            
         if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mousedown(event)
            if (self.button_press == False):
               self.button_press = True


         if event.type == pygame.MOUSEMOTION:  # allows us to move the Point
            if self.button_press == True:
               self.handle_mouse_motion(event)
            
   
            
         
   def handle_mouse_motion(self, event):
      print('handle_mouse_motion')
      print(event)
      if event.buttons == (1, 0, 0):  # checks if only the left mouse button is clicked
         self.small_Point.set_center(event.pos)  # event.pos = position of the event
         
            
   def handle_mousedown(self, event):
      print('handle_mousedown')
      print(event)
      # collidePoint checks if click is inside the Point
      # stops the Point only when inside of the Point is clicked
      if event.button == 1 and self.small_Point.collidePoint(event.pos):  # checks if position of click is inside the Point
         self.small_Point.stop()
         print("press")
         # self.small_Point.shape(self)
                  

   def handle_mouseup(self, event):
      # Point stops moving when the mouse is clicked and moves again when cloced again
      print(event)
      print('handle_mouseup')
      if event.button == 3:
         if self.small_Point.collidePoint(event.pos):
            self.small_Point.stop()
         else:
            self.small_Point.restart()
      if event.button == 1:
         self.small_Point.restart()

   def handle_keyup(self, event):
      if event.key == pygame.K_r or event.key == pygame.K_g or event.key == pygame.K_b:
         self.small_Point.set_color(self.default_color)
            
   def handle_keydown(self, event):
      if event.key == pygame.mouse.get_pressed(1):
         print("press")
         self.small_Point.shape(self)
         
         
      #if event.key == pygame.K_r:
         #self.small_Point.set_color('red')
      #if event.key == pygame.K_g:
         #self.small_Point.set_color('green')
      #if event.key == pygame.K_b:
         #self.small_Point.set_color('blue')
      #if event.key == pygame.K_SPACE:
         #self.small_Point.set_color(self.default_color)

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.small_Point.draw()
      pygame.display.update() # make the updated surface appear on the display

   #def update(self):
      ## Update the game objects for the next frame.
      ## - self is the Game to update
      
      #self.small_Point.move()

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      pass
      


class Point:
   # An object in this class represents a Point that moves 
   
   def __init__(self, Point_color, Point_radius, Point_center, Point_velocity, surface):
      # Initialize a Point.
      # - self is the Point to initialize
      # - color is the pygame.Color of the Point
      # - center is a list containing the x and y int
      #   coords of the center of the Point
      # - radius is the int pixel radius of the Point
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object

      self.color = pygame.Color(Point_color)
      self.radius = Point_radius
      self.center = Point_center
      self.velocity = Point_velocity
      self.velocity_backup = Point_velocity
      self.surface = surface
      
   
   def stop(self):
      # stops the movement of the Point by setting its velocity to zero
      # self is the Point
      self.velocity = [0, 0]
      
   def restart(self):
      # restarts the movement of the Point by setting the velocity back to its original value
      # - self is the Point
      self.velocity = self.velocity_backup
   
   def collidePoint(self, Point):
      # return True if the Point is inside the Point; False otherwise
      # - self is the Point
      # - Point is a tuple or list representing a Point
      
      distance = math.sqrt((self.center[0] - Point[0])**2   # math computation tells us the distance to the center
                           + (self.center[1] - Point[1])**2)
      return distance <= self.radius  # return statment only returns the distance variable if statement is True (boolean)
     
   def set_center(self, Point):
      # sets the center coordinates of the Point to a new Point
      # - self is the Point
      # - Point is a tuple or a list representing the new Point
      self.center[0] = Point[0]
      self.center[1] = Point[1]  # center list is same as Point tuple
      
   def set_color(self, color):
      # Changes the color of the Point
      # - self is the Point
      # - color is a string object representing a color name
      self.color = pygame.Color(color)
   
   def draw(self):
      # Draw the Point on the surface
      # - self is the Point
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
      
      
   def shape(self):
      coordinates = []
      
      rect_right = False
      rect_up = False
      rect_left = False
      rect_down = False
      print("work")
      if self.velocity[0] > 0 and self.velocity[1] == 0:
         rect_right == True
         
         if rect_right == True:
            if self.velocity[0] == 0 and self.velocty[1] < 0:
               rect_up == True
                  
               if rect_up == True:
                  if self.velocity[0] < 0 and self.veloct[1] == 0:
                     rect_left == True
                        
                     if rect_left == True:
                        if self.velocity[0] == 0 and self.velocity[1] > 0:
                           rect_down == True
                           
      if rect_right == True and rect_up == True and rect_left == True and rect_down == True:
         print("Rectangle")
           
      
         

main()