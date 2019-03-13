#
## Copyright (c) 2018, Bradley A. Minch
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met: 
## 
##     1. Redistributions of source code must retain the above copyright 
##        notice, this list of conditions and the following disclaimer. 
##     2. Redistributions in binary form must reproduce the above copyright 
##        notice, this list of conditions and the following disclaimer in the 
##        documentation and/or other materials provided with the distribution. 
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
## POSSIBILITY OF SUCH DAMAGE.
#

import Tkinter as tk
import tkFont, tkMessageBox
import tkplot
from numpy import *
import re, keyword
import smu

if __name__ != '__main__':
    import __main__

class smutake:

    def __init__(self, **kwargs):
        self.state_handler = None

        self.smu = smu.smu()
        if self.smu == None:
            print 'Could not find a USB Source/Measure Unit device.'

        self.background = '#CDCDCD'
        self.delay = 2

        self.root = kwargs.get('parent')
        if self.root == None:
            if __name__ != '__main__':
                self.root = tk.Toplevel(__main__.__root__)
            else:
                self.root = tk.Tk()
            self.root.configure(background = self.background)
            self.root.title('SMUtake')
            self.root.protocol('WM_DELETE_WINDOW', self.shut_down)

        self.function_options = ('SV/MI', 'SI/MV')
        self.primary_source_options = ('CH1', 'CH2')
        self.speed_accuracy_options = ('accurate', 'medium', 'fast')
        self.axes_options = ('linear', 'log')

        self.buffer_lengths = ((1, 1, 1), 
                               (1, 1, 1), 
                               (1, 1, 1), 
                               (1, 1, 1), 
                               (5, 3, 1), 
                               (10, 5, 3))

        self.ch1_function_var = tk.StringVar()
        self.ch1_function_var.set(self.function_options[0])
        self.ch1_source_name_var = tk.StringVar()
        self.ch1_source_name_var.set('')
        self.ch1_source_values_var = tk.StringVar()
        self.ch1_source_values_var.set('')
        self.ch1_measurement_name_var = tk.StringVar()
        self.ch1_measurement_name_var.set('')
        self.ch1_measurement_auto_var = tk.IntVar()
        self.ch1_measurement_auto_var.set(1)
        self.ch1_measurement_plot_var = tk.IntVar()
        self.ch1_measurement_plot_var.set(0)

        self.ch2_function_var = tk.StringVar()
        self.ch2_function_var.set(self.function_options[0])
        self.ch2_source_name_var = tk.StringVar()
        self.ch2_source_name_var.set('')
        self.ch2_source_values_var = tk.StringVar()
        self.ch2_source_values_var.set('')
        self.ch2_measurement_name_var = tk.StringVar()
        self.ch2_measurement_name_var.set('')
        self.ch2_measurement_auto_var = tk.IntVar()
        self.ch2_measurement_auto_var.set(1)
        self.ch2_measurement_plot_var = tk.IntVar()
        self.ch2_measurement_plot_var.set(0)

        self.primary_source_var = tk.StringVar()
        self.primary_source_var.set(self.primary_source_options[0])

        self.speed_accuracy_var = tk.StringVar()
        self.speed_accuracy_var.set(self.speed_accuracy_options[0])

        self.xaxis_var = tk.StringVar()
        self.xaxis_var.set(self.axes_options[0])

        self.left_yaxis_var = tk.StringVar()
        self.left_yaxis_var.set(self.axes_options[0])

        self.right_yaxis_var = tk.StringVar()
        self.right_yaxis_var.set(self.axes_options[0])

        ch_settings_frame = tk.Frame(self.root, background = self.background)

        ch1_settings_frame = tk.LabelFrame(ch_settings_frame, text = self.primary_source_options[0] + ' Settings', background = self.background, padx = 5, pady = 5)

        ch1_function_row = tk.Frame(ch1_settings_frame, background = self.background)
        ch1_function_menu = tk.OptionMenu(ch1_function_row, self.ch1_function_var, *self.function_options)
        self.set_width(ch1_function_menu, self.function_options)
        ch1_function_menu.pack(side = tk.RIGHT)
        tk.Label(ch1_function_row, text = 'Function:', background = self.background).pack(side = tk.RIGHT)
        ch1_function_row.pack(side = tk.TOP, anchor = tk.W)

        ch1_source_frame = tk.LabelFrame(ch1_settings_frame, text = 'Source', background = self.background, padx = 5, pady = 5)

        ch1_source_name_row = tk.Frame(ch1_source_frame, background = self.background)
        tk.Entry(ch1_source_name_row, textvariable = self.ch1_source_name_var).pack(side = tk.RIGHT)
        tk.Label(ch1_source_name_row, text = 'Name:', background = self.background).pack(side = tk.RIGHT)
        ch1_source_name_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        ch1_source_values_row = tk.Frame(ch1_source_frame, background = self.background)
        tk.Entry(ch1_source_values_row, textvariable = self.ch1_source_values_var).pack(side = tk.RIGHT)
        tk.Label(ch1_source_values_row, text = 'Values:', background = self.background).pack(side = tk.RIGHT)
        ch1_source_values_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        ch1_source_frame.pack(side = tk.TOP, pady = 5)

        ch1_measurement_frame = tk.LabelFrame(ch1_settings_frame, text = 'Measurement', background = self.background, padx = 5, pady = 5)

        ch1_measurement_name_row = tk.Frame(ch1_measurement_frame, background = self.background)
        tk.Entry(ch1_measurement_name_row, textvariable = self.ch1_measurement_name_var).pack(side = tk.RIGHT)
        tk.Label(ch1_measurement_name_row, text = 'Name:', background = self.background).pack(side = tk.RIGHT)
        ch1_measurement_name_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        ch1_measurement_settings_row = tk.Frame(ch1_measurement_frame, background = self.background)
        tk.Checkbutton(ch1_measurement_settings_row, text = 'Autorange', variable = self.ch1_measurement_auto_var, background = self.background).pack(side = tk.LEFT)
        tk.Checkbutton(ch1_measurement_settings_row, text = 'Plot', variable = self.ch1_measurement_plot_var, background = self.background).pack(side = tk.LEFT, padx = 5)
        ch1_measurement_settings_row.pack(side = tk.TOP, pady = 2)

        ch1_measurement_frame.pack(side = tk.TOP, fill = tk.X)

        ch1_settings_frame.pack(side = tk.TOP, padx = 5, pady = 5)

        ch2_settings_frame = tk.LabelFrame(ch_settings_frame, text = self.primary_source_options[1] + ' Settings', background = self.background, padx = 5, pady = 5)

        ch2_function_row = tk.Frame(ch2_settings_frame, background = self.background)
        ch2_function_menu = tk.OptionMenu(ch2_function_row, self.ch2_function_var, *self.function_options)
        self.set_width(ch2_function_menu, self.function_options)
        ch2_function_menu.pack(side = tk.RIGHT)
        tk.Label(ch2_function_row, text = 'Function:', background = self.background).pack(side = tk.RIGHT)
        ch2_function_row.pack(side = tk.TOP, anchor = tk.W)

        ch2_source_frame = tk.LabelFrame(ch2_settings_frame, text = 'Source', background = self.background, padx = 5, pady = 5)

        ch2_source_name_row = tk.Frame(ch2_source_frame, background = self.background)
        tk.Entry(ch2_source_name_row, textvariable = self.ch2_source_name_var).pack(side = tk.RIGHT)
        tk.Label(ch2_source_name_row, text = 'Name:', background = self.background).pack(side = tk.RIGHT)
        ch2_source_name_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        ch2_source_values_row = tk.Frame(ch2_source_frame, background = self.background)
        tk.Entry(ch2_source_values_row, textvariable = self.ch2_source_values_var).pack(side = tk.RIGHT)
        tk.Label(ch2_source_values_row, text = 'Values:', background = self.background).pack(side = tk.RIGHT)
        ch2_source_values_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        ch2_source_frame.pack(side = tk.TOP, pady = 5)

        ch2_measurement_frame = tk.LabelFrame(ch2_settings_frame, text = 'Measurement', background = self.background, padx = 5, pady = 5)

        ch2_measurement_name_row = tk.Frame(ch2_measurement_frame, background = self.background)
        tk.Entry(ch2_measurement_name_row, textvariable = self.ch2_measurement_name_var).pack(side = tk.RIGHT)
        tk.Label(ch2_measurement_name_row, text = 'Name:', background = self.background).pack(side = tk.RIGHT)
        ch2_measurement_name_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        ch2_measurement_settings_row = tk.Frame(ch2_measurement_frame, background = self.background)
        tk.Checkbutton(ch2_measurement_settings_row, text = 'Autorange', variable = self.ch2_measurement_auto_var, background = self.background).pack(side = tk.LEFT)
        tk.Checkbutton(ch2_measurement_settings_row, text = 'Plot', variable = self.ch2_measurement_plot_var, background = self.background).pack(side = tk.LEFT, padx = 5)
        ch2_measurement_settings_row.pack(side = tk.TOP, pady = 2)

        ch2_measurement_frame.pack(side = tk.TOP, fill = tk.X)

        ch2_settings_frame.pack(side = tk.TOP, padx = 5, pady = 5)

        ch_settings_frame.pack(side = tk.LEFT, anchor = tk.S)

        plot_frame = tk.Frame(self.root, background = self.background)

        settings_row = tk.Frame(plot_frame, background = self.background)

        measurement_settings_frame = tk.LabelFrame(settings_row, text = 'Measurement Settings', background = self.background, padx = 5, pady = 5)

        primary_source_row = tk.Frame(measurement_settings_frame, background = self.background)
        primary_source_menu = tk.OptionMenu(primary_source_row, self.primary_source_var, *self.primary_source_options)
        self.set_width(primary_source_menu, self.speed_accuracy_options)
        primary_source_menu.pack(side = tk.RIGHT)
        tk.Label(primary_source_row, text = 'Primary Source:', background = self.background).pack(side = tk.RIGHT)
        primary_source_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        speed_accuracy_row = tk.Frame(measurement_settings_frame, background = self.background)
        speed_accuracy_menu = tk.OptionMenu(speed_accuracy_row, self.speed_accuracy_var, *self.speed_accuracy_options)
        self.set_width(speed_accuracy_menu, self.speed_accuracy_options)
        speed_accuracy_menu.pack(side = tk.RIGHT)
        tk.Label(speed_accuracy_row, text = 'Speed/Accuracy:', background = self.background).pack(side = tk.RIGHT)
        speed_accuracy_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        measurement_settings_frame.pack(side = tk.LEFT, fill = tk.Y, padx = 5, pady = 5)

        axes_settings_frame = tk.LabelFrame(settings_row, text = 'Axes Settings', background = self.background, padx = 5, pady = 5)

        xaxis_row = tk.Frame(axes_settings_frame, background = self.background)
        xaxis_menu = tk.OptionMenu(xaxis_row, self.xaxis_var, *self.axes_options)
        self.set_width(xaxis_menu, self.axes_options)
        xaxis_menu.pack(side = tk.RIGHT)
        tk.Label(xaxis_row, text = 'X-Axis:', background = self.background).pack(side = tk.RIGHT)
        xaxis_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        left_yaxis_row = tk.Frame(axes_settings_frame, background = self.background)
        left_yaxis_menu = tk.OptionMenu(left_yaxis_row, self.left_yaxis_var, *self.axes_options)
        self.set_width(left_yaxis_menu, self.axes_options)
        left_yaxis_menu.pack(side = tk.RIGHT)
        tk.Label(left_yaxis_row, text = 'Left Y-Axis:', background = self.background).pack(side = tk.RIGHT)
        left_yaxis_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        right_yaxis_row = tk.Frame(axes_settings_frame, background = self.background)
        right_yaxis_menu = tk.OptionMenu(right_yaxis_row, self.right_yaxis_var, *self.axes_options)
        self.set_width(right_yaxis_menu, self.axes_options)
        right_yaxis_menu.pack(side = tk.RIGHT)
        tk.Label(right_yaxis_row, text = 'Right Y-Axis:', background = self.background).pack(side = tk.RIGHT)
        right_yaxis_row.pack(side = tk.TOP, anchor = tk.E, pady = 2)

        axes_settings_frame.pack(side = tk.LEFT, padx = 5, pady = 5)

        self.run_stop_button = tk.Button(settings_row, text = 'Start', command = self.sweep_start)
        self.run_stop_button.pack(side = tk.LEFT, anchor = tk.E, padx = 40)

        settings_row.pack(side = tk.BOTTOM, anchor = tk.W)

        plot_row = tk.Frame(plot_frame, background = self.background)
        plot_row.pack(side = tk.BOTTOM, anchor = tk.W, fill = tk.BOTH, expand = tk.TRUE)

        plot_frame.pack(side = tk.LEFT, anchor = tk.S, fill = tk.BOTH, expand = tk.TRUE)

        self.root.update()

        plot_width = float(settings_row.winfo_width())
        plot_height = float(ch_settings_frame.winfo_height() - settings_row.winfo_height())
        self.plot = tkplot.tkplot(parent = plot_row, width = plot_width, height = plot_height)
        self.plot.yaxes['right'] = self.plot.y_axis(name = 'right', color = '#FF0000')
        self.plot.right_yaxis = 'right'

    def shut_down(self):
        if self.state_handler is not None:
            self.root.after_cancel(self.state_handler)
        self.root.destroy()

    def set_width(self, option_menu, options):
        font = tkFont.nametofont(option_menu.cget('font'))
        zero_width = font.measure('0')
        max_width = max([font.measure(option) for option in options]) / zero_width
        option_menu.config(width = max_width)

    def is_var_name(self, s):
        return (not keyword.iskeyword(s)) and (re.match('^[^\d\W]\w*\Z', s) is not None)

    def sweep_start(self):
        ch1_src_name = str(self.ch1_source_name_var.get()).strip()
        ch1_src_vals = str(self.ch1_source_values_var.get()).strip()
        ch1_meas_name = str(self.ch1_measurement_name_var.get()).strip()

        ch2_src_name = str(self.ch2_source_name_var.get()).strip()
        ch2_src_vals = str(self.ch2_source_values_var.get()).strip()
        ch2_meas_name = str(self.ch2_measurement_name_var.get()).strip()

        if (ch1_src_name == '') or (ch1_src_vals == '') or (ch2_src_name == '') or (ch2_src_vals == ''):
            tkMessageBox.showerror(message = 'You must specify source names and values both for CH1 and for CH2.')
            return

        if (ch1_meas_name == '') and (ch2_meas_name == ''):
            tkMessageBox.showerror(message = 'You must specify measurement names either for CH1 or for CH2.')
            return

        if not self.is_var_name(ch1_src_name):
            tkMessageBox.showerror(message = 'CH1 source name specified is not a legitimate variable name.')
            return

        if (ch1_meas_name != '') and not self.is_var_name(ch1_meas_name):
            tkMessageBox.showerror(message = 'CH1 measurement name specified is not a legitimate variable name.')
            return

        if not self.is_var_name(ch2_src_name):
            tkMessageBox.showerror(message = 'CH2 source name specified is not a legitimate variable name.')
            return

        if (ch2_meas_name != '') and not self.is_var_name(ch2_meas_name):
            tkMessageBox.showerror(message = 'CH2 measurement name specified is not a legitimate variable name.')
            return

        try:
            if __name__ == '__main__':
                result = eval(ch1_src_vals)
            else:
                result = eval(ch1_src_vals, __main__.__dict__)
        except:
            tkMessageBox.showerror(message = 'Error evaluating specified CH1 source-value expression.')
            return

        if (type(result) is int) or (type(result) is long) or (type(result) is float):
            result = array([float(result)])
        elif type(result) is tuple:
            t = result
            result = ndarray(0)
            for e in t:
                result = append(result, e)
        elif type(result) is ndarray:
            pass
        else:
            tkMessageBox.showerror(message = 'CH1 source-value expression must evaluate either to a number, an ndarray, or a tuple of numbers / ndarrays.')
            return

        self.ch1_src_vals = result
        self.ch1_src_name = ch1_src_name
        self.ch1_meas_name = ch1_meas_name
        self.ch1_fn = self.function_options.index(self.ch1_function_var.get())

        try:
            if __name__ == '__main__':
                result = eval(ch2_src_vals)
            else:
                result = eval(ch2_src_vals, __main__.__dict__)
        except:
            tkMessageBox.showerror(message = 'Error evaluating specified CH2 source-value expression.')

        if (type(result) is int) or (type(result) is long) or (type(result) is float):
            result = array([float(result)])
        elif type(result) is tuple:
            t = result
            result = ndarray(0)
            for e in t:
                result = append(result, e)
        elif type(result) is ndarray:
            pass
        else:
            tkMessageBox.showerror(message = 'CH2 source-value expression must evaluate either to a number, an ndarray, or a tuple of numbers / ndarrays.')
            return

        self.ch2_src_vals = result
        self.ch2_src_name = ch2_src_name
        self.ch2_meas_name = ch2_meas_name
        self.ch2_fn = self.function_options.index(self.ch2_function_var.get())

        self.speed_accuracy = self.speed_accuracy_options.index(self.speed_accuracy_var.get())

        self.run_stop_button.configure(text = 'Stop')
        self.run_stop_button.configure(command = self.sweep_stop)

        self.smu.set_function(1, self.ch1_fn)
        self.smu.set_function(2, self.ch2_fn)

        self.prim_ch = self.primary_source_options.index(self.primary_source_var.get()) + 1
        self.sec_ch = 3 - self.prim_ch

        if self.prim_ch == 1:
            self.prim_fn = self.ch1_fn
            self.prim_vals = self.ch1_src_vals
            self.sec_fn = self.ch2_fn
            self.sec_vals = self.ch2_src_vals
        else:
            self.prim_fn = self.ch2_fn
            self.prim_vals = self.ch2_src_vals
            self.sec_fn = self.ch1_fn
            self.sec_vals = self.ch1_src_vals

        self.smu.set_source(self.prim_ch, self.prim_vals[0], self.prim_fn)
        self.smu.set_source(self.sec_ch, self.sec_vals[0], self.sec_fn)

        if self.prim_ch == 1:
            self.x_label = self.ch1_src_name
        else:
            self.x_label = self.ch2_src_name

        if self.prim_fn == 0:
            self.x_label += ' (V)'
        else:
            self.x_label += ' (A)'

        self.y1_label = self.ch1_meas_name

        if self.ch1_fn == 0:
            self.y1_label += ' (A)'
        else:
            self.y1_label += ' (V)'

        self.y2_label = self.ch2_meas_name

        if self.ch2_fn == 0:
            self.y2_label += ' (A)'
        else:
            self.y2_label += ' (V)'

        self.ch1_meas = [zeros(len(self.prim_vals)) for i in range(len(self.sec_vals))]
        self.ch2_meas = [zeros(len(self.prim_vals)) for i in range(len(self.sec_vals))]

        self.prim_index = 0
        self.sec_index = 0

        self.state_handler = self.root.after(self.delay, self.sweep_autorange)

    def sweep_stop(self):
        self.run_stop_button.configure(text = 'Start')
        self.run_stop_button.configure(command = self.sweep_start)

        if self.state_handler is not None:
            self.root.after_cancel(self.state_handler)
            self.state_handler = None

    def sweep_autorange(self):
        if self.ch1_measurement_auto_var.get() == 1:
            self.smu.autorange(1)

        if self.ch2_measurement_auto_var.get() == 1:
            self.smu.autorange(2)

        if self.ch1_meas_name != '':
            self.buffer_index = 0
            self.buffer_length = self.buffer_lengths[self.smu.get_irange(1)][self.speed_accuracy]
            self.meas_buffer = [0] * self.buffer_length
            self.state_handler = self.root.after(self.delay, self.sweep_meas_ch1)
        else:
            self.buffer_index = 0
            self.buffer_length = self.buffer_lengths[self.smu.get_irange(2)][self.speed_accuracy]
            self.meas_buffer = [0] * self.buffer_length
            self.state_handler = self.root.after(self.delay, self.sweep_meas_ch2)

    def sweep_meas_ch1(self):
        self.meas_buffer[self.buffer_index] = self.smu.get_meas(1)[0]
        self.buffer_index += 1
        if self.buffer_index == self.buffer_length:
            self.ch1_meas[self.sec_index][self.prim_index] = sum(self.meas_buffer) / self.buffer_length
            if self.ch2_meas_name != '':
                self.buffer_index = 0
                self.buffer_length = self.buffer_lengths[self.smu.get_irange(2)][self.speed_accuracy]
                self.meas_buffer = [0] * self.buffer_length
                self.state_handler = self.root.after(self.delay, self.sweep_meas_ch2)
            else:
                self.state_handler = self.root.after(self.delay, self.sweep_plot)
        else:
            self.state_handler = self.root.after(self.delay, self.sweep_meas_ch1)

    def sweep_meas_ch2(self):
        self.meas_buffer[self.buffer_index] = self.smu.get_meas(2)[0]
        self.buffer_index += 1
        if self.buffer_index == self.buffer_length:
            self.ch2_meas[self.sec_index][self.prim_index] = sum(self.meas_buffer) / self.buffer_length
            self.state_handler = self.root.after(self.delay, self.sweep_plot)
        else:
            self.state_handler = self.root.after(self.delay, self.sweep_meas_ch2)

    def sweep_plot(self):
        if (self.ch1_meas_name != '') and (self.ch1_measurement_plot_var.get() == 1) and (self.ch2_meas_name != '') and (self.ch2_measurement_plot_var.get() == 1):
            self.plot.yaxes['left'].color = '#0000FF'
            self.plot.plot(self.prim_vals[:self.prim_index + 1], self.ch1_meas[self.sec_index][:self.prim_index + 1], 'b.b-')
            self.plot.plot(self.prim_vals[:self.prim_index + 1], self.ch2_meas[self.sec_index][:self.prim_index + 1], 'r.r-', yaxis = 'right', hold = 'on')
            self.plot.xaxis(self.xaxis_var.get())
            self.plot.yaxis(self.left_yaxis_var.get())
            self.plot.yaxis(self.right_yaxis_var.get(), yaxis = 'right')
            self.plot.xlabel(self.x_label)
            self.plot.ylabel(self.y1_label)
            self.plot.ylabel(self.y2_label, yaxis = 'right')
        elif (self.ch1_meas_name != '') and (self.ch1_measurement_plot_var.get() == 1):
            self.plot.yaxes['left'].color = '#000000'
            self.plot.plot(self.prim_vals[:self.prim_index + 1], self.ch1_meas[self.sec_index][:self.prim_index + 1], 'b.b-')
            self.plot.xaxis(self.xaxis_var.get())
            self.plot.yaxis(self.left_yaxis_var.get())
            self.plot.xlabel(self.x_label)
            self.plot.ylabel(self.y1_label)
            self.plot.ylabel('', yaxis = 'right')
        elif (self.ch2_meas_name != '') and (self.ch2_measurement_plot_var.get() == 1):
            self.plot.yaxes['left'].color = '#000000'
            self.plot.plot(self.prim_vals[:self.prim_index + 1], self.ch2_meas[self.sec_index][:self.prim_index + 1], 'b.b-')
            self.plot.xaxis(self.xaxis_var.get())
            self.plot.yaxis(self.left_yaxis_var.get())
            self.plot.xlabel(self.x_label)
            self.plot.ylabel(self.y2_label)
            self.plot.ylabel('', yaxis = 'right')
        self.plot.draw_now()

        self.state_handler = self.root.after(self.delay, self.sweep_advance)

    def sweep_advance(self):
        self.prim_index += 1
        if self.prim_index == len(self.prim_vals):
            self.prim_index = 0
            self.sec_index += 1
            if self.sec_index == len(self.sec_vals):
                self.state_handler = self.root.after(self.delay, self.sweep_finish)
                return

        self.smu.set_source(self.prim_ch, self.prim_vals[self.prim_index], self.prim_fn)
        self.smu.set_source(self.sec_ch, self.sec_vals[self.sec_index], self.sec_fn)

        self.state_handler = self.root.after(self.delay, self.sweep_autorange)

    def sweep_finish(self):
        self.smu.set_source(self.prim_ch, self.prim_vals[0], self.prim_fn)
        self.smu.set_source(self.sec_ch, self.sec_vals[0], self.sec_fn)

        if __name__ != '__main__':
            __main__.__dict__[self.ch1_src_name] = self.ch1_src_vals
            __main__.__dict__[self.ch2_src_name] = self.ch2_src_vals
            if self.ch1_meas_name != '':
                __main__.__dict__[self.ch1_meas_name] = self.ch1_meas
            if self.ch2_meas_name != '':
                __main__.__dict__[self.ch2_meas_name] = self.ch2_meas
        else:
            f_out = open(self.ch1_src_name + '.txt', 'w')
            for i in range(len(self.ch1_src_vals)):
                f_out.write('{!s}{}'.format(self.ch1_src_vals[i], '\t' if i < len(self.ch1_src_vals) - 1 else '\n'))
            f_out.close()

            f_out = open(self.ch2_src_name + '.txt', 'w')
            for i in range(len(self.ch2_src_vals)):
                f_out.write('{!s}{}'.format(self.ch2_src_vals[i], '\t' if i < len(self.ch2_src_vals) - 1 else '\n'))
            f_out.close()

            if self.ch1_meas_name != '':
                f_out = open(self.ch1_meas_name + '.txt', 'w')
                for i in range(len(self.sec_vals)):
                    for j in range(len(self.prim_vals)):
                        f_out.write('{!s}{}'.format(self.ch1_meas[i][j], '\t' if j < len(self.prim_vals) - 1 else '\n'))
                f_out.close()

            if self.ch2_meas_name != '':
                f_out = open(self.ch2_meas_name + '.txt', 'w')
                for i in range(len(self.sec_vals)):
                    for j in range(len(self.prim_vals)):
                        f_out.write('{!s}{}'.format(self.ch2_meas[i][j], '\t' if j < len(self.prim_vals) - 1 else '\n'))
                f_out.close()

        self.sweep_stop()

if __name__ == '__main__':
    gui = smutake()
    gui.root.mainloop()

