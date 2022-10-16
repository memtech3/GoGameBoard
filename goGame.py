from textual import events
from textual.app import App
from textual.widgets import Header, Footer, Placeholder, ScrollView

import customWidgets

from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text


from textual.reactive import Reactive
from textual.widget import Widget

from textual_inputs.text_input import TextInput

col1 = [".", ".", ".", ".", ".", ".", "." ,"." ,"."]
col2 = [".", ".", ".", ".", ".", ".", "." ,"." ,"."]
col3 = [".", ".", ".", ".", ".", ".", "." ,"." ,"."]
col4 = [".", ".", ".", ".", ".", ".", "." ,"." ,"."]
col5 = [".", ".", ".", ".", ".", ".", "." ,"." ,"."]
col6 = [".", ".", ".", ".", ".", ".", "." ,"." ,"."]
col7 = [".", ".", ".", ".", ".", ".", "." ,"." ,"."]
col8 = [".", ".", ".", ".", ".", ".", "." ,"." ,"."]
col9 = [".", ".", ".", ".", ".", ".", "." ,"." ,"."]
rows = [col1, col2, col3, col4, col5, col6, col7 ,col8, col9]

currentCol = 0
currentRow = 0
previousCol = 0
previousRow = 0

blackTurn = True

# increments the col by an increment number, checks to make sure increment is valid
def incCol(increment:int):
    global currentCol
    if increment > 0:
        if  currentCol < 8:
            currentCol += increment
    elif increment < 0:
         if currentCol > 0:
            currentCol += increment

# increments the row by an increment number, checks to make sure increment is valid
def incRow(increment:int):
    global currentRow
    if increment > 0:
        if  currentRow < 8:
            currentRow += increment
    elif increment < 0:
         if currentRow > 0:
            currentRow += increment

# widget that creates the go board
class goBoard(Widget):
    def on_mount(self):
        self.set_interval(.001, self.refresh)
    def render(self):
        grid = Table.grid(expand=True)

        # creates top label row
        def label(number: int):
            return Panel(str(number))
        grid.add_row(label(0), label(1), label(2), label(3), label(4), label(5), label(6), label(7), label(8), label(9))
        
        # creates a Panel with the value of column[index]
        def cell(column:list, index:int):
            return Panel(str(column[index]))

        # renders empty grid, with side labels
        i = 1
        for col in rows:
            var = None
            grid.add_row(Panel(str(i)), cell(col, 0), cell(col, 1), cell(col, 2), cell(col, 3), cell(col, 4), cell(col, 5), cell(col, 6), cell(col, 7), cell(col, 8))
            i +=1
        result = Panel(grid)
        result.title = "9x9 Board"
        return result

errorMessage:str = ""
class sidePanel(Widget):
    def on_mount(self):
        self.set_interval(.01, self.refresh)
    def render(self):
        global errorMessage, blackTurn
        player = Panel("Black" if blackTurn else "White")
        player.title = "Player"
        instructions = Panel("Resize your terminal window to ensure you can see all 9 columns and rows of the board before continuing. \n\nPress H (lowercase) to toggle instructions panel. \nPress Q (lowercase) or ESCAPE to quit. \nUse WASD (lowercase) to navigate. \nPress 1 to place piece")
        instructions.title = "Instructions"
        errors = Panel(errorMessage)
        errors.title = "Errors"
        errors.style = "red"
        layout = Layout()
        layout.split_column(
            player,
            instructions,
            errors
        )
        return layout

class MyApp(App):
    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("h", "view.toggle('sidePanel')", "Toggle instructions")
        await self.bind("q", "quit", "Quit")
        await self.bind("escape", "quit", "Quit")
        await self.bind("w", "", "Up")
        await self.bind("a", "", "Left")
        await self.bind("s", "", "Down")
        await self.bind("d", "", "Right")
        await self.bind("1", "", "Place Piece")
        await self.bind("C", "", "Clear Errors")

    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""
        # Header / footer / dock
        await self.view.dock(customWidgets.Header(), name="header", edge="top")
        await self.view.dock(customWidgets.Footer(), edge="bottom")
        await self.view.dock(sidePanel(), edge="left", size=50, name="sidePanel")
        # Dock the body in the remaining space
        await self.view.dock(goBoard(), edge="right")

        # set first cell to "active" state
        rows[currentRow][currentCol] = "*" + str(rows[currentRow][currentCol]) + "*"

    async def on_key(self, event):
        # use variables declared outside of function
        global previousRow, previousCol, currentRow, currentCol, blackTurn, errorMessage
        
        # remove select icon from previously selected cell
        previousRow = currentRow
        previousCol = currentCol
        rows[previousRow][previousCol] = str(rows[previousRow][previousCol]).replace("*", "")

        # selects row
        if event.key == "w":
                incRow(-1)
        elif event.key == "a":
                incCol(-1)
        elif event.key == "s":
                incRow(1)
        elif event.key == "d":
                incCol(1)
        # add select icon to current cell
        rows[currentRow][currentCol] = "*" + str(rows[currentRow][currentCol]) + "*"

        # place piece
        if event.key == "1":
            if rows[currentRow][currentCol] == "*.*":
                if blackTurn:
                    rows[currentRow][currentCol] = "*" + "●" + "*"
                else:
                    rows[currentRow][currentCol] = "*" + "○" + "*"
                blackTurn = not blackTurn
            else:
                errorMessage = errorMessage + "Pieces may only be placed in empty cells\n"
        
        # clear error messages
        if event.key == "c":
            errorMessage = ""

MyApp.run(title="Module 7 Team Lab Go Game - Micah Guttman", log="textual.log")