from robocorp.tasks import task
from RPA.HTTP import HTTP
from robocorp import browser
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
from RPA.FileSystem import File

import time


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        slowmo=100,
    )
    open_robot_order_website()
    close_annoying_modal()
    get_orders()
    
def close_annoying_modal():
    """Closes annoying popup when opening robot order page"""
    page = browser.page()
    page.get_by_role("button", name="OK").click()


def open_robot_order_website():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    

def get_orders():
    HTTP().download(url="https://robotsparebinindustries.com/orders.csv",  overwrite=True)



