## Running the converter

Each time you want to convert something:
1. Put the images and mp3 files you want convert into a folder named "files" (create if it doesn't exist).
2. Ensure each image/mp3 pair have the same name (e.g. "dip_1_2.png" and "dip_1_2.mp3")
3. Open a terminal and navigate to the directory containing the files folder.
4. Run the following command: "docker run -v $(pwd)/files:/files/ elliotdiebold/media-md:mtv1"
5. Your mp4 file will be in the "files" folder, with the same name as the image/mp3.