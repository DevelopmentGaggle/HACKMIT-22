StyleSheet = '''
QPushButton {
    border-radius: 5px;
    color: #ffffff;
    font-weight: bold;
}
QFrame {
    background-color: #EEEEEE;
    border: 1px;
    border-radius: 10px;
}

QAbstractScrollArea {
    border: 10px solid white;
    border-radius: 10px;
}

QAbstractScrollArea#textBrowser {
    border: 0px solid white;
}

QWidget#scrollAreaWidgetContents {
    background-color: #ffffff;
    border: 1px solid white;
}
QPushButton#stopButton {
    background-color: #f44336;
}
#stopButton:hover {
    background-color: #e57373;
}
#stopButton:pressed { 
    background-color: #ffcdd2;
}
#runButton {
    background-color: #4caf50;
}
#runButton:hover {
    background-color: #81c784;            
}
#runButton:pressed {
    background-color: #c8e6c9;
}

'''