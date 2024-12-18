import React, { useState } from "react";
import Signin from "./signin";
import Login from "./Login";
import Chatbot from "./Chatbot";
import "./App.css";

function App() {
  const [page, setPage] = useState("signin"); // Possible values: signin, login, chatbot
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <div>
      {page === "signin" && <Signin setPage={setPage} />}
      {page === "login" && (
        <Login setPage={setPage} setIsAuthenticated={setIsAuthenticated} />
      )}
      {isAuthenticated && page === "chatbot" && (
        <Chatbot setPage={setPage} setIsAuthenticated={setIsAuthenticated} />
      )}
    </div>
  );
}

export default App;
