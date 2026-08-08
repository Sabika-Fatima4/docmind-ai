import { useState } from "react";
import api from "../api/client";

function DocumentChat({ document, onBack }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAsk = async (e) => {
    e.preventDefault();

    if (!question.trim() || loading) {
      return;
    }

    const currentQuestion = question.trim();

    setQuestion("");
    setError("");

    setMessages((previous) => [
      ...previous,
      {
        type: "user",
        text: currentQuestion,
      },
    ]);

    setLoading(true);

    try {
      const response = await api.post("/pdf/chat", {
        document_id: document.document_id,
        question: currentQuestion,
      });

      setMessages((previous) => [
        ...previous,
        {
          type: "assistant",
          text: response.data.answer,
          sources: response.data.sources || [],
        },
      ]);
    } catch (err) {
      console.error("CHAT ERROR:", err.response?.data);

      const detail = err.response?.data?.detail;

      setError(
        detail || "Something went wrong while asking DocMind."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-page">

      <header className="chat-header">

        <button
          className="back-button"
          onClick={onBack}
        >
          ← Back
        </button>

        <div className="chat-document">

          <div className="document-icon">
            PDF
          </div>

          <div>
            <h1>{document.filename}</h1>
            <p>Document chat</p>
          </div>

        </div>

      </header>

      <main className="chat-main">

        {messages.length === 0 ? (

          <div className="chat-empty">

            <div className="chat-empty-icon">
              ✦
            </div>

            <h2>Ask anything about this document</h2>

            <p>
              DocMind will search your document and
              generate an answer using the relevant sections.
            </p>

          </div>

        ) : (

          <div className="messages">

            {messages.map((message, index) => (

              <div
                key={index}
                className={`message ${
                  message.type === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
              >

                <div className="message-label">
                  {message.type === "user"
                    ? "You"
                    : "DocMind AI"}
                </div>

                <div className="message-text">
                  {message.text}
                </div>

                {message.sources &&
                  message.sources.length > 0 && (

                    <div className="sources">

                      <div className="sources-title">
                        Sources
                      </div>

                      {message.sources.map(
                        (source, sourceIndex) => (

                          <div
                            className="source-item"
                            key={sourceIndex}
                          >

                            <div>
                              <strong>
                                {source.filename}
                              </strong>

                              {source.page && (
                                <span>
                                  {" "}· Page {source.page}
                                </span>
                              )}
                            </div>

                            <p>
                              {source.text}
                            </p>

                          </div>

                        )
                      )}

                    </div>

                  )}

              </div>

            ))}

            {loading && (
              <div className="message assistant-message">

                <div className="message-label">
                  DocMind AI
                </div>

                <div className="typing">
                  Thinking...
                </div>

              </div>
            )}

          </div>

        )}

        {error && (
          <div className="chat-error">
            {error}
          </div>
        )}

      </main>

      <form
        className="chat-input-area"
        onSubmit={handleAsk}
      >

        <input
          type="text"
          placeholder="Ask a question about this document..."
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          disabled={loading}
        />

        <button
          type="submit"
          className="primary-button"
          disabled={loading || !question.trim()}
        >
          {loading ? "..." : "Ask"}
        </button>

      </form>

    </div>
  );
}

export default DocumentChat;