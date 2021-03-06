import pytest
import os
import src.app as app
from threading import Thread
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from dotenv import find_dotenv, load_dotenv
from datetime import datetime


@pytest.fixture(scope='module')
def test_app():
    env_file_path = find_dotenv('.env')
    load_dotenv(env_file_path, override=True)

    selenium_env_file_path = find_dotenv('.env.selenium.test')
    load_dotenv(selenium_env_file_path, override=True)
    os.environ['ANON_ID'] = 'test_write_user'

    application = app.create_app()

    thread = Thread(target=lambda: application.run(
        use_reloader=False, port=8080))
    thread.daemon = True
    thread.start()

    yield application

    thread.join(1)


@pytest.fixture(scope='session')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')

    with webdriver.Chrome(options=opts) as driver:
        yield driver


def get_items_in_list(driver, listClassName):
    try:
        list_element = driver.find_element_by_id(listClassName)
        list_items = list_element.find_elements_by_tag_name('li')
        item_names = [item.find_element_by_tag_name('h5').text
                      for item
                      in list_items]

        return list_items, item_names
    except NoSuchElementException:
        return [], []


def check_in_list(driver, itemName, listClassName, shouldBeInList=True):
    list_items, item_names = get_items_in_list(driver, listClassName)

    if (shouldBeInList):
        assert itemName in item_names
        return [item for item in list_items if item.find_element_by_tag_name('h5').text == itemName][0]
    else:
        assert itemName not in item_names


def check_in_done_list(driver, item_name, shouldBeInList=True):
    all_done_items, all_done_names = get_items_in_list(
        driver, 'all-done-items')
    recent_done_items, recent_done_names = get_items_in_list(
        driver, 'recent-done-items')
    older_done_items, older_done_names = get_items_in_list(
        driver, 'older-done-items')

    done_items = all_done_items + recent_done_items + older_done_items
    done_item_names = all_done_names + recent_done_names + older_done_names

    if (shouldBeInList):
        assert item_name in done_item_names
        return [item for item in done_items if item.find_element_by_tag_name('h5').text == item_name][0]
    else:
        assert item_name not in done_item_names


def test_task_journey(driver, test_app):
    current_date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    newTaskName = 'New task: created %s' % current_date_time
    driver.get('http://localhost:8080')

    assert driver.title == 'To-Do App'

    # Create new task

    addItemInput = driver.find_element_by_id('name-input')
    addItemButton = driver.find_element_by_id('add-item-btn')

    addItemInput.send_keys(newTaskName)
    addItemButton.click()

    addedItem = check_in_list(driver, newTaskName, 'to-do-items')

    # Start task

    startBtn = addedItem.find_element_by_class_name('start-btn')
    startBtn.click()

    check_in_list(driver, newTaskName, 'to-do-items', shouldBeInList=False)

    addedItem = check_in_list(driver, newTaskName, 'doing-items')

    # Complete task
    completeBtn = addedItem.find_element_by_class_name('complete-btn')
    completeBtn.click()

    check_in_list(driver, newTaskName, 'to-do-items', shouldBeInList=False)
    check_in_list(driver, newTaskName, 'doing-items', shouldBeInList=False)

    addedItem = check_in_done_list(driver, newTaskName)

    # Uncomplete task

    uncompleteBtn = addedItem.find_element_by_class_name('uncomplete-btn')
    uncompleteBtn.click()

    check_in_done_list(driver, newTaskName, shouldBeInList=False)
    addedItem = check_in_list(driver, newTaskName, 'doing-items')

    # Delete task
    deleteBtn = addedItem.find_element_by_class_name('delete-btn')
    deleteBtn.click()

    check_in_list(driver, newTaskName, 'todo-items', shouldBeInList=False)
    check_in_list(driver, newTaskName, 'doing-items', shouldBeInList=False)
    check_in_done_list(driver, newTaskName, shouldBeInList=False)
