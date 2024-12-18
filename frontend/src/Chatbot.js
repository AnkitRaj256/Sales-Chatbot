import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import './styles.css'; // Import the CSS file for styles

const Chat = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  
  const chatWindowRef = useRef(null); // Reference for scrolling

  // Load messages from localStorage on initial load
  useEffect(() => {
    const savedMessages = JSON.parse(localStorage.getItem("chatHistory")) || [];
    setMessages(savedMessages);
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("chatHistory", JSON.stringify(messages));
    // Scroll to the bottom when messages update
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSearch = async () => {
    if (!query) return; // Prevent empty queries

    const userMessage = { text: query, sender: 'user', timestamp: new Date().toLocaleString() };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await axios.post("http://localhost:5000/chat", { query });
      const data = res.data;

      const botMessage = { text: data.reply, sender: 'bot', timestamp: new Date().toLocaleString() };
      setMessages((prev) => [...prev, botMessage]);

      // Check if products exist and format the message
      if (data.products && data.products.length > 0) {
        const productDetails = data.products.map(product => 
          `${product.name} - $${product.price}`
        );
        const productMessage = {
          text: productDetails.join('\n'),
          sender: 'bot',
          timestamp: new Date().toLocaleString()
        };
        setMessages((prev) => [...prev, productMessage]);
      }

      setQuery("");
    } catch (error) {
      console.error("Error fetching data:", error);
      const errorMessage = {
        text: "An error occurred while fetching results. Please try again later.",
        sender: 'bot',
        timestamp: new Date().toLocaleString()
      };
      setMessages((prev) => [...prev, errorMessage]);
      setQuery("");
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  const handleReset = () => {
    setMessages([]);
    localStorage.removeItem("chatHistory");
  };

  return (
    <div className="chatbot-container">
      <h1 className="chatbot-title">Sales Chatbot</h1>
      <div className="chat-window" ref={chatWindowRef}>
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <div>{Array.isArray(message.text) ? message.text : message.text.split('\n').map((text, idx) => (
              <div key={idx}>{text}</div>
            ))}</div>
            <div className="timestamp">{message.timestamp}</div>
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Type your message..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyPress}
          className="input-field"
        />
        <button onClick={handleSearch} className="send-button">
          <span>&rarr;</span>
        </button>
        <button onClick={handleReset} className="reset-button">
          Reset
        </button>
      </div>
    </div>
  );
};

export default Chat;
