import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown'; // Import the react-markdown library
import './ChatbotUI.css';

const ChatbotUI = () => {
  const [messages, setMessages] = useState([]);
  const [image, setImage] = useState(null);

  // Handle sending the image and receiving the bot's response
  const handleSend = async (e) => {
    e.preventDefault();
    if (!image) return; // Only send if an image is uploaded

    const userMessage = {
      sender: "user",
      image: URL.createObjectURL(image),
    };
    setMessages([...messages, userMessage]);

    const botResponse = await getBotResponse(image); // Send image to backend and await response

    const botMessage = {
      sender: "bot",
      text: botResponse.text || "",
      image: botResponse.image || null,
    };
    setMessages((prevMessages) => [...prevMessages, botMessage]);

    setImage(null); // Reset image after sending
  };

  // Function to send image to the server and get a response
  const getBotResponse = async (image) => {
    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await fetch("http://127.0.0.1:5000/image", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        return result; // Return JSON object { text: "...", image: "..." }
      } else {
        console.error("Server error");
        return { text: "Sorry, there was an issue processing your request.", image: null };
      }
    } catch (error) {
      console.error("Error:", error);
      return { text: "Error connecting to the server.", image: null };
    }
  };

  // Handle image upload from the user
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
    }
  };

  return (
    <div className="chatgpt-container">
      <h1 className="welcome-header">Welcome to Instachef</h1> {/* Welcome Header */}
      <div className="chatgpt-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <div className={`message-bubble ${msg.sender}`}>
              {/* Render text using ReactMarkdown */}
              {msg.text && <ReactMarkdown>{msg.text}</ReactMarkdown>}
              {msg.image && <img src={msg.image} alt="Uploaded" className="uploaded-image" />}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSend} className="chatgpt-input-container">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          className="chatgpt-file-input"
        />
        <button type="submit" className="chatgpt-send-button">Send Image</button>
      </form>
    </div>
  );
};

export default ChatbotUI;
