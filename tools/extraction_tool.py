import os
import json
import shutil
from langchain.tools import tool
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx
from unstructured.partition.text import partition_text

# Add poppler and tesseract to PATH for Windows
POPPLER_BIN = r"C:\Users\info\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin"
TESSERACT_BIN = r"C:\Program Files\Tesseract-OCR"
if os.path.exists(POPPLER_BIN):
    os.environ["PATH"] = POPPLER_BIN + os.pathsep + os.environ["PATH"]
if os.path.exists(TESSERACT_BIN):
    os.environ["PATH"] = TESSERACT_BIN + os.pathsep + os.environ["PATH"]

@tool
def extract_documents(folder_path: str) -> str:
    """
    Extract text, tables, images, graphs from PDF/DOCX/TXT files in a folder
    and save structured JSON to extraction_output/. Also save extracted images to disk.
    """
    output = {
        "text": [],
        "tables": [],
        "images": [],
        "graphs": []
    }

    # Create directories for saving image files
    images_dir = "extraction_output/images"
    graphs_dir = "extraction_output/graphs"
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(graphs_dir, exist_ok=True)

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        ext = os.path.splitext(file)[1].lower()

        try:
            if ext == ".pdf":
                # Use auto strategy with image extraction enabled
                elements = partition_pdf(
                    filename=file_path,
                    extract_images_in_pdf=True,
                    infer_table_structure=True,
                    strategy="auto",  # will try hi_res, fallback to fast
                    extract_image_block_types=["Image", "Figure"],
                )
            elif ext == ".docx":
                elements = partition_docx(filename=file_path)
            elif ext == ".txt":
                elements = partition_text(filename=file_path)
            else:
                continue

            for el in elements:
                meta = el.metadata.to_dict() if el.metadata else {}
                meta["source_file"] = file

                if el.category in ["NarrativeText", "Title", "ListItem", "UncategorizedText", "Header"]:
                    output["text"].append({
                        "content": el.text,
                        "metadata": meta
                    })

                elif el.category == "Table":
                    output["tables"].append({
                        "content": el.text,
                        "metadata": meta
                    })

                elif el.category == "Image":
                    # Determine if it's a graph/figure
                    is_figure = meta.get("image_type") == "figure"
                    # Save image file if possible
                    image_path = None
                    if hasattr(el, 'metadata') and hasattr(el.metadata, 'image_path'):
                        src_path = el.metadata.image_path
                        if src_path and os.path.exists(src_path):
                            # Copy to output directory
                            basename = os.path.basename(src_path)
                            dest_dir = graphs_dir if is_figure else images_dir
                            dest_path = os.path.join(dest_dir, f"{file}_{basename}")
                            shutil.copy2(src_path, dest_path)
                            image_path = dest_path
                            meta["saved_path"] = dest_path
                    
                    item = {
                        "metadata": meta,
                        "image_path": image_path
                    }
                    if is_figure:
                        output["graphs"].append(item)
                    else:
                        output["images"].append(item)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue

    os.makedirs("extraction_output", exist_ok=True)

    for key in output:
        with open(f"extraction_output/{key}.json", "w", encoding="utf-8") as f:
            json.dump(output[key], f, indent=2, ensure_ascii=False)

    return "✅ Extraction finished. JSON files saved in extraction_output/. Images saved in subdirectories."
