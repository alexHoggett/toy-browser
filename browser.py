import tkinter
from url import URL

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

def lex(body):
   text = ""
   in_tag = False
   in_entity = False
   entity = ""
   for c in body:
      if c == "<":
         in_tag = True
      elif c == ">":
         in_tag = False
      elif c == "&":
         in_entity = True
      elif in_entity:
         entity += c
         if entity in ("lt;", "gt;"):
            text += "<" if entity == "lt;" else ">"
            in_entity = False
            entity = ""
      elif not in_tag:
         text += c
   return text

def layout(text, width):
   display_list = []
   cursor_x, cursor_y = HSTEP, VSTEP
   for c in text:
      if c == '\n':
         cursor_y += (VSTEP * 1.1)
         cursor_x = HSTEP
      else:
         display_list.append((cursor_x, cursor_y, c))
         cursor_x += HSTEP

      if cursor_x >= width - HSTEP:
         cursor_y += VSTEP
         cursor_x = HSTEP
   return display_list

class Browser:
   def __init__(self):
      self.window = tkinter.Tk()

      self.width = WIDTH
      self.height = HEIGHT

      self.canvas = tkinter.Canvas(
         self.window,
         width=self.width,
         height=self.height
      )
      self.canvas.pack(fill=tkinter.BOTH, expand=True)
      self.scroll = 0
      self.window.bind("<Down>", self.scrolldown)
      self.window.bind("<Up>", self.scrollup)
      self.window.bind("<MouseWheel>", self.scrollwheel)
      self.window.bind("<Configure>", self.resize)

   def load(self, url):
      self.text = lex(url.request())
      self.display_list = layout(self.text, self.width)
      self.draw()

   def draw(self):
      self.canvas.delete("all")
      for x, y, c in self.display_list:
         if y > self.scroll + HEIGHT: continue
         if y + VSTEP < self.scroll: continue
         self.canvas.create_text(x, y - self.scroll, text=c)

   def scrolldown(self, e):
      self.scroll += SCROLL_STEP
      self.draw()

   def scrollup(self, e):
      if self.scroll > 0 + SCROLL_STEP:
         self.scroll -= SCROLL_STEP
      self.draw()

   def scrollwheel(self, e):
      self.scroll -= e.delta * 5
      self.draw()

   def resize(self, e):
      # if self.canvas.winfo_width() == e.width and self.canvas.winfo_height() == e.height:
      #   return  # Avoid unnecessary resizing
      print('resizing')
      print(e.width, e.height)
      self.width, self.height = e.width, e.height
      self.display_list = layout(self.text, self.width)
      self.draw()

      
if __name__ == "__main__":
   import sys
   Browser().load(URL(sys.argv[1]))
   tkinter.mainloop()