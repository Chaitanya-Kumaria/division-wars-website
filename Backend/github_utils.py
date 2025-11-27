import os
import streamlit as st
from github import Github, GithubException

class GitHubManager:
    def __init__(self):
        self.token = st.secrets["github"]["token"]
        self.repo_name = st.secrets["github"]["repo"]
        self.owner = st.secrets["github"]["owner"]
        self.branch = st.secrets["github"]["branch"]
        self.g = Github(self.token)
        self.repo = self.g.get_repo(f"{self.owner}/{self.repo_name}")

    def update_file(self, file_path, content, commit_message):
        """
        Updates a file in the GitHub repository.
        
        Args:
            file_path (str): Relative path to the file in the repo (e.g., 'Backend/Sports/SportsData/Throwball/fixtures.csv')
            content (str): New content of the file.
            commit_message (str): Commit message.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Get the file to get its SHA
            contents = self.repo.get_contents(file_path, ref=self.branch)
            
            # Update the file
            self.repo.update_file(
                path=contents.path,
                message=commit_message,
                content=content,
                sha=contents.sha,
                branch=self.branch
            )
            return True
        except GithubException as e:
            st.error(f"GitHub Error: {e}")
            return False
        except Exception as e:
            st.error(f"Error updating file on GitHub: {e}")
            return False

def save_to_github(file_path, content, commit_message):
    """
    Wrapper function to save content to GitHub.
    """
    if "github" not in st.secrets:
        st.warning("GitHub secrets not configured. Changes saved locally only.")
        return False
        
    try:
        manager = GitHubManager()
        # Convert absolute path to relative path if needed
        # Assuming file_path might be absolute, we need to make it relative to the repo root
        # This part is tricky because we don't know exactly where the repo root is relative to the file system 
        # in all environments, but for this specific app structure:
        
        # If path contains 'Backend', strip everything before it
        if 'Backend' in file_path:
            relative_path = file_path[file_path.find('Backend'):]
        else:
            relative_path = file_path
            
        # Ensure forward slashes
        relative_path = relative_path.replace('\\', '/')
            
        return manager.update_file(relative_path, content, commit_message)
    except Exception as e:
        st.error(f"Failed to initialize GitHub manager: {e}")
        return False
