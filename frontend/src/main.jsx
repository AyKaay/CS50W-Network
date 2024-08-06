// frontend\src\main.jsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import LikeDislike from './LikeDislike';
import EditPost from './EditPost';

// Function to render LikeDislike component
function renderLikeDislikeComponents() {
  document.querySelectorAll('[data-post-id]').forEach(container => {
    const postId = container.getAttribute('data-post-id');
    
    // Render the LikeDislike component into each container
    ReactDOM.createRoot(container).render(
      <React.StrictMode>
        <LikeDislike postId={postId} />
      </React.StrictMode>
    );
  });
}

// TODO Fix edit button toggle (not showing forms)
// Function to toggle and render EditPost component
function handleEditPostButtonClick(event) {
  const postId = event.target.getAttribute('edit-post-button');
  const container = document.getElementById(`edit-post-container-${postId}`);
  
  if (container) {
    // Toggle the visibility of the EditPost container
    if (container.style.display === 'none' || !container.style.display) {
      container.style.display = 'block';
      ReactDOM.createRoot(container).render(
        <React.StrictMode>
          <EditPost postId={postId} />
        </React.StrictMode>
      );
    } 
    else {
      container.style.display = 'none';
    }
  }
}

// Ensure the DOM is loaded before rendering
document.addEventListener('DOMContentLoaded', () => {
  renderLikeDislikeComponents();

  // Add click event listeners for "Edit Post" buttons
  document.querySelectorAll('.edit-post-button').forEach(button => {
    button.addEventListener('click', handleEditPostButtonClick);
  });
});

