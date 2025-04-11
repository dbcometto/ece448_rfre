#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Fan Toggle
# Author: Ben Cometto
# Description: Turns on and off the fan in the classroom
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class fan_toggle(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Fan Toggle", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fan Toggle")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fan_toggle")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.waiting = waiting =  tuple(2 for x in range(1))
        self.samp_rate = samp_rate = 1000000
        self.device_code = device_code = (1,0,0,1)
        self.code_light = code_light = (0,0,0,0,0,1,1,1)
        self.code_fan = code_fan = (0,0,0,0,0,1,1,0)
        self.code_end = code_end = (0,1,1,1,1,1,1,1)
        self.code = code = 1
        self.bit_interval = bit_interval = 0.0063
        self.repeat_for_time = repeat_for_time = int(samp_rate/3*bit_interval)
        self.message = message = waiting if code == 0 else ( (1,) + device_code + (code_light if code == 1 else code_fan))
        self.long_waiting = long_waiting = 100*waiting
        self.f_data = f_data = 18000
        self.f_carrier = f_carrier = 350000000
        self.end_message = end_message = (1,) + device_code + code_end

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            (int(samp_rate*10)), #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            512, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.digital_map_bb_0 = digital.map_bb([3, 1,0])
        # Create the options list
        self._code_options = [0, 1, 2]
        # Create the labels list
        self._code_labels = ['None', 'Toggle Light', 'Toggle Fan']
        # Create the combo box
        self._code_tool_bar = Qt.QToolBar(self)
        self._code_tool_bar.addWidget(Qt.QLabel("Code Option" + ": "))
        self._code_combo_box = Qt.QComboBox()
        self._code_tool_bar.addWidget(self._code_combo_box)
        for _label in self._code_labels: self._code_combo_box.addItem(_label)
        self._code_callback = lambda i: Qt.QMetaObject.invokeMethod(self._code_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._code_options.index(i)))
        self._code_callback(self.code)
        self._code_combo_box.currentIndexChanged.connect(
            lambda i: self.set_code(self._code_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._code_tool_bar)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(3*(message + waiting) + end_message + long_waiting, True, 1, [])
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(3)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, repeat_for_time)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f_data, 1, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fan_toggle")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_waiting(self):
        return self.waiting

    def set_waiting(self, waiting):
        self.waiting = waiting
        self.set_long_waiting(100*self.waiting)
        self.set_message(self.waiting if self.code == 0 else ( (1,) + self.device_code + (self.code_light if self.code == 1 else self.code_fan)) )
        self.blocks_vector_source_x_0.set_data(3*(self.message + self.waiting) + self.end_message + self.long_waiting, [])

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_repeat_for_time(int(self.samp_rate/3*self.bit_interval))
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_device_code(self):
        return self.device_code

    def set_device_code(self, device_code):
        self.device_code = device_code
        self.set_end_message((1,) + self.device_code + self.code_end)
        self.set_message(self.waiting if self.code == 0 else ( (1,) + self.device_code + (self.code_light if self.code == 1 else self.code_fan)) )

    def get_code_light(self):
        return self.code_light

    def set_code_light(self, code_light):
        self.code_light = code_light
        self.set_message(self.waiting if self.code == 0 else ( (1,) + self.device_code + (self.code_light if self.code == 1 else self.code_fan)) )

    def get_code_fan(self):
        return self.code_fan

    def set_code_fan(self, code_fan):
        self.code_fan = code_fan
        self.set_message(self.waiting if self.code == 0 else ( (1,) + self.device_code + (self.code_light if self.code == 1 else self.code_fan)) )

    def get_code_end(self):
        return self.code_end

    def set_code_end(self, code_end):
        self.code_end = code_end
        self.set_end_message((1,) + self.device_code + self.code_end)

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code
        self._code_callback(self.code)
        self.set_message(self.waiting if self.code == 0 else ( (1,) + self.device_code + (self.code_light if self.code == 1 else self.code_fan)) )

    def get_bit_interval(self):
        return self.bit_interval

    def set_bit_interval(self, bit_interval):
        self.bit_interval = bit_interval
        self.set_repeat_for_time(int(self.samp_rate/3*self.bit_interval))

    def get_repeat_for_time(self):
        return self.repeat_for_time

    def set_repeat_for_time(self, repeat_for_time):
        self.repeat_for_time = repeat_for_time
        self.blocks_repeat_0.set_interpolation(self.repeat_for_time)

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
        self.blocks_vector_source_x_0.set_data(3*(self.message + self.waiting) + self.end_message + self.long_waiting, [])

    def get_long_waiting(self):
        return self.long_waiting

    def set_long_waiting(self, long_waiting):
        self.long_waiting = long_waiting
        self.blocks_vector_source_x_0.set_data(3*(self.message + self.waiting) + self.end_message + self.long_waiting, [])

    def get_f_data(self):
        return self.f_data

    def set_f_data(self, f_data):
        self.f_data = f_data
        self.analog_sig_source_x_1.set_frequency(self.f_data)

    def get_f_carrier(self):
        return self.f_carrier

    def set_f_carrier(self, f_carrier):
        self.f_carrier = f_carrier

    def get_end_message(self):
        return self.end_message

    def set_end_message(self, end_message):
        self.end_message = end_message
        self.blocks_vector_source_x_0.set_data(3*(self.message + self.waiting) + self.end_message + self.long_waiting, [])




def main(top_block_cls=fan_toggle, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
