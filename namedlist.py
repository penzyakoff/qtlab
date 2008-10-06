# namedlist.py, base class to implement named lists
# Reinier Heeres <reinier@heeres.eu>, 2008
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
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

import gobject
import logging

class NamedList(gobject.GObject):

    __gsignals__ = {
        'item-added': (gobject.SIGNAL_RUN_FIRST,
                    gobject.TYPE_NONE,
                    ([gobject.TYPE_PYOBJECT])),
        'item-changed': (gobject.SIGNAL_RUN_FIRST,
                    gobject.TYPE_NONE,
                    ([gobject.TYPE_PYOBJECT])),
        'item-removed': (gobject.SIGNAL_RUN_FIRST,
                    gobject.TYPE_NONE,
                    ([gobject.TYPE_PYOBJECT])),
    }

    def __init__(self, base_name='item', **kwargs):
        gobject.GObject.__init__(self)

        self._list = {}
        self._auto_counter = 0
        self._base_name = base_name

    def __repr__(self):
        s = "NamedList with %s" % str(self.get_items())
        return s

    def __getitem__(self, name):
        return self.get(name)

    def new_item_name(self, item, name):
        '''Generate a new item name.'''

        if name != '':
            return name

        self._auto_counter += 1
        name = self._base_name + str(self._auto_counter)
        return name

    def get(self, name=''):
        '''Get an item from the list; create a new one if it doesn't exist.'''

        if name in self._list:
            return self._list[name]

        item = self.create(name)
        name = self.new_item_name(item, name)
        self.add(name, item)
        return item

    def add(self, name, item):
        '''Add an item to the list.'''
        self._list[name] = item
        self.emit('item-added', name)

    def remove(self, name):
        '''Remove an item from the list.'''
        if name in self._list:
            self._list.__del__(name)
        self.emit('item-removed', name)

    def create(self, name, **kwargs):
        '''Override this function to create a new instance for the list'''
        return None

    def get_items(self):
        '''Return a list of available items.'''
        keys = self._list.keys()
        keys.sort()
        return keys
