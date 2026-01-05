"""
Backup and Restore Functionality
"""

import shutil
import os
from datetime import datetime

class BackupManager:
    """Handle database backup and restore operations"""

    @staticmethod
    def create_backup(db_path: str, backup_location: str = None) -> str:
        """
        Create a backup of the database

        Args:
            db_path: Path to the database file
            backup_location: Directory to save backup (defaults to same directory as database)

        Returns:
            Path to the backup file
        """
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")

        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"finance_backup_{timestamp}.db"

        # Determine backup location
        if backup_location is None:
            backup_location = os.path.dirname(db_path)

        # Ensure backup directory exists
        os.makedirs(backup_location, exist_ok=True)

        backup_path = os.path.join(backup_location, backup_filename)

        try:
            # Copy database file
            shutil.copy2(db_path, backup_path)
            return backup_path
        except Exception as e:
            raise Exception(f"Failed to create backup: {str(e)}")

    @staticmethod
    def restore_backup(backup_path: str, db_path: str, create_backup_of_current: bool = True) -> bool:
        """
        Restore database from backup

        Args:
            backup_path: Path to the backup file
            db_path: Path to the current database file
            create_backup_of_current: Whether to backup current database before restoring

        Returns:
            True if successful
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        try:
            # Optionally backup current database before restoring
            if create_backup_of_current and os.path.exists(db_path):
                current_backup_dir = os.path.join(os.path.dirname(db_path), 'pre_restore_backups')
                os.makedirs(current_backup_dir, exist_ok=True)
                BackupManager.create_backup(db_path, current_backup_dir)

            # Restore from backup
            shutil.copy2(backup_path, db_path)
            return True

        except Exception as e:
            raise Exception(f"Failed to restore backup: {str(e)}")

    @staticmethod
    def list_backups(backup_directory: str) -> list:
        """
        List all backup files in a directory

        Args:
            backup_directory: Directory to search for backups

        Returns:
            List of tuples: (filename, filepath, size_mb, created_time)
        """
        backups = []

        if not os.path.exists(backup_directory):
            return backups

        try:
            for filename in os.listdir(backup_directory):
                if filename.startswith('finance_backup_') and filename.endswith('.db'):
                    filepath = os.path.join(backup_directory, filename)
                    size_mb = os.path.getsize(filepath) / (1024 * 1024)
                    created_time = datetime.fromtimestamp(os.path.getctime(filepath))

                    backups.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size_mb': size_mb,
                        'created_time': created_time
                    })

            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x['created_time'], reverse=True)

        except Exception as e:
            raise Exception(f"Failed to list backups: {str(e)}")

        return backups

    @staticmethod
    def delete_backup(backup_path: str) -> bool:
        """
        Delete a backup file

        Args:
            backup_path: Path to the backup file to delete

        Returns:
            True if successful
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        try:
            os.remove(backup_path)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete backup: {str(e)}")

    @staticmethod
    def get_database_info(db_path: str) -> dict:
        """
        Get information about the database file

        Args:
            db_path: Path to the database file

        Returns:
            Dictionary with database information
        """
        if not os.path.exists(db_path):
            return {
                'exists': False,
                'path': db_path
            }

        try:
            size_mb = os.path.getsize(db_path) / (1024 * 1024)
            modified_time = datetime.fromtimestamp(os.path.getmtime(db_path))

            return {
                'exists': True,
                'path': db_path,
                'size_mb': size_mb,
                'last_modified': modified_time
            }
        except Exception as e:
            return {
                'exists': True,
                'path': db_path,
                'error': str(e)
            }
