from rapidocr_pdf import RapidOCRPDF


class PDFReader:
    def __init__(self, pdf_path=None):
        self.pdf_path = pdf_path
        self.pdf_extractor = RapidOCRPDF()

    def read_pdf(self, pdf_path=None, page_num_list=None, force_ocr=False):
        """
        Read and extract text from the PDF.
        :param pdf_path:
        :param page_num_list:
        :param force_ocr:
        :return: A list of dictionaries containing page number and extracted text.
        """
        if not pdf_path:
            pdf_path = self.pdf_path
            if not pdf_path:
                raise ValueError("PDF path must be provided either during initialization or as an argument.")
        texts = self.pdf_extractor(pdf_path, force_ocr=force_ocr, page_num_list=page_num_list)
        content = []
        for text in texts:
            content.append({
                "page_num": text[0] + 1,
                "text": text[1]
            })
        return content


if __name__ == "__main__":
    pdf = PDFReader("/Users/well/Downloads/screenshot-20251210-180843.pdf")
    print(pdf.read_pdf())