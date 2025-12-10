from epub_utils import Document
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


class EpubReader:
    def __init__(self, book_path):
        if not book_path:
            raise ValueError("EPUB book path must be provided.")
        self.doc = Document(book_path)

    def get_metadata(self):
        """
        Get basic metadata of the EPUB book.
        :return: A dictionary containing title, creator, identifier, language, publisher, and date.
        """
        metadata = self.doc.package.metadata
        # Basic Dublin Core elements
        metadata_dict = {
            'title': metadata.title,
            'creator': metadata.creator,
            'identifier': metadata.identifier,
            'language': metadata.language,
            'publisher': metadata.publisher,
            'date': metadata.date,
        }
        return metadata_dict

    def get_table_of_contents(self):
        """
        Get the table of contents (TOC) of the EPUB book.
        :return: A list of TOC items with their text and attributes.
        """
        toc = self.doc.toc
        def parse_ncx(toc_xml: str):
            # 注意要处理 namespace，否则找不到节点
            ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
            root = ET.fromstring(toc_xml)
            navpoints = []
            for np in root.findall(".//ncx:navPoint", ns):
                item = {
                    "id": np.attrib.get("id"),
                    "playOrder": np.attrib.get("playOrder"),
                    "text": np.find(".//ncx:text", ns).text.strip()
                }
                navpoints.append(item)
            return navpoints
        return parse_ncx(str(toc))

    def get_spine_items(self):
        """
        Get the spine items of the EPUB book.
        :return: A list of spine item idrefs.
        """
        spine = self.doc.package.spine
        print(type(spine))
        def parse_spine_idrefs(spine_xml: str):
            ns = {
                'opf': 'http://www.idpf.org/2007/opf'
            }
            root = ET.fromstring(spine_xml)
            idrefs = []
            for item in root.findall('.//opf:itemref', ns):
                idrefs.append(item.attrib.get('idref'))
            return idrefs
        return parse_spine_idrefs(str(spine))

    def get_main_content_by_id(self, id: str):
        """
        Get the main content of the EPUB book by its ID.
        :param id:
        :return: A dictionary containing the title and content paragraphs.
        """
        content_raw = self.doc.find_content_by_id(id)
        def extract_epub_html(html_str: str):
            soup = BeautifulSoup(html_str, "lxml")
            # title 字段 = 第一个 h1 文本
            h1 = soup.find('h1')
            title = h1.get_text(strip=True) if h1 else ""
            # 所有正文段落（p标签）
            content = []
            for p in soup.find_all('p'):
                txt = p.get_text(strip=True)
                if txt:
                    content.append(txt)
            return {
                "title": title.replace("\u3000", " "),
                "content": content
            }
        return extract_epub_html(str(content_raw))

if __name__ == '__main__':
    book_path = '/Users/well/Downloads/春明外史.epub'
    reader = EpubReader(book_path)
    print(reader.get_main_content_by_id('id_11'))