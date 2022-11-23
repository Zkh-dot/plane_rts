#!/usr/bin/env python3

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import sqlite3


class ContactModel(object):
    def __init__(self):
        # Create a database in RAM.
        self._db = sqlite3.connect(':memory:')
        self._db.row_factory = sqlite3.Row

        # Create the basic Plane table.
        self._db.cursor().execute('''
            CREATE TABLE Planes(
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                address TEXT,
                email TEXT,
                notes TEXT)
        ''')
        self._db.commit()

        # Current Plane when editing.
        self.current_id = None

    def add(self, Plane):
        self._db.cursor().execute('''
            INSERT INTO Planes(name, phone, address, email, notes)
            VALUES(:name, :phone, :address, :email, :notes)''',
                                  Plane)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT name, id from Planes").fetchall()

    def get_contact(self, contact_id):
        return self._db.cursor().execute(
            "SELECT * from Planes WHERE id=:id", {"id": contact_id}).fetchone()

    def get_current_contact(self):
        if self.current_id is None:
            return {"name": "", "address": "", "phone": "", "email": "", "notes": ""}
        else:
            return self.get_contact(self.current_id)

    def update_current_contact(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute('''
                UPDATE Planes SET name=:name, phone=:phone, address=:address,
                email=:email, notes=:notes WHERE id=:id''',
                                      details)
            self._db.commit()

    def delete_contact(self, contact_id):
        self._db.cursor().execute('''
            DELETE FROM Planes WHERE id=:id''', {"id": contact_id})
        self._db.commit()



class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Plane List")
        # Save off the model that accesses the Planes database.
        self._model = model

        # Create the form for displaying the list of Planes.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="Planes",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit)
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        layout2.add_widget(Button("Start", self._start), 4)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Plane")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["Planes"]
        raise NextScene("Edit Plane")

    def _delete(self):
        self.save()
        self._model.delete_contact(self.data["Planes"])
        self._reload_list()

    def _start(self):
        raise NextScene("Going Game")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class ContactView(Frame):
    def __init__(self, screen, model):
        super(ContactView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Plane Details",
                                          reduce_cpu=True)
        # Save off the model that accesses the Planes database.
        self._model = model

        # Create the form for displaying the list of Planes.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Name:", "name"))
        layout.add_widget(Text("Location (3 nums):", "address"))
        layout.add_widget(Text("Max speed:", "phone"))
        layout.add_widget(Text("Max acceleration:", "email"))
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Something:", "notes", as_string=True, line_wrap=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()
        
    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ContactView, self).reset()
        self.data = self._model.get_current_contact()

    def _ok(self):
        self.save()
        self._model.update_current_contact(self.data)
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


class GoingGame(Frame):
    def __init__(self, screen, model):
        super(GoingGame, self).__init__(screen,
                                          screen.height * 4 // 5,
                                          screen.width * 4 // 5,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Going game",
                                          reduce_cpu=True)



def demo(screen, scene):
    scenes = [
        Scene([ListView(screen, Planes)], -1, name="Main"),
        Scene([ContactView(screen, Planes)], -1, name="Edit Plane"),
        Scene([GoingGame(screen, Planes)], -1, name="Going Game")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


Planes = ContactModel()
last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene