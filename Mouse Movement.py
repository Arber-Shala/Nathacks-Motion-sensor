
import pygame
import math

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
      self.button_press = False
      self.close_clicked = False
      self.continue_game = True


      self.orgin = (0,0)
      self.rel_list = []
      self.clean_list = []
      self.angle_change = 0
      self.closed_shape = None
      self.shape=None
      
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
            self.draw_shape(self.clean_list)
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
            self.closed_shape = None
            if (len(self.rel_list) <10 ): 
               break
            # print(self.rel_list)
            #clean the error bit at the beginning 
            self.rel_list = self.rel_list[3:]
            self.rel_list = [i for i in self.rel_list if i != (0,0)]
            # self.rel_list.remove((0,0))
            # print('ref list')
            # print(self.rel_list)
            self.cleaning_list(self.rel_list)
            # print('clean ')
            # print(self.clean_list)



            self.clean_list = self.approx_data(self.clean_list, 4)
            # print('after approx')
            # print(self.clean_list)
            # print('after 2 clean')
            self.clean_list = [i for i in self.clean_list if i != (0,0)]
            self.cleaning_list(self.clean_list)
            # print(self.clean_list)


            

            self.clean_list = self.approx_angle_data(self.clean_list, 25)
            # print('after 1 angle apprx')
            # print(self.clean_list)
            
            self.clean_list = [i for i in self.clean_list if abs(i[0])>20 or abs(i[1])>20]
            # print('clean 1 angle apprx')

            # print(self.clean_list)
            # print(f'angle change after 1  is {self.angle_change}')

            self.clean_list = self.approx_angle_data(self.clean_list, 25)
            # print('after 2 angle apprx')
            # print(self.clean_list)

            # print('after 3 angle apprx')
            # print(f'angle change after 2  is {self.angle_change}')
            self.check_closed_shape(self.clean_list,50)
            self.clean_list = self.approx_angle_data(self.clean_list, 25)
            

            print('results:')
            print(self.clean_list)

           

            self.clean_list = [i for i in self.clean_list if abs(i[0])>20 or abs(i[1])>20]
            # print(self.clean_list)
            # print(f'angle change after 3  is {self.angle_change}')
            
            self.check_closed_shape(self.clean_list,50)
            print(f'shape is close: {self.closed_shape}')
            if self.closed_shape == True:
               self.update_if_closed(25)
            
            print(f'angle change final is {self.angle_change}')
            
            self.check_shape(self.clean_list)



            #draw the shape
            

         

         if event.type == pygame.MOUSEBUTTONDOWN:
            self.rel_list = []
            # self.surface.fill(self.bg_color) # clear the display surface first
            
            self.handle_mousedown(event)
            if (self.button_press == False):
               self.button_press = True


         if event.type == pygame.MOUSEMOTION:  # allows us to move the dot
            if self.button_press == True:
               self.handle_mouse_motion(event)


   def draw_shape(self, mylist ):
      start_pos = self.orgin
      # print(f'start is {start_pos}')

      for i in mylist:
         end_pos = (start_pos[0]+ i[0], start_pos[1] +i[1])
         
         pygame.draw.line(self.surface, self.default_color,start_pos,end_pos ,5)
         start_pos = end_pos


   def check_shape(self, mylist):
      # 1 line : is it a line
      if len(mylist) == 1 :
         self.shape ='Line'
         print(f'we got one: {self.shape}')
         line  = pygame.mixer.Sound('line.wav')
         line.play()
      
      # 2 line : is it a angle 
      elif len(mylist) ==2 :
         if  self.angle_change == 1 and self.closed_shape == False:
            self.shape ='Angle'
            print(f'we got one: {self.shape}')
            pygame.mixer.Sound('angle.wav').play()
                  
         else: 
            self.shape ='Return Line'
            print(f'we got one: {self.shape}')
      # 3 line : is it a triangle 
      elif len(mylist) == 3:
         if  self.angle_change == 3 and self.closed_shape == True:
            self.shape ='TRIangle'
            print(f'we got one: {self.shape}')
            pygame.mixer.Sound('Triangle.wav').play()
                  
         else: 
            self.shape ='3 line Non-Triangle'
            print(f'we got one: {self.shape}')
            pygame.mixer.Sound('threeconnectline.wav').play()
      
      # 4 line : is it a 
      elif len(mylist) == 4:
         angle1 = pygame.math.Vector2.angle_to(pygame.Vector2(1,0),mylist[0] )
         angle2 = pygame.math.Vector2.angle_to(pygame.Vector2(1,0),mylist[1] )
         angle3 = pygame.math.Vector2.angle_to(pygame.Vector2(1,0),mylist[2] )
         angle4 = pygame.math.Vector2.angle_to(pygame.Vector2(1,0),mylist[3] )
        
         # print( abs(angle2-angle1) )
         # print (abs(angle3-angle2))
         # print (abs(angle4-angle3) )
         # print (abs(angle1-angle4))
         diffi_1= round((int(abs(angle2-angle1)/10)*10))
         diffi_2= round((int(abs(angle3-angle2)/10)*10))
         diffi_3= round((int(abs(angle4-angle3)/10)*10))
         diffi_4= round((int(abs(angle1-angle4)/10)*10))
         # print (diffi_1)
         # print (diffi_2)
         # print (diffi_3)
         # print (diffi_4)
         #  if abs(math.sin(abs(angle2-angle1))) == 1 and abs(math.sin(abs(angle3-angle2)))==1:
         if  self.angle_change == 4 and self.closed_shape == True:
            if ((diffi_1 >=75 and diffi_1 <=105) or (diffi_1 >= 225 and diffi_1 <= 285) )and ((diffi_2 >=75 and diffi_2 <=105) or (diffi_2 >= 225 and diffi_2 <= 285) ):
               if (round(abs(mylist[0][0])/10)*10 == round(abs(mylist[1][0])/10)*10) and (round(abs(mylist[0][1])/10)*10 == round(abs(mylist[1][1])/10)*10):
                  self.shape ='Square'
                  print(f'we got one: {self.shape}')
                  pygame.mixer.Sound('square.wav').play()
               else:
                  self.shape ='Rectangle'
                  print(f'we got one: {self.shape}')
                  pygame.mixer.Sound('rectangle.wav').play()
            
            elif( abs(math.sin(diffi_1)) == abs(math.sin(diffi_3)) ) and  (abs(math.sin(diffi_2)) == abs(math.sin(diffi_4))): 
               self.shape ='Parallelogram'
               print(f'we got one: {self.shape}')
               pygame.mixer.Sound('paral.wav').play()
            else:
               self.shape ='Quadrilaterals'
               print(f'we got one: {self.shape}')
               pygame.mixer.Sound('quard.wav').play()
                  
         else: 
            self.shape ='4 line non close shape '
            print(f'we got one: {self.shape}')
            pygame.mixer.Sound('fourconnect.wav').play()


      else: 
         self.shape ='U F O!! PWEEE PWEE PWEEE!!!'
         print(f'we got one: {self.shape}')

   
   def update_if_closed(self, approx):
         angle = pygame.math.Vector2.angle_to(pygame.Vector2(1,0),self.clean_list[0] )
         angle1 = pygame.math.Vector2.angle_to(pygame.Vector2(1,0),self.clean_list[len(self.clean_list)-1])
         if abs(angle1-angle) > approx:
       
            self.angle_change =  self.angle_change +1  

         else:
            self.clean_list[len(self.clean_list)-1] = (self.clean_list[len(self.clean_list)-1][0] + self.clean_list[0][0],self.clean_list[len(self.clean_list)-1][1] + self.clean_list[0][1] )
            del self.clean_list[0]
      


   # def define_shape():
   def check_closed_shape(self, mylist,approx):
      sum_vectors = (0,0)
      for i in mylist:
         sum_vectors = (sum_vectors[0]+i[0], sum_vectors[1]+i[1])
      
      if (abs(sum_vectors[0]) < approx and abs(sum_vectors[1]) < approx):

         self.closed_shape = True

      else: 
         self.closed_shape = False




   def approx_data(self, list, approx):
      result = []
      count = 0

      while (count <(len(list))):
         for vector_i in list :
            if (abs(vector_i[0]) <approx):
               if (abs(vector_i[1]) <approx):
                  result.append((0, 0))
               else:   
                  result.append((0,vector_i[1]))
            elif (abs(vector_i[1]) <approx):
               result.append((vector_i[0], 0))
            
            else:
                result.append(vector_i)
            count = count+1

      # print('result')
      # print(result)
      count = 0 

      return result

   def approx_angle_data(self, list, approx):

      self.angle_change =0
      result = []
      count =1
      list_small_angles =[]
      if len(list) < 2:
            # print('list is one')
            result = list
      else: 

         while (count < len(list)):
         
            angle = pygame.math.Vector2.angle_to(pygame.Vector2(1,0),list[count-1] )
            angle1 = pygame.math.Vector2.angle_to(pygame.Vector2(1,0),list[count])
            # print(f'first Vect is: {list[count-1] }')
            # print(f'angle is: {angle}')
            # print(f'sec Vect is: {list[count] }')
            # print(f'sec angle is: {angle1}')

            # print(f' angle diff is {abs(angle1-angle)}')

            #    #((count ==len(list)-2) and (len(list)== 0))
            # print(count)
            if (abs(angle1-angle) > 25) and len(list) == 2:
               # print("     PPPPlus 1: start")
               self.angle_change =  self.angle_change +1  
               result = list
            
            #reach the end of the string 
            elif (count == len(list)-1): 
                  # print("last reached ")
                  if (abs(angle1-angle) > 25):
                     # print("     PPPPlus 1: end")
                     self.angle_change =  self.angle_change +1  

                     list_small_angles.append(list[count-1])
                     tuple_sum =(0,0)
                     # print(f'biger than 25 list is: {list_small_angles}')  
                     for i in list_small_angles:
                     # print(f'is {i}')
                      tuple_sum = (tuple_sum[0]+i[0], tuple_sum[1]+ i[1])
                  # print(f'tuple_sum is: {tuple_sum}')  

                     result.append(tuple_sum)

                     result.append(list[count])

                  else:

                     list_small_angles.append(list[count-1])
                     list_small_angles.append(list[count])

                     tuple_sum =(0,0)

                     # print(f'biger than 25 list is: {list_small_angles}')  
                     for i in list_small_angles:
                     # print(f'is {i}')
                      tuple_sum = (tuple_sum[0]+i[0], tuple_sum[1]+ i[1])
                   # print(f'tuple_sum is: {tuple_sum}')  

                     result.append(tuple_sum)      

                  list_small_angles =[]
            

            else: 

             if ((abs(angle1-angle) > 25)  ): 
                  # print("     PPPPlus 1: mid")
         
                  self.angle_change =  self.angle_change +1
                  list_small_angles.append(list[count-1])

                
                  tuple_sum =(0,0)

                  # print(f'biger than 25 list is: {list_small_angles}')  
                  for i in list_small_angles:
                  # print(f'is {i}')
                     tuple_sum = (tuple_sum[0]+i[0], tuple_sum[1]+ i[1])
                  # print(f'tuple_sum is: {tuple_sum}')  

                  result.append(tuple_sum)

               # if ((count ==len(list)-2) and (len(list)== 0))
               #    print('last one'
                  list_small_angles =[]
                  # print("perdect ")
             else:

                  list_small_angles.append(list[count-1])
               # print(f'list_small_angles add in: {list_small_angles}') 
                  # print("here i am")

               
            count = count +1 
      return result

   def cleaning_list(self, mylist):
      self.clean_list =[]
      self.clean_list.append(mylist[0])
      i = 1
      j = 0

      while (i < len(mylist)):



         if (mylist[i][0] * mylist[i-1][0] > 0) and (mylist[i][1]== 0 and mylist[i-1][1] == 0 ):
            self.clean_list.append((self.clean_list[j][0] + mylist[i][0] , 0))
            del self.clean_list[j]
         
         
         elif (mylist[i][1] * mylist[i-1][1] > 0) and (mylist[i][0]== 0 and  mylist[i-1][0] == 0):
         
            self.clean_list.append((0, self.clean_list[j][1] + mylist[i][1]) )
            del self.clean_list[j]

         elif (mylist[i][0] * mylist[i-1][0] > 0) and (mylist[i][1] * mylist[i-1][1] > 0) :
            if (mylist[i][0] / mylist[i][1] == mylist[i-1][0] / mylist[i-1][1]):
               self.clean_list.append((self.clean_list[j][0] + mylist[i][0] , self.clean_list[j][1] + mylist[i][1]) )
               del self.clean_list[j]

            else:
               self.clean_list.append( mylist[i])
               j= j+1 
               # print('angles not equal  ')

         else:
          self.clean_list.append( mylist[i])
          j= j+1 
         i= i +1
            
         
   def handle_mouse_motion(self, event):
      print('handle_mouse_motion')
      # print(event)
      pos = pygame.mouse.get_pos()
      # print(pos)
      
      self.rel_list.append(pygame.mouse.get_rel())

      # print(self.rel_list)
      if event.buttons == (1, 0, 0):  # checks if only the left mouse button is clicked
         self.small_dot.set_center(event.pos)  # event.pos = position of the event
         
            
   def handle_mousedown(self, event):
      print('handle_mousedown')
      print(event)
      pos = pygame.mouse.get_pos()
      print(pos)
      self.orgin = pos
      # collidepoint checks if click is inside the dot
      # stops the dot only when inside of the dot is clicked
      if event.button == 1 and self.small_dot.collidepoint(event.pos):  # checks if position of click is inside the dot
         self.small_dot.stop()
         print("press")
         # self.small_dot.shape(self)
                  

   def handle_mouseup(self, event):
      # Dot stops moving when the mouse is clicked and moves again when cloced again
      print(event)
      print('handle_mouseup')
      # pygame.mixer.Sound('drawshape.wav').play()
      
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
         
         
    
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.small_dot.draw()
      if  self.button_press ==False:
         self.draw_shape(self.clean_list)
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
      
         
      
         

main()