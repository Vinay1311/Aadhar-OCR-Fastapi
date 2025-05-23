from sre_parse import SPECIAL_CHARS
import pytesseract
from PIL import Image
import io
import re
from typing import Dict, Optional

class OCRService:
    def __init__(self):
        self.aadhaar_pattern = r'\d{4} \d{4} \d{4}'
        self.dob_pattern = r'\d{2}/\d{2}/\d{4}'
        self.mobile_pattern = r'\d{10}'
        self.pincode_pattern = r'\b\d{6}\b'
        self.address_keywords = [
            'Address','C/O','S/O','D/O', 'W/O','House','Village','Post','P.O.',
            'Near','Dist','State','C/o','S/o','D/o','W/o','House','Village',
            'Post','P.O.','Near','Dist','State'
        ]

    def extract_text_from_image(self, image_bytes: bytes) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            # print(text)
            return text
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    def parse_aadhaar_text(self, text: str) -> Dict[str, Optional[str]]:
        """
        Parse extracted text to find Aadhaar card details
        """
        result = {}
        lines = text.splitlines()
        
        # Extract basic info
        for line in lines:
            # if 'aadhaar' in line.lower():
            match = re.search(self.aadhaar_pattern, line)
            if match:
                result['aadhaar_number'] = match.group(0)
            
            
            match = re.search(self.dob_pattern, line)
            if match:
                result['dob'] = match.group(0)
            
            match = re.search(self.mobile_pattern, line)
            if match:
                result['mobile_number'] = match.group(0)
            
            line_lower = line.lower()
            if 'female' in line_lower or 'f' in line_lower:
                result['gender'] = 'Female'
            elif 'male' in line_lower or 'm' in line_lower:
                result['gender'] = 'Male'

        # Extract name
        name = None
        dob_index = None
        gender_index = None
        
        # Find DOB and Gender positions
        for i, line in enumerate(lines):
            if re.search(self.dob_pattern, line):
                dob_index = i
            line_lower = line.lower()
            if 'female' in line_lower or 'male' in line_lower:
                gender_index = i
        
        # Try to find name above DOB
        if dob_index and dob_index > 0:
            name_line = lines[dob_index - 1].strip()
            if name_line and any(word[0].isupper() for word in name_line.split()):
                name = name_line
        
        # Try between DOB and Gender
        if not name and gender_index and dob_index:
            for i in range(dob_index + 1, gender_index):
                line = lines[i].strip()
                if line and any(word[0].isupper() for word in line.split()):
                    name = line
                    break
        
        # Try Name/To prefix
        if not name:
            for line in lines:
                if line.startswith(('Name', 'To', 'TO')):
                    name = line.replace('Name', '').replace('To', '').replace('TO', '').strip()
                    if name:
                        break
        
        # Try capitalized words
        if not name:
            for line in lines:
                words = line.split()
                if len(words) >= 2 and all(word[0].isupper() for word in words):
                    name = ' '.join(words)
                    break
                # Check for two consecutive capitals
                for word in words:
                    if len(word) >= 2 and word[:2].isupper():
                        name_words = [w for w in words if w[0].isupper()]
                        if len(name_words) >= 2:
                            name = ' '.join(name_words)
                            break
                if name:
                    break
        
        if name:
            result['name'] = name.title()

        # Extract address
        address_lines = []
        is_address = False
        
        for line in lines:
            if not is_address:
                if any(kw.lower() in line.lower() for kw in self.address_keywords):
                    is_address = True
                    address_lines.append(line)
                    continue
            
            if is_address:
                if any(char.isalpha() or char.isdigit() for char in line):
                    address_lines.append(line)
                    if re.search(self.pincode_pattern, line) and any(kw.lower() in line.lower() for kw in ['dist', 'state', 'pin', 'code']):
                        break
                elif len(address_lines) > 0 and not any(char.isalpha() or char.isdigit() for char in line):
                    break

        if address_lines:
            address_text = ' '.join(address_lines)
            address_text = re.sub(r'["\{}\[\]]', '', address_text)
            address_text = re.sub(r'\s+', ' ', address_text).strip()
            address_text = re.sub(r'^Address\s*:', '', address_text, flags=re.IGNORECASE)
            result['address'] = address_text
        else:
            result['address'] = None

        return result
