import pyaudio
import tkinter as tk
import numpy as np
import time
from PIL import Image, ImageDraw, ImageOps, ImageTk

# convert image to circle
def image_to_circle(image_path):
    im = Image.open(image_path)
    # create mask
    mask = Image.new('L', im.size)
    draw = ImageDraw.Draw(mask)

    draw.ellipse((0, 0) + mask.size,  fill = 255)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save('out.png')


image_to_circle('test.png')

# setup stream
pa = pyaudio.PyAudio()
stream = pa.open(
    rate = 44100,
    frames_per_buffer = 1024,
    input = True,
    channels = 1,
    format = pyaudio.paInt16
)

# create the window
root = tk.Tk()
root.geometry('600x400')

# add canvas
canvas = tk.Canvas(root, background = 'black', highlightthickness=0)
canvas.pack(fill='both', expand=True)


def draw(audio_data):
    canvas.delete('all')

    max_circle_size = 200 + (np.max(audio_data) - np.min(audio_data))

    if max_circle_size < 220:
        max_circle_size = 200
    
    circle_x = (root.winfo_width() - max_circle_size) / 2
    circle_y = (root.winfo_height() - max_circle_size) / 2
    end_x = circle_x + max_circle_size
    end_y = circle_y + max_circle_size


    image_x = (root.winfo_width() / 2)
    image_y = (root.winfo_height() / 2)
    image = ImageTk.PhotoImage(Image.open('out.png').resize((
        200, 
        200
    )))

    root.image = image

    
    # draw circle
    time.sleep(0.005)
    canvas.create_oval(circle_x, circle_y, end_x, end_y, fill = '#0984e3')

    # draw image in the center of circle
    canvas.create_image((image_x, image_y), image = image)




while True:
    try:
        audio_data = np.frombuffer(stream.read(1024), dtype = np.int16)
        draw(audio_data)
        root.update_idletasks()
        root.update()
    except tk.TclError as e:
        print(e)
        break



stream.stop_stream()
stream.close()
#root.mainloop()
