#!/usr/bin/env python3
"""
Document Converter - Any Format to Screenshot
============================================
Converts DOCX, PDF, or any document format to high-quality screenshots
for AI vision processing.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple
import fitz  # PyMuPDF
from PIL import Image
import logging
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentConverter:
    """
    🎯 Convert any document format to high-quality screenshot
    
    Supports:
    - PDF files → Screenshot  
    - DOCX files → PDF → Screenshot
    - Image files → Optimized screenshot
    - Any format LibreOffice can handle
    """
    
    def __init__(self, output_dir: str = "output/screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = self.output_dir.parent / "temp"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎯 DocumentConverter initialized: {self.output_dir}")
        logger.info(f"🎯 Temp directory: {self.temp_dir}")
    
    def convert_to_screenshot(self, file_path: str, output_name: Optional[str] = None) -> str:
        """
        Convert any document to high-quality screenshot
        
        Args:
            file_path: Path to input document
            output_name: Optional custom output name
            
        Returns:
            Path to generated screenshot
        """
        input_path = Path(file_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        # Generate output filename
        if not output_name:
            output_name = f"{input_path.stem}_screenshot"
        
        output_path = self.output_dir / f"{output_name}.png"
        
        logger.info(f"🔄 Converting: {input_path.name} → {output_path.name}")
        
        # Route to appropriate converter based on file type
        file_ext = input_path.suffix.lower()
        
        if file_ext == '.pdf':
            return self._pdf_to_screenshot(input_path, output_path)
        elif file_ext in ['.docx', '.doc']:
            return self._docx_to_screenshot(input_path, output_path)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            return self._image_to_screenshot(input_path, output_path)
        else:
            # Try LibreOffice for other formats
            return self._libreoffice_to_screenshot(input_path, output_path)
    
    def _pdf_to_screenshot(self, input_path: Path, output_path: Path) -> str:
        """Convert PDF to high-quality screenshot using PyMuPDF"""
        try:
            # Open PDF document
            doc = fitz.open(input_path)
            
            if len(doc) == 0:
                raise ValueError("PDF has no pages")
            
            # Get first page (most resume PDFs are single page)
            page = doc[0]
            
            # Render at high DPI for quality (300 DPI)
            matrix = fitz.Matrix(300/72, 300/72)  # 300 DPI scaling
            pix = page.get_pixmap(matrix=matrix)
            
            # Convert to PIL Image for processing
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            
            # Optimize and save
            self._optimize_and_save(image, output_path)
            
            doc.close()
            logger.info(f"✅ PDF converted: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ PDF conversion failed: {e}")
            raise
    
    def _docx_to_screenshot(self, input_path: Path, output_path: Path) -> str:
        """Convert DOCX to screenshot via LibreOffice"""
        try:
            # LibreOffice creates PDF with same name as input file
            temp_pdf = self.temp_dir / f"{input_path.stem}.pdf"
            
            # LibreOffice headless conversion
            cmd = [
                "libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", str(self.temp_dir),
                str(input_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")
            
            # Check if LibreOffice created the PDF
            if temp_pdf.exists():
                screenshot_path = self._pdf_to_screenshot(temp_pdf, output_path)
                temp_pdf.unlink()  # Clean up temp PDF
                return screenshot_path
            else:
                # Debug: list what files were actually created
                temp_files = list(self.temp_dir.glob("*.pdf"))
                raise FileNotFoundError(f"PDF conversion output not found. Expected: {temp_pdf}, Found: {temp_files}")
                
        except Exception as e:
            logger.error(f"❌ DOCX conversion failed: {e}")
            raise
    
    def _image_to_screenshot(self, input_path: Path, output_path: Path) -> str:
        """Optimize existing image for AI vision"""
        try:
            # Open and optimize image
            image = Image.open(input_path)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Optimize and save
            self._optimize_and_save(image, output_path)
            
            logger.info(f"✅ Image optimized: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Image optimization failed: {e}")
            raise
    
    def _libreoffice_to_screenshot(self, input_path: Path, output_path: Path) -> str:
        """Convert any format via LibreOffice → PDF → Screenshot"""
        try:
            # LibreOffice creates PDF with same name as input file
            temp_pdf = self.temp_dir / f"{input_path.stem}.pdf"
            
            cmd = [
                "libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", str(self.temp_dir),
                str(input_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise RuntimeError(f"Format conversion failed: {result.stderr}")
            
            # Check if LibreOffice created the PDF
            if temp_pdf.exists():
                screenshot_path = self._pdf_to_screenshot(temp_pdf, output_path)
                temp_pdf.unlink()  # Clean up
                return screenshot_path
            else:
                # Debug: list what files were actually created
                temp_files = list(self.temp_dir.glob("*.pdf"))
                raise FileNotFoundError(f"Conversion output not found. Expected: {temp_pdf}, Found: {temp_files}")
                
        except Exception as e:
            logger.error(f"❌ Generic conversion failed: {e}")
            raise
    
    def _optimize_and_save(self, image: Image.Image, output_path: Path) -> None:
        """Optimize image for AI vision processing"""
        
        # Resize if too large (max 2048px on longest side for vision APIs)
        max_size = 2048
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Enhance contrast slightly for better text recognition
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        # Save with high quality
        image.save(output_path, "PNG", quality=95, optimize=True)
    
    def get_document_info(self, file_path: str) -> dict:
        """Get basic information about the document"""
        input_path = Path(file_path)
        
        info = {
            "filename": input_path.name,
            "size_mb": round(input_path.stat().st_size / (1024 * 1024), 2),
            "extension": input_path.suffix.lower(),
            "supported": input_path.suffix.lower() in ['.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg']
        }
        
        # For PDFs, get page count
        if input_path.suffix.lower() == '.pdf':
            try:
                doc = fitz.open(input_path)
                info["pages"] = len(doc)
                doc.close()
            except:
                info["pages"] = "unknown"
        
        return info 