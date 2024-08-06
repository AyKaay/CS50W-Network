// src/components/EditPost.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Get CSRF token from hidden input
const getCsrfToken = () => {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
};

// Set CSRF token in axios default headers
axios.defaults.headers.common['X-CSRFToken'] = getCsrfToken();

const EditPost = ({postId}) => {
    const [title, setTitle] = useState('');
    const [body, setBody] = useState('');
    const [image, setImage] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);

    useEffect(() => {
        // Fetch the existing post data when the component mounts
        axios.get(`/api/posts/${postId}/`)
          .then(response => {
            console.log('Response Data:', response.data);
            setTitle(response.data.title); // Set the title state with the fetched data
            setBody(response.data.body); // Set the body state with the fetched data
            setImage(response.data.image); // Set the image state with the fetched data
          })
          .catch(error => {
            console.error('Error fetching data', error);
          });
    }, [postId]); // Dependency array ensures the effect runs when postId changes

    // Handlers
    const handleTitleChange = (e) => setTitle(e.target.value);
    const handleBodyChange = (e) => setBody(e.target.value);
    const handleImageChange = (e) => setImage(e.target.files[0]);

    const handleSubmit = (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('title', title);
        formData.append('body', body);
        if (image) {
            formData.append('image', image);
        }

        // Ensure CSRF Token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        axios.post(`/api/posts/${postId}/edit/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                console.log('Post updated successfully:', response.data);
                setTitle(response.data.title);
                setBody(response.data.body);
                setImageUrl(response.data.image);
            })
            .catch(error => {
                console.error("Error POST (Unable to submit)", error);
            });
    };

    return (
        <div>
          <form onSubmit={handleSubmit}>
            <div>
              <label>Title</label>
              <input type='text' value={title} onChange={handleTitleChange} />
            </div>
            <div>
              <label>Body</label>
              <textarea value={body} onChange={handleBodyChange} />
            </div>
            <div>
              <label>Image</label>
              <input type='file' onChange={handleImageChange} />
              {imageUrl && <img src={imageUrl} alt="Post Image" style={{ maxWidth: '200px', maxHeight: '200px' }} />} {/* Display the existing image */}
            </div>

            <button type="submit">Submit</button>
          </form>
        </div>
      );
}

export default EditPost;