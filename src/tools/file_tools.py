# src/tools/file_tools.py
"""
File operations module for the MCP Code Sandbox.
Contains all file-related tools for the sandbox environment.
"""
import os
import logging
from typing import Dict, Any

# logger
logger = logging.getLogger('sandbox-server')

class FileTools:
    """File operations for sandboxes"""
    
    def __init__(self, active_sandboxes):
        """Initialize with a reference to the active sandboxes dictionary"""
        self.active_sandboxes = active_sandboxes
    
    def register_tools(self, mcp):
        """Register all file tools with the MCP server"""
        
        @mcp.tool()
        async def list_files(session_id: str, path: str = "/") -> Dict[str, Any]:
            """List files in the sandbox at the specified path.
            
            Args:
                session_id: The unique identifier for the sandbox session
                path: The directory path to list files from (default: root directory)
            
            Returns:
                A dictionary containing the file listing or an error message
            """
            # Check if sandbox exists
            if session_id not in self.active_sandboxes:
                return {"error": f"No sandbox found with session ID: {session_id}. Create a sandbox first."}
            
            # Get the interpreter
            interpreter = self.active_sandboxes[session_id]
            
            try:
                # List files
                files = interpreter.files.list(path)
                return {"path": path, "files": files}
            except Exception as e:
                logger.error(f"Error listing files in sandbox {session_id}: {str(e)}")
                return {"error": f"Error listing files: {str(e)}"}

        @mcp.tool()
        async def read_file(session_id: str, file_path: str) -> Dict[str, Any]:
            """Read the contents of a file in the sandbox.
            
            Args:
                session_id: The unique identifier for the sandbox session
                file_path: The path to the file to read
            
            Returns:
                A dictionary containing the file content or an error message
            """
            # Check if sandbox exists
            if session_id not in self.active_sandboxes:
                return {"error": f"No sandbox found with session ID: {session_id}. Create a sandbox first."}
            
            # Get the interpreter
            interpreter = self.active_sandboxes[session_id]
            
            try:
                # Read the file
                content = interpreter.files.read(file_path)
                return {"path": file_path, "content": content}
            except Exception as e:
                logger.error(f"Error reading file in sandbox {session_id}: {str(e)}")
                return {"error": f"Error reading file: {str(e)}"}

        @mcp.tool()
        async def write_file(session_id: str, file_path: str, content: str) -> Dict[str, Any]:
            """Write content to a file in the sandbox.
            
            Args:
                session_id: The unique identifier for the sandbox session
                file_path: The path to the file to write
                content: The content to write to the file
            
            Returns:
                A dictionary containing a success message or an error message
            """
            # Check if sandbox exists
            if session_id not in self.active_sandboxes:
                return {"error": f"No sandbox found with session ID: {session_id}. Create a sandbox first."}
            
            # Get the interpreter
            interpreter = self.active_sandboxes[session_id]
            
            try:
                # Write the file
                interpreter.files.write(file_path, content)
                return {"path": file_path, "message": "File written successfully"}
            except Exception as e:
                logger.error(f"Error writing file in sandbox {session_id}: {str(e)}")
                return {"error": f"Error writing file: {str(e)}"}

        @mcp.tool()
        async def upload_file(session_id: str, file_name: str, file_content: str, destination_path: str = "/") -> Dict[str, Any]:
            """Upload a file to the sandbox.
            
            Args:
                session_id: The unique identifier for the sandbox session
                file_name: The name of the file to create
                file_content: The content of the file
                destination_path: The directory where the file should be created (default: root directory)
            
            Returns:
                A dictionary containing a success message or an error message
            """
            # Check if sandbox exists
            if session_id not in self.active_sandboxes:
                return {"error": f"No sandbox found with session ID: {session_id}. Create a sandbox first."}
            
            # Get the interpreter
            interpreter = self.active_sandboxes[session_id]
            
            try:
                # Create full file path
                full_path = os.path.join(destination_path, file_name)
                if not full_path.startswith("/"):
                    full_path = "/" + full_path
                    
                # Write the file
                interpreter.files.write(full_path, file_content)
                return {"path": full_path, "message": "File uploaded successfully"}
            except Exception as e:
                logger.error(f"Error uploading file to sandbox {session_id}: {str(e)}")
                return {"error": f"Error uploading file: {str(e)}"}

        @mcp.tool()
        async def delete_file(session_id: str, file_path: str) -> Dict[str, Any]:
            """Delete a file in the sandbox.
            
            Args:
                session_id: The unique identifier for the sandbox session
                file_path: The path to the file to delete
            
            Returns:
                A dictionary containing a success message or an error message
            """
            if session_id not in self.active_sandboxes:
                return {"error": f"No sandbox found with session ID: {session_id}. Create a sandbox first."}
            
            interpreter = self.active_sandboxes[session_id]
            
            try:
                interpreter.files.delete(file_path)
                return {"path": file_path, "message": "File deleted successfully"}
            except Exception as e:
                logger.error(f"Error deleting file in sandbox {session_id}: {str(e)}")
                return {"error": f"Error deleting file: {str(e)}"}

        @mcp.tool()
        async def get_file_metadata(session_id: str, file_path: str) -> Dict[str, Any]:
            """Get metadata for a file in the sandbox.
            
            Args:
                session_id: The unique identifier for the sandbox session
                file_path: The path to the file to get metadata for
            
            Returns:
                A dictionary containing the file metadata or an error message
            """
            if session_id not in self.active_sandboxes:
                return {"error": f"No sandbox found with session ID: {session_id}. Create a sandbox first."}
            
            interpreter = self.active_sandboxes[session_id]
            
            try:
                metadata = interpreter.files.stat(file_path)
                return {"path": file_path, "metadata": metadata}
            except Exception as e:
                logger.error(f"Error getting file metadata in sandbox {session_id}: {str(e)}")
                return {"error": f"Error getting file metadata: {str(e)}"}
                
        # Make the functions available as class methods
        self.list_files = list_files
        self.read_file = read_file
        self.write_file = write_file
        self.upload_file = upload_file
        self.delete_file = delete_file
        self.get_file_metadata = get_file_metadata
        
        return {
            "list_files": list_files,
            "read_file": read_file,
            "write_file": write_file,
            "upload_file": upload_file,
            "delete_file": delete_file,
            "get_file_metadata": get_file_metadata
        }