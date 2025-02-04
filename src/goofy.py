import sys
import logging

FILE_EXTENSION_NAME = ".goofy"

LOGGER = logging.getLogger(__name__)

def configure_logging():
    """ Configures logging for goofy lang
    """
    
    logging.basicConfig(
       level=logging.INFO,
       format="[%(asctime)s] %(levelname)s: %(message)s",
       handlers=[
           logging.StreamHandler(sys.stdout), 
        
       ]
    )

def main():
    configure_logging()
    
    if len(sys.argv) < 2:
        LOGGER.info("Goofy lang file was not provided\nUsage: python3 goofy.py <goofy_file>",)
        
        return
    
    if not sys.argv[1].__contains__(FILE_EXTENSION_NAME):
        LOGGER.info("The file you provided is not a valid goofy lang file. Please provide a file with the .goofy extension.")
        
        return
    
    file = sys.argv[1]
    
    # Probably better to read and process at the same time for larger files. but for this language it's okay
    file_lines = []
    
    with open(file, "r", encoding="UTF-8") as file_to_intrepret:
        while current_line := file_to_intrepret.readline():
            file_lines.append(current_line)
        
    if len(file_lines) == 0:
        LOGGER.warning(f"The file you provided has no content. Did you provid the right file? File at: {file}")
        
        return
    
if __name__ == '__main__':
    main()