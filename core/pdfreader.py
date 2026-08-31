import pymupdf
import os

class PDFReader:
    def __init__(self):
        pass
    
    def convert_pdf_to_images(self,file_path):
        folder_name = os.path.basename(file_path).replace(".pdf","")
        output_dir = os.path.join("storage","pdfs",folder_name)
        
        image_paths = []
        
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        
        doc = pymupdf.open(file_path)
        
        for i in range(len(doc)):
            page = doc.load_page(i)
            mat = pymupdf.Matrix(2,2)
            pix = page.get_pixmap(matrix=mat)
            
            image_path = os.path.join(output_dir,f"page_{i}.png")
            
            pix.save(image_path)
            
            image_paths.append(image_path)

        return image_paths