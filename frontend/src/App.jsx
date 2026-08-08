import { useState } from "react";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/dashboard";
import DocumentChat from "./pages/DocumentChat";

function App() {
  const [page, setPage] = useState("login");

  const [selectedDocument, setSelectedDocument] =
    useState(null);

  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  const handleLogin = () => {
    setIsLoggedIn(true);
    setPage("dashboard");
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsLoggedIn(false);
    setSelectedDocument(null);
    setPage("login");
  };

  const handleOpenDocument = (document) => {
    setSelectedDocument(document);
    setPage("chat");
  };

  const handleBackToDashboard = () => {
    setSelectedDocument(null);
    setPage("dashboard");
  };

  if (!isLoggedIn) {
    if (page === "register") {
      return (
        <Register
          onBackToLogin={() =>
            setPage("login")
          }
        />
      );
    }

    return (
      <Login
        onLogin={handleLogin}
        onRegister={() =>
          setPage("register")
        }
      />
    );
  }

  if (page === "chat" && selectedDocument) {
    return (
      <DocumentChat
        document={selectedDocument}
        onBack={handleBackToDashboard}
      />
    );
  }

  return (
    <Dashboard
      onLogout={handleLogout}
      onOpenDocument={handleOpenDocument}
    />
  );
}

export default App;