from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import csv
from RPA.PDF import PDF
from RPA.Archive import Archive

import csv, os

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
    download_csv_file()
    open_the_intranet_order_website()
    close_annoying_modal()
    fill_order_with_csv_data()
    archive_receipts()

def open_the_intranet_order_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def close_annoying_modal():
    """Closes annoying popup when opening robot order page"""
    page = browser.page()
    page.get_by_role("button", name="OK").click()

def export_pdf(order_id):
    """After page is populated to correct order, make the order and generate pdf receipt"""
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()
    page.locator("#robot-preview-image").screenshot(path="output/order_preview.png")
    receipt_html = receipt_html + '<img src="output/order_preview.png" alt="Image" style="width: 60px; height: auto;">'

    pdf = PDF()
    pdf.html_to_pdf(receipt_html, "output/pdf/receipt"+order_id+".pdf")

def order_another():
    """Complete form and order another robot"""
    page = browser.page()
    page.click("text=ORDER ANOTHER ROBOT")

def order_robot(order_id):
    """After page is populated to correct order, make the order"""
    page = browser.page()
    
    while(True):
        page.click("button:text('order')")
        
        # Using a CSS selector to find a div with a role of 'alert'
        # alert_divs = page.get_by_role("alert").filter(has_text="danger") #page.locator("#alert-danger")
        if page.get_by_role("alert").filter(has_text="Error").is_visible(): #.filter(has_text="Error").is_enabled():#alert_divs.count() > 0:
            print("Found a div with alert'.")
        else:
            break

    #Export order as PDF
    export_pdf(order_id)

def download_csv_file():
    """Downloads csv file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

def fill_order_with_csv_data():
    """Finds .csv file and populates order with found data"""
    project_path = os.getcwd()
    csv_file_path = project_path + '/orders.csv'
    # Open the CSV file
    csv_file = open(csv_file_path, newline='')
    # Create a csv.reader object
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    # Skip the header row if it exists
    next(csv_reader, None)
    
    # Iterate over each row in the reader object
    for row in csv_reader:
        # Populate order by row in csv
        populate_order(row)
        # Close receipt form and ready the page to order another robot
        order_another()
        close_annoying_modal()

    csv_file.close()

def populate_order(row):
    """Fills an order with csv data"""
    page = browser.page()
    page.select_option("#head", str(row[1]))
    page.set_checked("#id-body-"+str(row[2]), True)
    page.fill('//*[contains(@id, "170")]', str(row[3]))
    page.fill("#address", str(row[4]))
    
    # Capture order id and make an order
    order_id = str(row[0])
    order_robot(order_id)

def archive_receipts():
    """Archive receipt PDFs"""
    project_path = os.getcwd()
    source_directory = project_path + '/output/pdf/'
    archive = Archive()
    zip_file_name = project_path + "/output/archive.zip"
    archive.archive_folder_with_zip(source_directory, zip_file_name)
