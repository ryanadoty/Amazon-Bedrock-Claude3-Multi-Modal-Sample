import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv
from llm_multi_modal_invoke import image_to_text, text_to_text

# load environment variables
load_dotenv()
# title of the streamlit app
st.title(f""":rainbow[Multi-Modal with Amazon Bedrock and Anthropic Claude 3]""")
st.header(f"""Directions to use this application:
You have several options when it comes to leveraging Claude 3, you can either:
1. Upload an image, and ask a specific question about it by inserting the question into the text box.
2. Upload an image, and let the model describe the image without inserting text.
3. Insert a question in the text box, and let the model answer the question directly without uploading an image.

""", divider='rainbow')
# default container that houses the document upload field
with st.container():
    # header that is shown on the web UI
    st.subheader('Image File Upload:')
    # the file upload field, the specific ui element that allows you to upload the file
    File = st.file_uploader('Upload an Image', type=["png", "jpg", "jpeg"], key="new")
    # when a file is uploaded it saves the file to the directory, creates a path, and invokes the
    # Chunk_and_Summarize Function
    text = st.text_input("Do you have a question about the image? Or about anything in general?")
    result = st.button("Process Image or Answer Question or Both!")
    if result:
        if File is not None:
            st.image(File)
            # determine the path to temporarily save the PDF file that was uploaded
            save_folder = "/Users/rdoty/PycharmProjects/Amazon-Bedrock-Claude3-Multi-Modal-Sample"
            # create a posix path of save_folder and the file name
            save_path = Path(save_folder, File.name)
            # write the uploaded PDF to the save_folder you specified
            with open(save_path, mode='wb') as w:
                w.write(File.getvalue())
            # once the save path exists...
            if save_path.exists():
                # write a success message saying the file has been successfully saved
                st.success(f'File {File.name} is successfully saved!')
                # running the summarization task, and outputting the results to the front end
                st.write(image_to_text(File.name, text))
                # removing the PDF that was temporarily saved to perform the summarization task
                os.remove(save_path)
        else:
            st.write(text_to_text(text))