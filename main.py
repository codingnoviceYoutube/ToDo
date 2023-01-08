import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class TodoList(App):
    def build(self):
        # Create a layout
        layout = BoxLayout(orientation='vertical')

        # Create an input box and a button to add items to the list
        self.input_box = TextInput(text='', size_hint_y=None, height=60)
        add_button = Button(text='Add', size_hint_y=None, height=30)
        add_button.bind(on_release=self.add_item)
        done_button = Button(text='Show Done Items', size_hint_y=None, height=30)
        done_button.bind(on_release=self.show_done_items)
        layout.add_widget(done_button)

        # Create a container for the todo list items
        self.item_container = BoxLayout(orientation='vertical')

        # Add the input box and button to the layout
        layout.add_widget(self.input_box)
        layout.add_widget(add_button)
        layout.add_widget(self.item_container)

        return layout

    def add_item(self, instance):
        # Get the text from the input box
        text = self.input_box.text

        # Clear the input box
        self.input_box.text = ''

        # Create a horizontal layout for the item and done button
        item_layout = BoxLayout(orientation='horizontal')

        # Add the text of the item to the layout
        label = Button(text=text, size_hint_y=None, height=30)
        item_layout.add_widget(label)

        # Add the done button to the layout
        done_button = Button(text='Done', size_hint_y=None, height=30)
        done_button.bind(on_release=self.mark_done)
        done_button.item_text = text  # store the text of the item in the done button
        item_layout.add_widget(done_button)

        # Add the item layout to the item container
        self.item_container.add_widget(item_layout)

    def mark_done(self, instance):
        # Get the text of the item from the done button
        item_text = instance.item_text

        # Remove the item layout from the item container
        item_layout = instance.parent
        self.item_container.remove_widget(item_layout)

        # Add the text of the item to the done.txt file
        with open('done.txt', 'a') as f:
            f.write(item_text + '\n')

    def show_done_items(self, instance):
        # Read the items from the done.txt file
        with open('done.txt', 'r') as f:
            items = f.readlines()

        # Create a grid layout with the items
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for item in items:
            label = Label(text=item, size_hint_y=None, height=30)
            grid.add_widget(label)
        grid.minimum_height = len(items) * 30

        # Create a scroll view for the grid layout
        scroll_view = ScrollView(size_hint=(1, 1), size=(400, 400))
        scroll_view.add_widget(grid)

        # Create the popup window
        popup = Popup(title='Done Items', content=scroll_view, size_hint=(None, None), size=(400, 400))

        # Open the popup window
        popup.open()


if __name__ == '__main__':
    TodoList().run()
