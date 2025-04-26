import os
import json
from datetime import datetime
from typing import Dict, Any
from .config import Config

class Storage:
    """Handles file storage operations for exported data."""
    
    def __init__(self, config: Config):
        """Initialize the storage handler with configuration."""
        self.config = config
        self.trans_table = self._create_translation_table()

    @staticmethod
    def _create_translation_table() -> dict:
        """Create a translation table for filename sanitization."""
        trans_table = {'&': '+'}
        for bracket in '[{<':
            trans_table.update({bracket: '('})
        for bracket in ']}>':
            trans_table.update({bracket: ')'})
        return str.maketrans(trans_table)

    def sanitize_filename(self, name: str) -> str:
        """Make filenames safer by replacing special characters."""
        name = name.strip()
        name = name.translate(self.trans_table)
        return ''.join([char if char.isalnum() or char in '-_,.!?()"\'…—' else '_' for char in name])

    def write_json(self, data: Dict[str, Any], dir_path: str, name: str, date: datetime) -> None:
        """Write data to a JSON file with proper timestamp."""
        filename = self.sanitize_filename(name)
        dir_path = f'{self.config.export_dir}/{dir_path}'

        timestamp = date.timestamp()
        date_str = date.strftime('%Y%m%d%H%M')
        path = os.path.join(dir_path, f'{date_str}.{filename}.json')
        print(f'Writing to {path}')

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

        os.utime(path, (timestamp, timestamp))

    def write_image(self, image_data: bytes, dir_path: str, name: str, date: datetime) -> None:
        """Write image data to a file with proper timestamp."""
        filename = self.sanitize_filename(name)
        dir_path = f'{self.config.export_dir}/{dir_path}'

        timestamp = date.timestamp()
        date_str = date.strftime('%Y%m%d%H%M')
        path = os.path.join(dir_path, f'{date_str}.{filename}.jpg')
        print(f'Writing to {path}')

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(path, 'wb') as f:
            f.write(image_data)

        os.utime(path, (timestamp, timestamp)) 