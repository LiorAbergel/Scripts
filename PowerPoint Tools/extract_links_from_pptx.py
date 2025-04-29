import win32com.client
import csv
import os

def extract_hyperlinks_from_ppt(filename, output_csv):
    # Initialize the PowerPoint application
    PptApp = win32com.client.Dispatch("Powerpoint.Application")
    PptApp.Visible = True  # Make the PowerPoint application visible

    # Open the PowerPoint presentation in read-write mode
    pptx = PptApp.Presentations.Open(filename, ReadOnly=False)

    # Initialize a set to track seen hyperlinks
    seen_hyperlinks = set()

    # Ensure the output_csv is a full file path with a file name and extension
    if os.path.isdir(output_csv):
        output_csv = os.path.join(output_csv, 'output.csv')

    # Check if the directory exists; create it if it does not
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Open the CSV file for writing
    with open(output_csv, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Slide Number', 'Hyperlink'])

        # Iterate through each slide in the presentation
        for slide in pptx.Slides:
            slide_number = slide.SlideIndex
            # Iterate through each shape on the slide
            for shape in slide.Shapes:
                try:
                    # Check if the shape has a hyperlink
                    if shape.ActionSettings(1).Hyperlink.Address:
                        current_address = shape.ActionSettings(1).Hyperlink.Address
                        if current_address not in seen_hyperlinks:
                            csvwriter.writerow([slide_number, current_address])
                            seen_hyperlinks.add(current_address)  # Mark as seen

                    # If the shape contains text, check the text for embedded hyperlinks
                    if shape.HasTextFrame:
                        text = shape.TextFrame.TextRange.Text
                        if "://" in text and text not in seen_hyperlinks:  # Look for text that contains a URL
                            csvwriter.writerow([slide_number, text])
                            seen_hyperlinks.add(text)  # Mark as seen
                except Exception as e:
                    # If any error occurs (e.g., the shape doesn't have a text frame), continue to the next shape
                    pass

    # Close the PowerPoint application
    PptApp.Quit()
    pptx = None
    PptApp = None

    # Display the total number of unique hyperlinks found
    print(f"Total unique hyperlinks extracted: {len(seen_hyperlinks)}")

# Define the path to the PowerPoint file and the output CSV file
filename = input("Enter the path to the PowerPoint file: ").replace('"', '')
output_csv = input("Enter the path to the output CSV file: ").replace('"', '')

# Run the extraction function
extract_hyperlinks_from_ppt(filename, output_csv)
