import zipfile
import xml.etree.ElementTree as ET

def get_docx_text(path):
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
            root = ET.fromstring(xml_content)
            paragraphs = []
            
            # We want to iterate paragraphs properly. In docx XML:
            # <w:p> represents a paragraph. <w:r> is a run, <w:t> is text.
            # Let's iterate all w:p elements and extract their text.
            namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
            p_tag = f'{namespace}p'
            t_tag = f'{namespace}t'
            br_tag = f'{namespace}br'
            
            for p in root.iter(p_tag):
                p_text = []
                for node in p.iter():
                    if node.tag == t_tag and node.text:
                        p_text.append(node.text)
                    elif node.tag == br_tag:
                        p_text.append('\n')
                paragraphs.append(''.join(p_text))
            
            return '\n'.join(paragraphs)
    except Exception as e:
        import traceback
        return f"Error: {e}\n{traceback.format_exc()}"

with open('BẢNG_MÔ_TẢ_SẢN_PHẨM_docx.txt', 'w', encoding='utf-8') as f:
    f.write(get_docx_text('BẢNG MÔ TẢ SẢN PHẨM.docx'))

with open('Thuyết_minh_thiết_bị_thông_minh_Green_Eye_docx.txt', 'w', encoding='utf-8') as f:
    f.write(get_docx_text('Thuyết minh hiết bị thông minh Green Eye.docx'))

print("Extracted DOCX files successfully.")
