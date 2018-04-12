# Copyright (C) 2012 Cristhofer Travieso <cristhofert97@gmail.com>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gi.repository import Gtk
from gi.repository import Pango
from gi.repository import Gdk

import locale
import convert

from sugar3.activity import activity
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.radiotoolbutton import RadioToolButton

from gettext import gettext as _

SCREEN_WIDTH = Gdk.Screen.width()
ENTER_KEY = 65293


class ConvertActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle, True)

        self.max_participants = 1
        self.dic = {}

        # Canvas
        self._canvas = Gtk.VBox()

        hbox = Gtk.HBox()
        self._liststore1 = Gtk.ListStore(str)
        self.combo1 = Gtk.ComboBox.new_with_model_and_entry(self._liststore1)
        cell = Gtk.CellRendererText()
        self.combo1.pack_start(cell, True)
        self.combo1.add_attribute(cell, 'markup', 0)
        self.combo1.set_entry_text_column(0)
        self.combo1.connect('changed', self._call)

        flip_btn = Gtk.Button()
        flip_btn.connect('clicked', self._flip)
        flip_btn.add(Gtk.Image.new_from_file('icons/flip.svg'))

        self._liststore2 = Gtk.ListStore(str)
        self.combo2 = Gtk.ComboBox.new_with_model_and_entry(self._liststore2)
        cell = Gtk.CellRendererText()
        self.combo2.pack_start(cell, True)
        self.combo2.add_attribute(cell, 'markup', 0)
        self.combo2.set_entry_text_column(0)
        self.combo2.connect('changed', self._call)

        self.label_box = Gtk.HBox()

        self.adjustment = Gtk.Adjustment(1.0, 0, 10.00 ** 10.00 , 1.0, 1.0, 0)  
        self.spin = Gtk.SpinButton() 
        self.spin.set_adjustment(self.adjustment)

        self.label = Gtk.Label()
        self.label.set_selectable(True)
        self.label._size = 12
        self.label.connect('draw', self.resize_label)

        self.convert_btn = Gtk.Button(_('Convert'))
        self.convert_btn.connect('clicked', self._call)

        self._canvas.pack_start(hbox, False, False, 20)
        hbox.pack_start(self.combo1, False, True, 20)
        hbox.pack_start(flip_btn, True, False, 20)
        hbox.pack_end(self.combo2, False, True, 20)
        spin_box = Gtk.HBox()
        convert_box = Gtk.HBox()
        convert_box.pack_start(spin_box, True, False, 0)
        spin_box.pack_start(self.spin, False, False, 0)
        self._canvas.pack_start(convert_box, False, False, 5)
        self._canvas.pack_start(self.label_box, True, False, 0)
        self.label_box.add(self.label)
        spin_box.pack_start(self.convert_btn, False, False, 20)

        self.set_canvas(self._canvas)

        # Toolbar
        toolbarbox = ToolbarBox()

        activity_button = ActivityToolbarButton(self)

        toolbarbox.toolbar.insert(activity_button, 0)

        separator = Gtk.SeparatorToolItem()
        separator.set_expand(False)
        separator.set_draw(True)
        toolbarbox.toolbar.insert(separator, -1)

        # RadioToolButton
        self._length_btn = RadioToolButton()
        self._length_btn.connect('clicked',
                                 lambda w: self._update_combo(convert.length))
        # TRANS: https://en.wikipedia.org/wiki/Length
        self._length_btn.set_tooltip(_('Length'))
        self._length_btn.props.icon_name = 'length'

        self._volume_btn = RadioToolButton()
        self._volume_btn.connect('clicked',
                                 lambda w: self._update_combo(convert.volume))
        # TRANS: https://en.wikipedia.org/wiki/Volume
        self._volume_btn.set_tooltip(_('Volume'))
        self._volume_btn.props.icon_name = 'volume'
        self._volume_btn.props.group = self._length_btn

        self._area_btn = RadioToolButton()
        self._area_btn.connect('clicked',
                               lambda w: self._update_combo(convert.area))
        # TRANS: https://en.wikipedia.org/wiki/Area
        self._area_btn.set_tooltip(_('Area'))
        self._area_btn.props.icon_name = 'area'
        self._area_btn.props.group = self._length_btn

        self._weight_btn = RadioToolButton()
        self._weight_btn.connect('clicked',
                                 lambda w: self._update_combo(convert.weight))
        # TRANS: https://en.wikipedia.org/wiki/Weight
        self._weight_btn.set_tooltip(_('Weight'))
        self._weight_btn.props.icon_name = 'weight'
        self._weight_btn.props.group = self._length_btn

        self._speed_btn = RadioToolButton()
        self._speed_btn.connect('clicked',
                                lambda w: self._update_combo(convert.speed))
        # TRANS: https://en.wikipedia.org/wiki/Speed
        self._speed_btn.set_tooltip(_('Speed'))
        self._speed_btn.props.icon_name = 'speed'
        self._speed_btn.props.group = self._length_btn

        self._time_btn = RadioToolButton()
        self._time_btn.connect('clicked',
                               lambda w: self._update_combo(convert.time))
        # TRANS: https://en.wikipedia.org/wiki/Time
        self._time_btn.set_tooltip(_('Time'))
        self._time_btn.props.icon_name = 'time'
        self._time_btn.props.group = self._length_btn

        self._temp_btn = RadioToolButton()
        self._temp_btn.connect('clicked',
                               lambda w: self._update_combo(convert.temp))
        # TRANS: https://en.wikipedia.org/wiki/Temperature
        self._temp_btn.set_tooltip(_('Temperature'))
        self._temp_btn.props.icon_name = 'temp'
        self._temp_btn.props.group = self._length_btn

        toolbarbox.toolbar.insert(self._length_btn, -1)
        toolbarbox.toolbar.insert(self._volume_btn, -1)
        toolbarbox.toolbar.insert(self._area_btn, -1)
        toolbarbox.toolbar.insert(self._weight_btn, -1)
        toolbarbox.toolbar.insert(self._speed_btn, -1)
        toolbarbox.toolbar.insert(self._time_btn, -1)
        toolbarbox.toolbar.insert(self._temp_btn, -1)

        separator = Gtk.SeparatorToolItem()
        separator.set_expand(True)
        separator.set_draw(False)
        toolbarbox.toolbar.insert(separator, -1)

        stopbtn = StopButton(self)
        toolbarbox.toolbar.insert(stopbtn, -1)

        self.set_toolbar_box(toolbarbox)
        self._update_combo(convert.length)
        self.show_all()

    def _update_label(self):
        try:
            spin_value = str(self.spin.get_value())
            decimals = str(len(spin_value.split('.')[-1]))
            fmt = '%.' + decimals + 'f'
            new_value = locale.format(fmt, float(spin_value))

            convert_value = str(self.convert())
            decimals = str(len(convert_value.split('.')[-1]))
            fmt = '%.' + decimals + 'f'
            new_convert = locale.format(fmt, float(convert_value))

            text = '%s ~ %s' % (new_value, new_convert)
            self.label.set_text(text)
        except KeyError:
            pass

    def _call(self, widget=None):
        self._update_label()
        self.show_all()

    def _update_combo(self, data):
        self._liststore1.clear()
        self._liststore2.clear()
        self.dic = data
        keys = self.dic.keys()
        keys.sort()
        for x in keys:
            symbol = ''
            if len(self.dic[x]) == 3:
                symbol = self.dic[x][-1]
                symbol = '<sup><b>%s</b></sup>' % symbol

            self._liststore1.append(['%s%s' % (x, symbol)])
            self._liststore2.append(['%s%s' % (x, symbol)])
        self.combo1.set_active(0)
        self.combo2.set_active(0)
        self._call()
        self.show_all()

    def _get_active_text(self, combobox):
        active = combobox.get_active()
        keys = self.dic.keys()
        keys.sort()
        if active < 0:
            return None
        text = keys[active]
        if '<sup>' in text:
            text = text.split('<b>')[1].split('</b>')[0]
        return text

    def _flip(self, widget):
        active_combo1 = self.combo1.get_active()
        active_combo2 = self.combo2.get_active()
        self.combo1.set_active(active_combo2)
        self.combo2.set_active(active_combo1)
        value = float(self.label.get_text().split(' ~ ')[1].replace(',', '.'))
        self.spin.set_value(value)
        self._call()

    def resize_label(self, widget, event):
        num_label = len(self.label.get_text())
        try:
            size = str((60 * SCREEN_WIDTH / 100) / num_label)
            if not size == self.label._size:
                self.label.modify_font(Pango.FontDescription(size))
                self.label._size = size
        except ZeroDivisionError:
            pass

    def convert(self):
        number = float(self.spin.get_text().replace(',', '.'))
        unit = self._get_active_text(self.combo1)
        to_unit = self._get_active_text(self.combo2)
        return convert.convert(number, unit, to_unit, self.dic)
