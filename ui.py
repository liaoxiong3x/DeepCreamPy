"""
Code illustration: 6.09
    
    Modules imported here:
        from tkinter import messagebox
        from tkinter import filedialog
    
    Attributes added here:
        file_name = "untitled"
    
    Methods modified here:
        on_new_file_menu_clicked()
        on_save_menu_clicked()
        on_save_as_menu_clicked()
        on_close_menu_clicked()
        on_undo_menu_clicked()
        on_canvas_zoom_in_menu_clicked()
        on_canvas_zoom_out_menu_clicked()
        on_about_menu_clicked()

    Methods added here
        start_new_project()
        actual_save()
        close_window()
        undo()
        canvas_zoom_in()
        canvas_zoom_out()
        
@ Tkinter GUI Application Development Blueprints
"""
import math
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import framework
import decensor
import os

class PaintApplication(framework.Framework):

    def __init__(self, root):
        super().__init__(root)
        self.circle = 0
        self.drawn_img = None
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = 0, 0
        self.current_item = None
        self.fill = "#00ff00"
        self.fill_pil = (0,255,0,255)
        self.outline = "#00ff00"
        self.brush_width = 2
        self.background = 'white'
        self.foreground = "#00ff00"
        self.file_name = "Untitled"
        self.tool_bar_functions = (
            "draw_line", "draw_irregular_line"
        )
        self.selected_tool_bar_function = self.tool_bar_functions[0]
        
        self.create_gui()
        self.bind_mouse()

        # Create blank image to avoid errors with irregular line drawing on blank canvas
        # TODO: Optimize this, seems too inefficient
        self.canvas.img = Image.new('RGB', (800,1280), (255, 255, 255))
        self.canvas.img_width, self.canvas.img_height = self.canvas.img.size
        # make reference to image to prevent garbage collection
        # https://stackoverflow.com/questions/20061396/image-display-on-tkinter-canvas-not-working
        self.canvas.tk_img = ImageTk.PhotoImage(self.canvas.img)
        self.canvas.config(width=self.canvas.img_width, height=self.canvas.img_height)
        self.canvas.create_image(self.canvas.img_width / 2.0, self.canvas.img_height / 2.0, image=self.canvas.tk_img)

        self.drawn_img = Image.new("RGBA", self.canvas.img.size)
        self.drawn_img_draw = ImageDraw.Draw(self.drawn_img)

    def on_new_file_menu_clicked(self, event=None):
        self.start_new_project()

    def start_new_project(self):
        self.canvas.delete(tk.ALL)
        self.canvas.config(bg="#ffffff")
        self.root.title('untitled')

    def on_open_image_menu_clicked(self, event=None):
        self.open_image()

    def open_image(self):
        self.file_name = filedialog.askopenfilename(master=self.root, title="Open...")
        print(self.file_name)
        self.canvas.img = Image.open(self.file_name)
        self.canvas.img_width, self.canvas.img_height = self.canvas.img.size
        #make reference to image to prevent garbage collection
        #https://stackoverflow.com/questions/20061396/image-display-on-tkinter-canvas-not-working
        self.canvas.tk_img = ImageTk.PhotoImage(self.canvas.img)
        self.canvas.config(width=self.canvas.img_width, height=self.canvas.img_height)
        self.canvas.create_image(self.canvas.img_width/2.0,self.canvas.img_height/2.0,image=self.canvas.tk_img)

        self.drawn_img = Image.new("RGBA", self.canvas.img.size)
        self.drawn_img_draw = ImageDraw.Draw(self.drawn_img)


    def on_import_mask_clicked(self, event=None):
        self.import_mask()

    def display_canvas(self):
        composite_img = Image.alpha_composite(self.canvas.img.convert('RGBA'), self.drawn_img).convert('RGB')
        self.canvas.tk_img = ImageTk.PhotoImage(composite_img)

        self.canvas.create_image(self.canvas.img_width/2.0,self.canvas.img_height/2.0,image=self.canvas.tk_img)

    def import_mask(self):
        file_name_mask = filedialog.askopenfilename(master=self.root, filetypes = [("All Files","*.*")], title="Import mask...")
        mask_img = Image.open(file_name_mask)
        if (mask_img.size != self.canvas.img.size):
            messagebox.showerror("Import mask", "Mask image size does not match the original image size! Mask image not imported.")
            return
        self.drawn_img = mask_img
        self.drawn_img_draw = ImageDraw.Draw(self.drawn_img)
        self.display_canvas()

    def on_save_menu_clicked(self, event=None):
        if self.file_name == 'untitled':
            self.on_save_as_menu_clicked()
        else:
            self.actual_save()

    def on_save_as_menu_clicked(self):
        file_name = filedialog.asksaveasfilename(
            master=self.root, filetypes=[('All Files', ('*.png'))], title="Save...")
        if not file_name:
            return
        self.file_name = file_name
        self.actual_save()

    def actual_save(self):
        self.canvas.postscript(file=self.file_name, colormode='color')
        self.root.title(self.file_name)

    def on_close_menu_clicked(self):
        self.close_window()

    def close_window(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def on_undo_menu_clicked(self, event=None):
        self.undo()

    def undo(self):
        items_stack = list(self.canvas.find("all"))
        try:
            last_item_id = items_stack.pop()
        except IndexError:
            return
        self.canvas.delete(last_item_id)

    def on_canvas_zoom_in_menu_clicked(self):
        self.canvas_zoom_in()

    def on_canvas_zoom_out_menu_clicked(self):
        self.canvas_zoom_out()

    def canvas_zoom_in(self):
        self.canvas.scale("all", 0, 0, 1.2, 1.2)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        self.canvas.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

    def canvas_zoom_out(self):
        self.canvas.scale("all", 0, 0, .8, .8)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        self.canvas.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

    def on_decensor_menu_clicked(self, event=None):
        combined_img = Image.alpha_composite(self.canvas.img.convert('RGBA'), self.drawn_img)
        decensorer = decensor.Decensor()
        print(self.file_name)
        orig_name = self.file_name
        path, file = os.path.split(self.file_name)
        name, ext = os.path.splitext(file)
        name = name + "_decensored"
        self.file_name = os.path.join(path, name + ext)
        print(self.file_name)
        decensorer.decensor_image(combined_img.convert('RGB'),combined_img.convert('RGB'), self.file_name)
        messagebox.showinfo(
           "Decensoring", "Decensoring complete! image saved to {save_path}".format(save_path=self.file_name))
        self.file_name = orig_name
    def on_about_menu_clicked(self, event=None):
        # messagebox.showinfo(
        #    "Decensoring", "Decensoring in progress.")
        messagebox.showinfo(
           "About", "Tkinter GUI Application\n Development Blueprints")

    def get_all_configurations_for_item(self):
        configuration_dict = {}
        for key, value in self.canvas.itemconfig("current").items():
            if value[-1] and value[-1] not in ["0", "0.0", "0,0", "current"]:
                configuration_dict[key] = value[-1]
        return configuration_dict

    def canvas_function_wrapper(self, function_name, *arg, **kwargs):
        func = getattr(self.canvas, function_name)
        func(*arg, **kwargs)

    def adjust_canvas_coords(self, x_coordinate, y_coordinate):
        # low_x, high_x = self.x_scroll.get()
        # percent_x = low_x/(1+low_x-high_x)

        # low_y, high_y = self.y_scroll.get()
        # percent_y = low_y/(1+low_y-high_y)
        
        low_x, high_x = self.x_scroll.get()
        low_y, high_y = self.y_scroll.get()
        #length_y = high_y - low_y
        return low_x * 800 + x_coordinate, low_y * 800 + y_coordinate

    def create_circle(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def draw_irregular_line(self):
        # self.current_item = self.canvas.create_line(
        #    self.start_x, self.start_y, self.end_x, self.end_y, fill=self.fill, width=self.brush_width)
        # self.current_item = self.create_circle(self.end_x, self.end_y, self.brush_width/2.0, fill=self.fill, width=0)

        #draw in PIL
        self.drawn_img_draw.line((self.start_x, self.start_y, self.end_x, self.end_y), fill=self.fill_pil, width=int(self.brush_width))
        self.drawn_img_draw.ellipse((self.end_x - self.brush_width/2.0, self.end_y - self.brush_width/2.0, self.end_x + self.brush_width/2.0, self.end_y + self.brush_width/2.0), fill=self.fill_pil)

        self.display_canvas()
        # composite_img = Image.alpha_composite(self.canvas.img.convert('RGBA'), self.drawn_img).convert('RGB')
        # self.canvas.tk_img = ImageTk.PhotoImage(composite_img)

        # self.canvas.create_image(self.canvas.img_width/2.0,self.canvas.img_height/2.0,image=self.canvas.tk_img)

        self.canvas.bind("<B1-Motion>", self.draw_irregular_line_update_x_y)

    # Creates circular indicator for brush size, modified from https://stackoverflow.com/questions/42631060/draw-a-defined-size-circle-around-cursor-in-tkinter-python
    def motion(self, event=None):
        x, y = event.x, event.y
        # the addition is just to center the oval around the center of the mouse
        # remove the the +3 and +7 if you want to center it around the point of the mouse


        self.canvas.delete(self.circle)  # to refresh the circle each motion

        radius = self.brush_width/2.0  # change this for the size of your circle

        x_max = x + radius
        x_min = x - radius
        y_max = y + radius
        y_min = y - radius

        self.circle = self.canvas.create_oval(x_max, y_max, x_min, y_min, outline="black")

    def draw_irregular_line_update_x_y(self, event=None):
        self.start_x, self.start_y = self.end_x, self.end_y
        self.end_x, self.end_y = self.adjust_canvas_coords(event.x, event.y)
        # self.motion(event)
        self.draw_irregular_line()
        self.motion(event)
    def draw_irregular_line_options(self):
        self.create_fill_options_combobox()
        self.create_width_options_combobox()

    def on_tool_bar_button_clicked(self, button_index):
        self.selected_tool_bar_function = self.tool_bar_functions[button_index]
        self.remove_options_from_top_bar()
        self.display_options_in_the_top_bar()
        self.bind_mouse()

    def float_range(self, x, y, step):
        while x < y:
            yield x
            x += step

    def set_foreground_color(self, event=None):
        self.foreground = self.get_color_from_chooser(
            self.foreground, "foreground")
        self.color_palette.itemconfig(
            self.foreground_palette, width=0, fill=self.foreground)

    def set_background_color(self, event=None):
        self.background = self.get_color_from_chooser(
            self.background, "background")
        self.color_palette.itemconfig(
            self.background_palette, width=0, fill=self.background)

    def get_color_from_chooser(self, initial_color, color_type="a"):
        color = colorchooser.askcolor(
            color=initial_color,
            title="select {} color".format(color_type)
        )[-1]
        if color:
            return color
        # dialog has been cancelled
        else:
            return initial_color

    def try_to_set_fill_after_palette_change(self):
        try:
            self.set_fill()
        except:
            pass

    def try_to_set_outline_after_palette_change(self):
        try:
            self.set_outline()
        except:
            pass

    def display_options_in_the_top_bar(self):
        self.show_selected_tool_icon_in_top_bar(
            self.selected_tool_bar_function)
        options_function_name = "{}_options".format(self.selected_tool_bar_function)
        func = getattr(self, options_function_name, self.function_not_defined)
        func()

    def draw_line_options(self):
        self.create_fill_options_combobox()
        self.create_width_options_combobox()

    def create_fill_options_combobox(self):
        tk.Label(self.top_bar, text='Fill:').pack(side="left")
        self.fill_combobox = ttk.Combobox(
            self.top_bar, state='readonly', width=5)
        self.fill_combobox.pack(side="left")
        self.fill_combobox['values'] = ('none', 'fg', 'bg', 'black', 'white')
        self.fill_combobox.bind('<<ComboboxSelected>>', self.set_fill)
        self.fill_combobox.set(self.fill)

    def create_outline_options_combobox(self):
        tk.Label(self.top_bar, text='Outline:').pack(side="left")
        self.outline_combobox = ttk.Combobox(
            self.top_bar, state='readonly', width=5)
        self.outline_combobox.pack(side="left")
        self.outline_combobox['values'] = (
            'none', 'fg', 'bg', 'black', 'white')
        self.outline_combobox.bind('<<ComboboxSelected>>', self.set_outline)
        self.outline_combobox.set(self.outline)

    def create_width_options_combobox(self):
        tk.Label(self.top_bar, text='Width:').pack(side="left")
        self.width_combobox = ttk.Combobox(
            self.top_bar, state='readonly', width=3)
        self.width_combobox.pack(side="left")
        self.width_combobox['values'] = (
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50)
        self.width_combobox.bind('<<ComboboxSelected>>', self.set_brush_width)
        self.width_combobox.set(self.brush_width)

    def set_fill(self, event=None):
        fill_color = self.fill_combobox.get()
        if fill_color == 'none':
            self.fill = ''  # transparent
        elif fill_color == 'fg':
            self.fill = self.foreground
        elif fill_color == 'bg':
            self.fill = self.background
        else:
            self.fill = fill_color

    def set_outline(self, event=None):
        outline_color = self.outline_combobox.get()
        if outline_color == 'none':
            self.outline = ''  # transparent
        elif outline_color == 'fg':
            self.outline = self.foreground
        elif outline_color == 'bg':
            self.outline = self.background
        else:
            self.outline = outline_color

    def set_brush_width(self, event):
        self.brush_width = float(self.width_combobox.get())

    def create_color_palette(self):
        self.color_palette = tk.Canvas(self.tool_bar, height=55, width=55)
        self.color_palette.grid(row=10, column=1, columnspan=2, pady=5, padx=3)
        self.background_palette = self.color_palette.create_rectangle(
            15, 15, 48, 48, outline=self.background, fill=self.background)
        self.foreground_palette = self.color_palette.create_rectangle(
            1, 1, 33, 33, outline=self.foreground, fill=self.foreground)
        self.bind_color_palette()

    def bind_color_palette(self):
        self.color_palette.tag_bind(
            self.background_palette, "<Button-1>", self.set_background_color)
        self.color_palette.tag_bind(
            self.foreground_palette, "<Button-1>", self.set_foreground_color)

    def create_current_coordinate_label(self):
        self.current_coordinate_label = tk.Label(
            self.tool_bar, text='x:0\ny: 0 ')
        self.current_coordinate_label.grid(
            row=13, column=1, columnspan=2, pady=5, padx=1, sticky='w')

    def show_current_coordinates(self, event=None):
        x_coordinate = event.x
        y_coordinate = event.y
        coordinate_string = "x:{0}\ny:{1}".format(x_coordinate, y_coordinate)
        self.current_coordinate_label.config(text=coordinate_string)

    def function_not_defined(self):
        pass

    def execute_selected_method(self):
        self.current_item = None
        func = getattr(
            self, self.selected_tool_bar_function, self.function_not_defined)
        func()

    def draw_line(self):
        self.current_item = self.canvas.create_line(
            self.start_x, self.start_y, self.end_x, self.end_y, fill=self.fill, width=self.brush_width)

        # self.drawn_img_draw.line((self.start_x, self.start_y, self.end_x, self.end_y), fill=self.fill_pil, width=self.brush_width)

    def create_tool_bar_buttons(self):
        for index, name in enumerate(self.tool_bar_functions):
            icon = tk.PhotoImage(file='icons/' + name + '.gif')
            self.button = tk.Button(
                self.tool_bar, image=icon, command=lambda index=index: self.on_tool_bar_button_clicked(index))
            self.button.grid(
                row=index // 2, column=1 + index % 2, sticky='nsew')
            self.button.image = icon

    def remove_options_from_top_bar(self):
        for child in self.top_bar.winfo_children():
            child.destroy()

    def show_selected_tool_icon_in_top_bar(self, function_name):
        display_name = function_name.replace("_", " ").capitalize() + ":"
        tk.Label(self.top_bar, text=display_name).pack(side="left")
        photo = tk.PhotoImage(
            file='icons/' + function_name + '.gif')
        label = tk.Label(self.top_bar, image=photo)
        label.image = photo
        label.pack(side="left")

    def bind_mouse(self):
        self.canvas.bind("<Button-1>", self.on_mouse_button_pressed)
        self.canvas.bind(
            "<Button1-Motion>", self.on_mouse_button_pressed_motion)
        self.canvas.bind(
            "<Button1-ButtonRelease>", self.on_mouse_button_released)
        self.canvas.bind("<Motion>", self.on_mouse_unpressed_motion)

    def on_mouse_button_pressed(self, event):
        self.start_x = self.end_x = self.canvas.canvasx(event.x)
        self.start_y = self.end_y = self.canvas.canvasy(event.y)
        self.execute_selected_method()
        self.motion(event)

    def on_mouse_button_pressed_motion(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.canvas.delete(self.current_item)
        self.motion(event)
        self.execute_selected_method()

    def on_mouse_button_released(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.motion(event)

    def on_mouse_unpressed_motion(self, event):
        self.show_current_coordinates(event)
        self.motion(event)

    def create_gui(self):
        self.create_menu()
        self.create_top_bar()
        self.create_tool_bar()
        self.create_tool_bar_buttons()
        self.create_drawing_canvas()
        self.create_color_palette()
        self.create_current_coordinate_label()
        self.bind_menu_accelrator_keys()
        self.show_selected_tool_icon_in_top_bar("draw_line")
        self.draw_line_options()

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        menu_definitions = (
            'File- &New/Ctrl+N/self.on_new_file_menu_clicked, Open/Ctrl+O/self.on_open_image_menu_clicked, Import Mask/Ctrl+M/self.on_import_mask_clicked, Save/Ctrl+S/self.on_save_menu_clicked, SaveAs/ /self.on_save_as_menu_clicked, sep, Exit/Alt+F4/self.on_close_menu_clicked',
            'Edit- Undo/Ctrl+Z/self.on_undo_menu_clicked, sep',
            'View- Zoom in//self.on_canvas_zoom_in_menu_clicked,Zoom Out//self.on_canvas_zoom_out_menu_clicked',
            'Decensor- Decensor/Ctrl+D/self.on_decensor_menu_clicked',
            'About- About/F1/self.on_about_menu_clicked'
        )
        self.build_menu(menu_definitions)

    def create_top_bar(self):
        self.top_bar = tk.Frame(self.root, height=25, relief="raised")
        self.top_bar.pack(fill="x", side="top", pady=2)

    def create_tool_bar(self):
        self.tool_bar = tk.Frame(self.root, relief="raised", width=50)
        self.tool_bar.pack(fill="y", side="left", pady=3)

    def create_drawing_canvas(self):
        self.canvas_frame = tk.Frame(self.root, width=900, height=900)
        self.canvas_frame.pack(side="right", expand="yes", fill="both")
        self.canvas = tk.Canvas(self.canvas_frame, background="white",
                                width=512, height=512, scrollregion=(0, 0, 512, 512))
        self.create_scroll_bar()
        self.canvas.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        self.canvas.img = Image.open('./icons/canvas_top_test.png').convert('RGBA')
        self.canvas.img = self.canvas.img.resize((512,512))
        self.canvas.tk_img = ImageTk.PhotoImage(self.canvas.img)
        self.canvas.create_image(256,256,image=self.canvas.tk_img)

    def create_scroll_bar(self):
        self.x_scroll = tk.Scrollbar(self.canvas_frame, orient="horizontal")
        self.x_scroll.pack(side="bottom", fill="x")
        self.x_scroll.config(command=self.canvas.xview)
        self.y_scroll = tk.Scrollbar(self.canvas_frame, orient="vertical")
        self.y_scroll.pack(side="right", fill="y")
        self.y_scroll.config(command=self.canvas.yview)
        self.canvas.config(
            xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)

    def bind_menu_accelrator_keys(self):
        self.root.bind('<KeyPress-F1>', self.on_about_menu_clicked)
        self.root.bind('<Control-N>', self.on_new_file_menu_clicked)
        self.root.bind('<Control-n>', self.on_new_file_menu_clicked)
        self.root.bind('<Control-s>', self.on_save_menu_clicked)
        self.root.bind('<Control-S>', self.on_save_menu_clicked)
        self.root.bind('<Control-z>', self.on_undo_menu_clicked)
        self.root.bind('<Control-Z>', self.on_undo_menu_clicked)

if __name__ == '__main__':
    root = tk.Tk()
    app = PaintApplication(root)
    root.mainloop()