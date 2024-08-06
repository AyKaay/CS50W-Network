// src/components/LikeDislike.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Get CSRF token from hidden input
const getCsrfToken = () => {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
};

// Set CSRF token in axios default headers
axios.defaults.headers.common['X-CSRFToken'] = getCsrfToken();

// Declare state variable
const LikeDislike = ( {postId} ) => {
    const [likes, setLikes] = useState(0);
    const [dislikes, setDislikes] = useState(0);
    const [liked, setLiked] = useState(false);
    const [disliked, setDisliked] = useState(false);

    // Fetch the initial like/dislike counts and user status (Hook)
    useEffect(() => {
        axios.get(`/api/posts/${postId}/like-dislike/`)
            .then(response => {
                console.log('Response data:', response.data);

                setLikes(response.data.likes);
                setDislikes(response.data.dislikes);
                setLiked(response.data.liked);
                setDisliked(response.data.disliked);
            })
            .catch(error => {
                console.error('Error fetching data', error);
            });
    }, [postId]);

    // Handles like feat.
    const handleLike = () => {
        axios.post(`/api/posts/${postId}/like/`)
            .then (response => {
                setLikes(response.data.likes);
                setDislikes(response.data.dislikes);
                setLiked(response.data.liked);
                setDisliked(response.data.disliked);
            })
            .catch (error => {
                console.error('Error saving data', error);
            });
    };

    //Handles dislike feat.
    const handleDislike = () => {
        axios.post(`/api/posts/${postId}/dislike/`)
            .then(response => {
                setLikes(response.data.likes);
                setDislikes(response.data.dislikes);
                setLiked(response.data.liked);
                setDisliked(response.data.disliked);
            })
            .catch(error => {
                console.error('Error saving disliked data', error);
            });
    };

    // Template render
    return (
        <div>
            <p>Likes: {likes}</p>
            <p>Dislikes: {dislikes}</p>
            <button 
                data-point-id={postId}  // This is a unique ID for the post
                onClick={handleLike}
            >
                {liked ? 'Unlike' : 'Like'}
            </button>

            <button 
                data-point-id={postId}  // This is a unique ID for the post
                onClick={handleDislike}
            >
                {disliked ? 'Undislike' : 'Dislike'}
            </button>
        </div>
    );
}

export default LikeDislike;

/* 
Flow:
    1. Component Mounts: When the LikeDislike component is first rendered, it fetches the initial like/dislike counts and user statuses using the useEffect hook.
    2. Fetching Data: The useEffect hook makes a GET request to retrieve the current like/dislike counts and whether the user has liked or disliked the post.
    3. Displaying Data: The component displays the like and dislike counts, and the buttons are enabled or disabled based on the user’s status.
    4. Handling Clicks: When a button is clicked, the corresponding handler function (handleLike or handleDislike) is called, making a POST request to update the like or dislike status.
    5. Updating State: The state is updated based on the response from the server, and the component re-renders with the new data.
*/