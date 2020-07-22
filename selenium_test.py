import pytest
import os
import app
import trello_items as trello
from threading import Thread
from selenium import webdriver

@pytest.fixture(scope='module')
def test_app():
    board_id = trello.create_board()
    os.environ['TRELLO_BOARD_ID'] = board_id

    application = app.create_app()
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app.create_app()

    thread.join(1)
    trello.delete_board(board_id)

@pytest.fixture(scope='module')
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def checkInList(driver, itemName, listClassName, shouldBeInList = True):
    listElement = driver.find_element_by_id(listClassName)
    listItems = listElement.find_elements_by_tag_name('li')
    listItemNames = [item.find_element_by_tag_name('h5').text 
        for item 
        in listItems]

    if (shouldBeInList):
        assert itemName in listItemNames
        return [item for item in listItems if item.find_element_by_tag_name('h5').text == itemName][0]
    else:
        assert itemName not in listItemNames

def test_task_journey(driver, test_app):
    newTaskName = 'New task name'
    driver.get('http://localhost:5000')

    assert driver.title == 'To-Do App'

    # Create new task

    addItemInput = driver.find_element_by_id('name-input')
    addItemButton = driver.find_element_by_id('add-item-btn')

    addItemInput.send_keys(newTaskName)
    addItemButton.click()

    addedItem = checkInList(driver, newTaskName, 'to-do-items')

    # Start task

    startBtn = addedItem.find_element_by_class_name('start-btn')
    startBtn.click()

    checkInList(driver, newTaskName, 'to-do-items', shouldBeInList=False)

    addedItem = checkInList(driver, newTaskName, 'doing-items')

    # Complete task
    completeBtn = addedItem.find_element_by_class_name('complete-btn')
    completeBtn.click()

    checkInList(driver, newTaskName, 'to-do-items', shouldBeInList=False)
    checkInList(driver, newTaskName, 'doing-items', shouldBeInList=False)

    addedItem = checkInList(driver, newTaskName, 'all-done-items')
    
    # Uncomplete task

    uncompleteBtn = addedItem.find_element_by_class_name('uncomplete-btn')
    uncompleteBtn.click()

    checkInList(driver, newTaskName, 'all-done-items', shouldBeInList=False)
    checkInList(driver, newTaskName, 'doing-items')

    driver.close()
